import pandas as pd
import math
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import random


number_weekday_map = {
    1: "Mon",
    2: "Tues",
    3: "Wed",
    4: "Thurs",
    5: "Fri",
    6: "Sat",
    7: "Sun",
}

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
            if len(tmp)==0:
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

    def generate(self, weekday, time, query_data, probability, class_probability, airline_p, user_price):
        self.Size = 0
        self.Weekday = weekday
        self.Time = time
        self.Users = []
        self.Size = gen_user_size(query_data, self.Weekday, self.Time)
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
    def __init__(self, name, type, class_,airline, price):
        self.Name = name
        self.Type = type
        self.Class = class_
        self.Airline = airline
        self.Price = price

    def choice(self):
        return

    def show(self):
        print "Name: %s, Type: %d, Class: %s, Airline:%s, Price:%.3f" % (self.Name, self.Type, self.Class,self.Airline, self.Price)
# 1. zhike 2. shanglv 3. santuan 4. daili 5. fenxiaoshang
# 1.Y. economy 2.C. business 3.F. top


if __name__ == "__main__":
    query_data = load_query_data()
    user_type = gen_user_type(query_data)
    user_class = gen_user_class(load_class_data())
    user_airline = gen_user_airline(load_airline_data())
    user_price = gen_user_price(load_price_data())
    s = Simulator()
    s.generate(1, "10:30", query_data, user_type, user_class, user_airline, user_price)
    s.show()

