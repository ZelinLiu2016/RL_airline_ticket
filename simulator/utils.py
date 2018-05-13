import pandas as pd
import csv

def integrate_price():
    df = pd.DataFrame([], columns=['takeofftime','order_date','airline','class','subclass','prc'])
    for i in [2016, 2017, 2018]:
        csv_path = "data/data/price/%4d_prc_time.csv" % i
        new_df = pd.read_csv(csv_path)
        df = pd.concat([df, new_df])
    df.to_csv("all_price.csv", index=None)


def calculate():
    file = "data/data/search/Search.csv"
    search_dict = {}
    with open(file, 'rb') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            print row
    return search_dict


if __name__ == "__main__":
    calculate()