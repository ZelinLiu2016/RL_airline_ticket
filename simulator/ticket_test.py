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


def load_qtable(file_path):
    ret = {}
    f = open(file_path, 'r')
    t = f.read().split('\n')[1:-1]
    for dd in t:
        data = dd.split(',')
        ret[(int(data[0]), int(data[1]))] = float(data[2])
    return ret


def load_qtable_3d(file_path):
    ret = {}
    f = open(file_path, 'r')
    t = f.read().split('\n')[1:-1]
    for dd in t:
        data = dd.split(',')
        ret[(int(data[0]), int(data[1]), int(data[2]))] = float(data[3])
    return ret


def test():
    qtable = load_qtable('qtable_e_1.00.csv')
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

    label_revenue = 0
    test_revenue = 0
    test_time = 100
    for j in range(test_time):
        print j
        for i in range(90):
            s_date = begin_date + dt.timedelta(days=i)
            search_date_str = date2str(s_date)
            search_list = search_dict[search_date_str]
            conv_rate_list = train_conversion(s_date - dt.timedelta(days=TRAIN_DURATION), s_date - dt.timedelta(days=1),
                                              real_df, meta_dict)
            orders, r = predict_order(search_date_str, search_list, category_distribution, class_distribution,
                                      airline_distribution, user_price, px_dict, conv_rate_list, meta_dict,
                                      price_diff=5)
            label_revenue += r

    for j in range(test_time):
        print j
        o_diff = 0
        for i in range(90):
            s_date = begin_date + dt.timedelta(days=i)
            search_date_str = date2str(s_date)
            search_list = search_dict[search_date_str]
            conv_rate_list = train_conversion(s_date - dt.timedelta(days=TRAIN_DURATION), s_date - dt.timedelta(days=1),
                                              real_df, meta_dict)
            pdf = qtable[(i, o_diff)]
            orders, r = predict_order(search_date_str, search_list, category_distribution, class_distribution,
                                      airline_distribution, user_price, px_dict, conv_rate_list, meta_dict,
                                      price_diff=pdf)
            n_orders, n_r = predict_order(search_date_str, search_list, category_distribution, class_distribution,
                                          airline_distribution, user_price, px_dict, conv_rate_list, meta_dict,
                                          price_diff=0)
            test_revenue += r
            o_diff = orders - n_orders
            o_diff = min(max(o_diff, -150), 150)
    print test_revenue / test_time, label_revenue / test_time
    print test_revenue / test_time / (label_revenue / test_time)


def test3d():
    qtable = load_qtable('qtable_e_1.00.csv')
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

    label_revenue = 0
    test_revenue = 0
    test_time = 100
    for j in range(test_time):
        print j
        for i in range(90):
            s_date = begin_date + dt.timedelta(days=i)
            search_date_str = date2str(s_date)
            search_list = search_dict[search_date_str]
            conv_rate_list = train_conversion(s_date - dt.timedelta(days=TRAIN_DURATION), s_date - dt.timedelta(days=1),
                                              real_df, meta_dict)
            orders, r = predict_order(search_date_str, search_list, category_distribution, class_distribution,
                                      airline_distribution, user_price, px_dict, conv_rate_list, meta_dict,
                                      price_diff=5)
            label_revenue += r

    for j in range(test_time):
        print j
        o_diff = 0
        for i in range(90):
            s_date = begin_date + dt.timedelta(days=i)
            search_date_str = date2str(s_date)
            search_list = search_dict[search_date_str]
            conv_rate_list = train_conversion(s_date - dt.timedelta(days=TRAIN_DURATION), s_date - dt.timedelta(days=1),
                                              real_df, meta_dict)

            n_orders, n_r = predict_order(search_date_str, search_list, category_distribution, class_distribution,
                                          airline_distribution, user_price, px_dict, conv_rate_list, meta_dict,
                                          price_diff=0)
            pdf = qtable[(i, o_diff, n_orders)]
            orders, r = predict_order(search_date_str, search_list, category_distribution, class_distribution,
                                      airline_distribution, user_price, px_dict, conv_rate_list, meta_dict,
                                      price_diff=pdf)
            test_revenue += r
            o_diff = orders - n_orders
            o_diff = min(max(o_diff, -150), 150)
    print test_revenue / test_time, label_revenue / test_time
    print test_revenue / test_time / (label_revenue / test_time)


if __name__ == '__main__':
    qtable = load_qtable('qtable_e_1.00.csv')
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

    label_revenue = 0
    test_revenue = 0
    test_time = 100
    for j in range(test_time):
        print j
        for i in range(90):
            s_date = begin_date + dt.timedelta(days=i)
            search_date_str = date2str(s_date)
            search_list = search_dict[search_date_str]
            conv_rate_list = train_conversion(s_date - dt.timedelta(days=TRAIN_DURATION), s_date - dt.timedelta(days=1),
                                              real_df, meta_dict)
            orders, r = predict_order(search_date_str, search_list, category_distribution, class_distribution,
                                      airline_distribution, user_price, px_dict, conv_rate_list, meta_dict,
                                      price_diff=5)
            label_revenue += r

    for j in range(test_time):
        print j
        o_diff = 0
        for i in range(90):
            s_date = begin_date + dt.timedelta(days=i)
            search_date_str = date2str(s_date)
            search_list = search_dict[search_date_str]
            conv_rate_list = train_conversion(s_date - dt.timedelta(days=TRAIN_DURATION), s_date - dt.timedelta(days=1),
                                              real_df, meta_dict)
            pdf = qtable[(i, o_diff)]
            orders, r = predict_order(search_date_str, search_list, category_distribution, class_distribution,
                                      airline_distribution, user_price, px_dict, conv_rate_list, meta_dict,
                                      price_diff=pdf)
            n_orders, n_r = predict_order(search_date_str, search_list, category_distribution, class_distribution,
                                      airline_distribution, user_price, px_dict, conv_rate_list, meta_dict,
                                      price_diff=0)
            test_revenue += r
            o_diff = orders - n_orders
            o_diff = min(max(o_diff, -150), 150)
    print test_revenue/test_time, label_revenue/test_time
    print test_revenue/test_time / (label_revenue/test_time)
