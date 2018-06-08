import random
import pandas as pd
import csv


def random_generate(probability):
    r = random.random()
    sum = 0
    for i in probability:
        sum += probability[i]
        if sum >= r:
            return i


def integrate_price():
    df = pd.DataFrame([], columns=['takeofftime','order_date','airline','class','subclass','prc'])
    for i in [2016, 2017, 2018]:
        csv_path = "data/data/price/%4d_prc_time.csv" % i
        new_df = pd.read_csv(csv_path)
        df = pd.concat([df, new_df])
    df.to_csv("all_price.csv", index=None)


def order_qty_searchdate():
    df = pd.DataFrame([], columns=['order_date', 'order_cnt'])
    for i in [2017, 2018]:
        csv_path = "data/%4d_order_qtt_searchdate.csv" % i
        new_df = pd.read_csv(csv_path)
        df = pd.concat([df, new_df])
    df.to_csv("order_qty_searchdate.csv", index=None)


def calculate():
    file = "data/data/search/Search.csv"
    search_dict = {}
    with open(file, 'rb') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            print row
    return search_dict


if __name__ == "__main__":
    order_qty_searchdate()
