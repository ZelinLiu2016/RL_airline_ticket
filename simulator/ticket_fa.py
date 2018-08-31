import itertools
import gym
import numpy as np
import sklearn.pipeline
import sklearn.preprocessing
from sklearn.kernel_approximation import RBFSampler
from sklearn.linear_model import SGDRegressor
import random
import ticket_plotting
from conversion import train_conversion
from datetime_utils import date2str
from predict import get_price_data, predict_order, find_all_tickets
from predict import get_search_data
from user_airline import gen_weekday_airline_dtb
from user_category import gen_weekday_category_dtb
from user_class import gen_weekday_class_dtb
from user_price import load_price_range
import datetime as dt
import pandas as pd


class Estimator(object):
    def __init__(self, obs_example, env):
        self.models = []
        self.scaler = sklearn.preprocessing.StandardScaler()
        self.scaler.fit(obs_example)
        self.featurizer = sklearn.pipeline.FeatureUnion([
            ("rbf1", RBFSampler(gamma=5.0, n_components=100)),
            ("rbf2", RBFSampler(gamma=2.0, n_components=100)),
            ("rbf3", RBFSampler(gamma=1.0, n_components=100)),
            ("rbf4", RBFSampler(gamma=0.5, n_components=100))
        ])
        self.featurizer.fit(self.scaler.transform(obs_example))
        for _ in range(len(env.action_space)):
            model = SGDRegressor(learning_rate="constant")
            model.partial_fit([self.feature_state(env.reset())], [0])
            self.models.append(model)

    def predict(self, s, a=None):
        s = self.feature_state(s)
        if a:
            return self.models[a].predict([s])[0]
        else:
            return [self.models[m].predict([s])[0] for m in range(len(environment.action_space))]

    def update(self, s, a, target):
        s = self.feature_state(s)
        self.models[a].partial_fit([s], [target])

    def feature_state(self, s):
        return self.featurizer.transform(self.scaler.transform([s]))[0]


class Env:
    def __init__(self, days):
        self.action_space = [-10, -5, 0, 5, 10]
        self.day = 0
        self.max_day = days

    def reset(self):
        self.day = 0
        return [0, 0]

    def step(self, pxdiff):
        global meta_dict
        search_date = begin_date + dt.timedelta(days=self.day)
        search_date_str = date2str(search_date)
        search_list = search_dict[search_date_str]
        conv_rate_list = train_conversion(search_date - dt.timedelta(days=TRAIN_DURATION),
                                          search_date - dt.timedelta(days=1), real_df, meta_dict)
        orders, revenue = predict_order(search_date_str, search_list, category_distribution, class_distribution,
                                        airline_distribution, user_price, px_dict, conv_rate_list, meta_dict,
                                        price_diff=pxdiff)
        n_orders, n_revenue = predict_order(search_date_str, search_list, category_distribution, class_distribution,
                                        airline_distribution, user_price, px_dict, conv_rate_list, meta_dict,
                                        price_diff=0)
        self.day += 1
        is_done = self.day == self.max_day
        order_diff = min(max(orders - n_orders, -150), 150)
        return [self.day, order_diff], revenue, is_done, {}


def get_random_obersvation():
    return np.array([(random.randint(0, 89), random.randint(-150, 150)) for _ in range(10000)])


def make_epsilon_greedy_policy(esm, nA, epsilon):
    def epsilon_greedy_policy(observation):
        a = esm.predict(observation)
        best_action = np.argmax(a)
        A = np.ones(nA, dtype=np.float32) * epsilon/nA
        A[best_action] += 1-epsilon
        return A
    return epsilon_greedy_policy


def q_learning_with_value_approximation(env, estm, epoch_num, discount_factor=1.0, epsilon=0.1, epsilon_decay=1.0):
    for i_epoch_num in range(epoch_num):
        policy = make_epsilon_greedy_policy(estm, len(env.action_space), epsilon * epsilon_decay ** i_epoch_num)
        state = env.reset()
        for it in itertools.count():
            action_probs = policy(state)
            action = np.random.choice(np.arange(len(action_probs)), p=action_probs)
            print action
            next_state, reward, done, _ = env.step(action)
            q_values_next = estm.predict(next_state)
            td_target = reward + discount_factor * np.max(q_values_next)
            estm.update(state, action, td_target)

            # stats.episode_rewards[i_epoch_num] += reward
            # stats.episode_lengths[i_epoch_num] = it
            print("\rStep {} @ Episode {}/{}".format(it, i_epoch_num + 1, epoch_num))

            if done:
                print it
                break
            state = next_state


def generate_q_table(esm, env, e):
    ret = {}
    for x in range(env.max_day):
        for y in range(-150, 151):
            z = esm.predict([x, y])
            print z
            action_idx = int(np.where(z == np.max(z))[0].tolist()[0])
            print action_idx
            print x, y, env.action_space[action_idx]
            ret[(x, y)] = env.action_space[action_idx]
    f = open('qtable_e_%.2f.csv' % e, 'w')
    f.write('Day, Diff, Value\n')
    for k, v in ret.items():
        f.write('%d, %d, %f\n' % (k[0], k[1], v))
    f.close()
    return ret


if __name__ == '__main__':
    environment = Env(90)
    observation_examples = get_random_obersvation()
    estimator = Estimator(observation_examples, environment)

    category_distribution = gen_weekday_category_dtb()
    class_distribution = gen_weekday_class_dtb()
    airline_distribution = gen_weekday_airline_dtb()
    user_price = load_price_range()
    search_dict = get_search_data()
    px_dict = get_price_data()
    conv_df = pd.read_csv("data/search/conversion_rate.csv")
    conv_rate = dict(conv_df.values.tolist())
    real_df = pd.read_csv("data/search/order_qty_searchdate.csv", index_col='fdate')
    global meta_dict
    meta_dict = {}

    TRAIN_DURATION = 14
    begin_date = dt.date(2017, 8, 1)
    end_date = dt.date(2018, 4, 20)
    pre_begin_date = begin_date - dt.timedelta(days=TRAIN_DURATION)
    d = pre_begin_date
    while d < begin_date:
        d_str = date2str(d)
        search_list = search_dict[d_str]
        predict_order(d_str, search_list, category_distribution, class_distribution, airline_distribution,
                      user_price, px_dict, conv_rate, meta_dict)
        d = d + dt.timedelta(days=1)

    eps = 1
    q_learning_with_value_approximation(environment, estimator, 100, epsilon=eps)
    generate_q_table(estimator, environment, eps)
    ticket_plotting.plot_cost_to_go_mountain_car(environment, estimator)

