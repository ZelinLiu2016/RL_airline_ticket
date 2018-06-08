import csv
import datetime as dt
import pandas as pd
from Simulator import Simulator
from conversion import train_conversion
from datetime_utils import str2date, date2str
from user_price import load_price_range
from user_airline import gen_weekday_airline_dtb
from utils import random_generate
from user_category import gen_weekday_category_dtb
from user_class import gen_weekday_class_dtb
import matplotlib.pyplot as plt


def show_result(x):
    x.plot()
    plt.show()
    data = x.values.tolist()
    error = 0
    for i in range(len(data)):
        error += abs(data[i][1]-data[i][0])/(data[i][0] + 0.0)
    print error*100/len(data)


def get_search_data():
    file = "data/search/Search.csv"
    search_dict = {}
    with open(file, 'rb') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            if row[0] != 'search_date':
                search_dict[row[0]] = [int(row[i]) for i in range(1, len(row))]
    return search_dict


def get_price_data():
    price_dict = {}
    price_list = pd.read_csv("data/price/all_price.csv").values.tolist()
    for row in price_list:
        s_d = row[1]
        f_d = row[0].split(' ')[0]
        if (s_d, f_d) not in price_dict:
            price_dict[(s_d, f_d)] = []
        price_dict[(s_d, f_d)].append((row[2], row[3], float(row[5])))
    return price_dict


def find_all_tickets(search_date, flight_date, price_dict):
    ret = price_dict.get((search_date, flight_date), [])
    return ret


def predict_order(s_d_str, s_list, category_dtb, class_dtb, airline_dtb, price_range, price_dict, conversion_rate, history_unconv):
    # search_list: search cnt for different days after current day
    # simulator: a simulator
    order_cnt = 0
    history_unconv[s_d_str] = [0]*181
    for i in range(len(s_list)):
        flight_date = str2date(s_d_str) + dt.timedelta(days=i)
        week_day = flight_date.weekday() + 1
        flight_date_str = date2str(flight_date)
        search_number = s_list[i]
        simulator = Simulator(search_number, week_day)
        simulator.generate(category_dtb, class_dtb, airline_dtb, price_range)
        for u in simulator.Users:
            # user_data.append((search_date_str, flight_date_str, u.Name, u.Type, u.Class, u.Airline, u.Price))
            tickets = find_all_tickets(s_d_str, flight_date_str, price_dict)
            # yes_tickets = find_all_tickets(date2str(str2date(search_date)-dt.timedelta(days=1)), flight_date_str, price_dict)
            # yesyes_tickets = find_all_tickets(date2str(str2date(search_date) - dt.timedelta(days=2)), flight_date_str,
            #                                price_dict)
            # ticket_selected = u.choice_2days(tickets, yes_tickets, yesyes_tickets)
            ticket_selected = u.choice(tickets)
            if ticket_selected is not None:
                history_unconv[s_d_str][i] += 1
                conv_prob = {0: 1 - conversion_rate[i], 1: conversion_rate[i]}
                conv = random_generate(conv_prob)
                order_cnt += conv
    return order_cnt


if __name__ == "__main__":
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
    search_date = begin_date
    while search_date <= end_date:
        print search_date
        search_date_str = date2str(search_date)
        search_list = search_dict[search_date_str]
        conv_rate_list = train_conversion(search_date - dt.timedelta(days=TRAIN_DURATION), search_date - dt.timedelta(days=1), real_df, meta_dict)
        orders = predict_order(search_date_str, search_list, category_distribution, class_distribution, airline_distribution, user_price, px_dict, conv_rate_list, meta_dict)
        simulate_orders[search_date_str] = orders
        search_date = search_date + dt.timedelta(days=1)

    simulate_df = pd.DataFrame(data=[[x, simulate_orders[x]] for x in simulate_orders], columns=["fdate", "predict"]).sort_values(by=['fdate'])
    simulate_df.to_csv("result.csv")
    simulate_df = simulate_df.set_index(['fdate'])
    df = pd.concat([real_df, simulate_df], axis=1)
    df.fillna(0, inplace=True)
    df = df[(df.index >= date2str(begin_date)) & (df.index <= date2str(end_date))]
    print df
    # user_df = pd.DataFrame(data=user_data, columns=["Search Date", "Flight Date", "Name", "Type", "Class", "Airline", "Price"])
    # user_df.to_csv("user.csv", index=None)
    df.to_csv("result.csv")

    show_result(df)
