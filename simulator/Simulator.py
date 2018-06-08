import pandas as pd
import math
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import random
import csv
import datetime as dt

from User import User
from datetime_utils import str2date, date2str
from user_category import number_weekday_map
from utils import random_generate

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


def load_query_data():
    path_root = "data/category"
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
    path_root = "data/class"
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
    path_root = "data/airline"
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
    path_root = "data/PVG-LAX"
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

    def generate(self, category_dtb, class_dtb, airline_dtb, price_range):
        self.Size = self.Size
        self.Weekday = self.Weekday
        self.Time = self.Time
        self.Users = []
        for i in range(self.Size):
            name = "User%03d" % (i+1)
            t = random_generate(category_dtb[self.Weekday])
            c = random_generate(class_dtb[(t, self.Weekday)])
            a = random_generate(airline_dtb[(t, self.Weekday)])
            p = price_range.get((a, c), [1000, 20000])
            self.Users.append(User(name, t, c, a, p))

    def show(self):
        print "There are %d users at Day %d %s " % (self.Size, self.Weekday, self.Time)
        for u in self.Users:
            u.show()


def get_order_data():
    file = "data/data/search/order_qtt.csv"
    order_dict = {}
    with open(file, 'rb') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            if row[0] != 'fdate':
                order_dict[row[0]] = row[1]
    return order_dict


if __name__ == "__main__":
    a = {1:1,2:2}
    u = User(a,2,3,4,5)
    a[1] = 3
    print u.Name


