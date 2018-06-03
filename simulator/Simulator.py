import pandas as pd
import math
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import random
import csv
import datetime as dt

from datetime_utils import str2date, date2str


class_map = {
    1: "Y",
    2: "C",
    3: "F"
}

all_time = ["06:30", "07:00", "07:30", "08:00", "08:30", "09:00", "09:30", "10:00", "10:30", "11:00", "11:30", "12:00",
            "12:30", "13:00", "13:30", "14:00", "14:30", "15:00", "15:30", "16:00", "16:30", "17:00", "17:30", "18:00",
            "18:30", "19:00", "19:30", "20:00", "20:30", "21:00", "21:30", "22:00", "22:30", "23:30"]

# Generate some data for this demonstration.
data = norm.rvs(10.0, 2.5, size=500)

# Fit a normal distribution to the data:

user_data = []


def gaussian(sigma, x, u):
    y = np.exp(-(x - u) ** 2 / (2 * sigma ** 2)) / (sigma * math.sqrt(2 * math.pi))
    return y*sigma + u


def random_generate(probability):
    r = random.random()
    sum = 0
    for i in probability:
        sum += probability[i]
        if sum >= r:
            return i


def load_query_data():
    path_root = "data/data/category"
    distuibution = {}
    for day in range(1, 8):
        for type in range(1, 6):
            file = "%s/%s_category_%d_processed.csv" % (path_root, number_weekday_map[day], type)
            f = open(file, "r")
            data = f.read().split()[1:]
            for d in data:
                time = d.split(',')[0]
                value = int(d.split(',')[1])
                distuibution[(day, time, type)] = value
    return distuibution


def gen_user_type(user_data):
    result = {}
    for day in range(1, 8):
        for time in all_time:
            sum = 0
            for i in range(1, 6):
                sum += user_data.get((day, time, i), 0)
            tmp = {}
            if sum != 0:
                for i in range(1, 6):
                    tmp[i] = float(user_data.get((day, time, i), 0))/sum
                result[(day, time)] = tmp
    return result


def load_class_data():
    path_root = "data/data/class"
    distribution = {}
    for class_ in ['Y', 'C', 'F']:
        for type in range(1, 6):
            file = "%s/2016_%s_%d.csv" % (path_root, class_, type)
            f = open(file, "r")
            data = f.read().split()[1:]
            file = "%s/2017_%s_%d.csv" % (path_root, class_, type)
            f = open(file, "r")
            tmpdata = f.read().split()[1:]
            data = data + tmpdata
            for d in data:
                day = int(d.split(',')[0])
                value = int(d.split(',')[1])
                if day == 0:
                    continue
                else:
                    if (day, class_, type) not in distribution:
                        distribution[(day, class_, type)] = 0
                    distribution[(day, class_, type)] += value
    return distribution


def gen_user_class(user_data):
    result = {}
    for day in range(1, 8):
        for i in range(1, 6):
            sum = 0
            for class_ in ['Y', 'C', 'F']:
                sum += user_data.get((day, class_, i), 0)
            tmp = {}
            if sum != 0:
                for class_ in ['Y', 'C', 'F']:
                    tmp[class_] = float(user_data.get((day, class_, i), 0))/sum
                result[(day, i)] = tmp
    return result


def load_airline_data():
    path_root = "data/data/airline"
    distribution = {}
    for airline in ['AA', 'DL', 'MU', 'UA']:
        for type in range(1, 6):
            file = "%s/2016_%s_%d.csv" % (path_root, airline, type)
            f = open(file, "r")
            data = f.read().split()[1:]
            file = "%s/2017_%s_%d.csv" % (path_root, airline, type)
            f = open(file, "r")
            tmpdata = f.read().split()[1:]
            data += tmpdata
            for d in data:
                day = int(d.split(',')[0])
                value = int(d.split(',')[1])
                if day == 0:
                    continue
                else:
                    if (day, airline, type) not in distribution:
                        distribution[(day, airline, type)] = 0
                    distribution[(day, airline, type)] += value
    return distribution


def gen_user_airline(user_data):
    result = {}
    for day in range(1, 8):
        for i in range(1, 6):
            sum = 0
            for airline in ['AA', 'DL', 'MU', 'UA']:
                sum += user_data.get((day, airline, i), 0)
            tmp = {}
            if sum != 0:
                for airline in ['AA', 'DL', 'MU', 'UA']:
                    tmp[airline] = float(user_data.get((day, airline, i), 0))/sum
                result[(day, i)] = tmp
    return result


def load_price_data():
    path_root = "data/data/PVG-LAX"
    distribution = {}
    for month in range(1, 13):
        file = "%s/2017-%02d.csv" % (path_root,month)
        f = open(file, "r")
        data = f.read().split()[1:]
        for d in data:
            airline = d.split(',')[1]
            class_ = d.split(',')[2]
            if (airline, class_) not in distribution:
                distribution[(airline, class_)] = []
            distribution[(airline, class_)].append(float(d.split(',')[4]))
    return distribution


def gen_user_price(user_data):
    result = {}
    for airline in ['AA', 'DL', 'MU', 'UA']:
        for class_ in ['Y', 'C', 'F']:
            sum = 0
            tmp = user_data.get((airline, class_), [])
            if len(tmp) == 0:
                print airline, class_
                continue
            for px in user_data.get((airline, class_), []):
                sum += px
            result[(airline, class_)] = float(sum)/len(tmp)
    return result


def gen_user_size(user_data, weekday, time):
    sum = 0
    for i in range(1, 6):
        sum += user_data.get((weekday, time, i), 0)
    return sum


class Simulator:
    def __init__(self, size=0, weekday=1, time=""):
        self.Size = size
        self.Weekday = weekday
        self.Time = time
        self.Users = []

    def generate(self, size, weekday, time, query_data, probability, class_probability, airline_p, user_price):
        self.Size = size
        self.Weekday = weekday
        self.Time = time
        self.Users = []
        # self.Size = gen_user_size(query_data, self.Weekday, self.Time)
        for i in range(self.Size):
            name = "User%03d" % (i+1)
            t = random_generate(probability[(weekday, time)])
            c = random_generate(class_probability[(weekday, t)])
            a = random_generate(airline_p[(weekday, t)])
            p = user_price.get((a, c), 0)
            self.Users.append(User(name, t, c, a, p))

    def show(self):
        print "There are %d users at Day %d %s " % (self.Size, self.Weekday, self.Time)
        for u in self.Users:
            u.show()


class User:
    def __init__(self, name, type, class_, airline, price):
        self.Name = name
        self.Type = type
        self.Class = class_
        self.Airline = airline
        self.Price = price

    def choice(self, tickets):
        selected = None
        if len(tickets) > 0:
            return tickets[0]
        for t in tickets:
            if self.Airline == t[0] and self.Class == t[1]:  # self.Price > (t[2] + 5000):
                return t
        return selected

    def choice_1day(self, tickets, yes_tickets):
        selected = None
        yes_ticket = None
        for t in yes_tickets:
            if yes_ticket is None:
                if self.Airline == t[0] and self.Class == t[1]:
                    yes_ticket = t
            else:
                if self.Airline == t[0] and self.Class == t[1] and yes_ticket[2] > t[2]:
                    yes_ticket = t
        if yes_ticket is None:
            return None
        for t in tickets:
            if self.Airline == t[0] and self.Class == t[1] and t[2] <= yes_ticket[2]:#self.Price > (t[2] + 5000):
                return t
        return selected

    def choice_2days(self, tickets, yes_tickets, yesyes_tickets):
        selected = None
        yes_ticket = None
        yesyes_ticket = None
        for t in yesyes_tickets:
            if yesyes_ticket is None:
                if self.Airline == t[0] and self.Class == t[1]:
                    yesyes_ticket = t
            else:
                if self.Airline == t[0] and self.Class == t[1] and yesyes_ticket[2] > t[2]:
                    yesyes_ticket = t
        for t in yes_tickets:
            if yes_ticket is None:
                if self.Airline == t[0] and self.Class == t[1]:
                    yes_ticket = t
            else:
                if self.Airline == t[0] and self.Class == t[1] and yes_ticket[2] > t[2]:
                    yes_ticket = t
        if yes_ticket is None:
            return None
        if yesyes_ticket is None:
            return None
        for t in tickets:
            if self.Airline == t[0] and self.Class == t[1] and t[2] <= yes_ticket[2] and t[2] <= yesyes_ticket[2]:#elf.Price > (t[2] + 5000):
                return t
        return selected

    def show(self):
        print "Name: %s, Type: %d, Class: %s, Airline:%s, Price:%.3f" % (self.Name, self.Type, self.Class,self.Airline, self.Price)
# 1. zhike 2. shanglv 3. santuan 4. daili 5. fenxiaoshang
# 1.Y. economy 2.C. business 3.F. top


def get_order_data():
    file = "data/data/search/order_qtt.csv"
    order_dict = {}
    with open(file, 'rb') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            if row[0] != 'fdate':
                order_dict[row[0]] = row[1]
    return order_dict


def get_search_data():
    file = "data/data/search/Search.csv"
    search_dict = {}
    with open(file, 'rb') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            if row[0] != 'search_date':
                search_dict[row[0]] = [int(row[i]) for i in range(1, len(row))]
    return search_dict


def get_price_data():
    price_dict = {}
    price_list = pd.read_csv("data/data/price/all_price.csv").values.tolist()
    for row in price_list:
        s_d = row[1]
        f_d = row[0].split(' ')[0]
        if (s_d, f_d) not in price_dict:
            price_dict[(s_d, f_d)] = []
        price_dict[(s_d, f_d)].append((row[2], row[3], float(row[5])))
    return price_dict


def make_choice(simulator, query_data, user_type, user_class, user_airline, user_price, search_date, search_dict, price_dict, conversion_rate):
    order_cnt = {}
    search_list = search_dict[search_date]
    global user_data
    for i in range(len(search_list)):
        flight_date = str2date(search_date) + dt.timedelta(days=i)
        week_day = flight_date.weekday() + 1
        flight_date_str = date2str(flight_date)
        search_number = search_list[i]
        simulator.generate(search_number, week_day, "12:00", query_data, user_type, user_class, user_airline, user_price)
        for u in simulator.Users:
            user_data.append((search_date_str, flight_date_str, u.Name, u.Type, u.Class, u.Airline, u.Price))
            tickets = find_all_tickets(search_date, flight_date_str, price_dict)
            # yes_tickets = find_all_tickets(date2str(str2date(search_date)-dt.timedelta(days=1)), flight_date_str, price_dict)
            # yesyes_tickets = find_all_tickets(date2str(str2date(search_date) - dt.timedelta(days=2)), flight_date_str,
            #                                price_dict)
            # ticket_selected = u.choice_2days(tickets, yes_tickets, yesyes_tickets)
            ticket_selected = u.choice(tickets)
            # if ticket_selected is not None:
            if True:
                conv_prob = {0: 1 - conversion_rate[i], 1: conversion_rate[i]}
                conv = random_generate(conv_prob)
                number = order_cnt.get(search_date_str, 0)
                order_cnt[search_date_str] = (number + conv)
    return order_cnt


def find_all_tickets(search_date, flight_date, price_dict):
    ret = price_dict.get((search_date, flight_date), [])
    return ret


def show_result(x):
    x.plot()
    plt.show()
    data = x.values.tolist()
    error = 0
    for i in range(len(data)):
        error += abs(data[i][1]-data[i][0])/(data[i][0] + 0.0)
    print error*100/len(data)


if __name__ == "__main__":
    simulate_orders = {}
    query_data = load_query_data()
    user_type = gen_user_type(query_data)
    user_class = gen_user_class(load_class_data())
    user_airline = gen_user_airline(load_airline_data())
    user_price = gen_user_price(load_price_data())
    s = Simulator()
    search_dict = get_search_data()
    price_dict = get_price_data()
    conversion_df = pd.read_csv("data/data/search/conversion_rate.csv")
    conversion_rate = dict(conversion_df.values.tolist())

    begin_date = dt.date(2017, 5, 1)
    end_date = dt.date(2018, 4, 20)
    search_date = begin_date
    while search_date <= end_date:
        print search_date
        search_date_str = date2str(search_date)
        orders = make_choice(s, query_data, user_type, user_class, user_airline, user_price, search_date_str, search_dict, price_dict, conversion_rate)
        for date_str, order_num in orders.items():
            # simulate_orders[date_str] = (simulate_orders.get(date_str, 0) + order_num)
            if search_date_str not in simulate_orders:
                simulate_orders[search_date_str] = 0
            simulate_orders[search_date_str] += order_num
        search_date = search_date + dt.timedelta(days=1)
    simulate_df = pd.DataFrame(data=[[x, simulate_orders[x]] for x in simulate_orders], columns=["fdate", "predict"]).sort_values(by=['fdate'])
    simulate_df.to_csv("result.csv")
    simulate_df = simulate_df.set_index(['fdate'])
    real_df = pd.read_csv("data/data/search/order_qty_searchdate.csv", index_col='fdate')
    df = pd.concat([real_df, simulate_df], axis=1)
    df.fillna(0, inplace=True)
    df = df[(df.index >= date2str(begin_date)) & (df.index <= date2str(end_date))]
    print df
    user_df = pd.DataFrame(data=user_data, columns=["Search Date", "Flight Date", "Name", "Type", "Class", "Airline", "Price"])
    # user_df.to_csv("user.csv", index=None)
    df.to_csv("result.csv")

    show_result(df)
