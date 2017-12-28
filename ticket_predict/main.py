import pandas as pd
import matplotlib.pyplot as plt


def draw(file):
    df = pd.read_csv(file)
    df['date'] = pd.to_datetime(df['date'])
    df.set_index("date", inplace=True)
    df = df[["sh_order", "bj_order"]]
    df["dif"] = df["sh_order"] - df["bj_order"]
    df = df[["dif"]]
    #df = df.resample('W')
    df.plot()
    plt.show()


if __name__ == "__main__":
    draw("newyork.csv")
