import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm


def draw(file):
    df = pd.read_csv(file)
    df['date'] = pd.to_datetime(df['date'])
    df.set_index("date", inplace=True)
    df = df[["sh_order", "bj_order"]]
    df["dif"] = df["sh_order"] - df["bj_order"]
    df = df[["dif"]]
    df = df.resample('W').sum()

    df = df.diff(1)[1:]
    print df[-8:]

    fig = plt.figure(figsize=(12, 8))
    ax1 = fig.add_subplot(211)
    fig = sm.graphics.tsa.plot_acf(df, lags=60, ax=ax1)
    ax2 = fig.add_subplot(212)
    fig = sm.graphics.tsa.plot_pacf(df, lags=60, ax=ax2)
    plt.show()

    arma_mod24 = sm.tsa.ARMA(df, (7, 3)).fit()
    print(arma_mod24.aic, arma_mod24.bic, arma_mod24.hqic)
    predict_sunspots = arma_mod24.predict('2017-10-22', '2017-11-19', dynamic=True)
    print(predict_sunspots)


if __name__ == "__main__":
    draw("newyork.csv")
