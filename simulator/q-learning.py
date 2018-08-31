import pandas as pd
import numpy as np
import random
import time

from conversion import train_conversion
from datetime_utils import date2str
from predict import get_price_data, predict_order, find_all_tickets
from predict import get_search_data
from user_airline import gen_weekday_airline_dtb
from user_category import gen_weekday_category_dtb
from user_class import gen_weekday_class_dtb
from user_price import load_price_range
import datetime as dt


def choose_action_by_epsilon_greedy(status, Q_table):
    max_action_idx = [i for i in range(len(actions))]
    if random.random() < epsilon:
        max_action = -1
        for i in range(len(actions)):
            if Q_table[status][i] == max_action:
                max_action_idx.append(i)
            if Q_table[status][i] > max_action:
                max_action_idx = [i]
                max_action = Q_table[status][i]
    random_choice = random.randint(0, len(max_action_idx)-1)
    return max_action_idx[random_choice]


def predictTicket(s, pxdiff):
    global meta_dict
    search_date = begin_date + dt.timedelta(days=s)
    search_date_str = date2str(search_date)
    search_list = search_dict[search_date_str]
    conv_rate_list = train_conversion(search_date - dt.timedelta(days=TRAIN_DURATION),
                                      search_date - dt.timedelta(days=1), real_df, meta_dict)
    orders, revenue = predict_order(search_date_str, search_list, category_distribution, class_distribution,
                           airline_distribution, user_price, px_dict, conv_rate_list, meta_dict, price_diff=pxdiff)
    return orders, revenue


def get_environment_feedback(s, action_name):
    tic, revunue = predictTicket(s, actions[action_name])
    s_ = s + 1
    return s_, revunue
#
#
# def display_status(s, episode, steps):
#     if s == n_status - 1:
#         print('\r{}'.format('Episode: %d, total_steps: %d' % (episode, steps)))
#         time.sleep(1)
#     else:
#         status_list = ['-'] * (n_status - 1) + ['T']
#         status_list[s] = 'o'
#         print('\r{}'.format(''.join(status_list)), end='')
#         time.sleep(0.3)


def Q_learning(Q_table):
    theta = [0, 0]
    for episode in range(max_episodes):
        print episode
        s = 0
        while s < n_status:
            print s
            a = choose_action_by_epsilon_greedy(s, Q_table)
            s_, r = get_environment_feedback(s, a)
            Q_old = Q_table[s][a]
            max_new_q = -1
            for i in range(len(actions)):
                if Q_table[s_][i] > max_new_q:
                    max_new_q = Q_table[s_][i]
            Q_new = r + gamma * max_new_q
            A = r - (theta[0] * actions[a] + theta[1] * 1)
            theta[0] += A*alpha*actions[a]
            theta[1] += A*alpha*1
            Q_table[s][a] = (1 - alpha) * Q_old + alpha * Q_new
            s = s_
    print theta
    return Q_table


if __name__ == "__main__":
    n_status = 10
    actions = [-10, -5, 0, 5, 10]
    tickets = 5000
    epsilon = 0.8
    alpha = 0.1
    gamma = 0.9
    max_episodes = 10
    Q_table = {}

    simulate_orders = {}
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
    for i in range(0, n_status + 1, 1):
        Q_table[i] = [0] * len(actions)
    a = (Q_learning(Q_table))
    print a