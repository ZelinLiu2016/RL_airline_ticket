import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import math


def metrice(test, pred):
    rmse = 0
    avg = 0
    soe = 0
    for i in range(1, len(pred.index)):
        rmse += (test[pred.index[i]] - pred[i])**2
        avg += test[pred.index[i]]
        soe += (float(abs(test[pred.index[i]] - pred[i])))/test[pred.index[i]]
    rmse = rmse/float(len(pred.index)-1)
    rmse = math.sqrt(rmse)
    avg = avg/float(len(pred.index)-1)
    soe = soe/float(len(pred.index)-1)
    print "RMSE: %.3f\nAVG_ORDER: %.3f\nRATIO: %.3f%%\n" %(rmse, avg, 100*rmse/avg)
    print "ERROR: %.3f\n" % (100 * soe)


def get_raw_weekly_data(file):
    df = pd.read_csv("../" + file)
    df['date'] = pd.to_datetime(df['date'])
    df.set_index("date", inplace=True)
    df = df[["sh_order", "bj_order"]]
    df = df.resample('W').sum()
    return df


def get_weekly_data(file):
    df = pd.read_csv("../" + file)
    df['date'] = pd.to_datetime(df['date'])
    df.set_index("date", inplace=True)
    df = df[["sh_order", "bj_order"]]
    df["dif"] = df["sh_order"] - df["bj_order"]
    df = df[["dif"]]
    df = df.resample('W').sum()
    return df


def draw(df1, df2):
    fig, ax = plt.subplots(figsize=(12, 8))
    ax = df1.plot(ax=ax)
    df2.plot(ax=ax)
    plt.show()


def arima_weekly(file, p, q):
    df = get_weekly_data(file)
    df = find_d(df, 1, True)
    train_size = int(len(df)*0.9)
    df_train = df[:train_size]
    find_p_q(df_train)
    predict = train(df_train, p, q)
    return predict


def find_d(df, d, show_figure):
    df = df.diff(d)[d:]
    # df.loc['2017-04-16'] = 48
    if show_figure:
        df.plot()
        plt.show()
    return df


def find_p_q(df):
    fig = plt.figure(figsize=(12, 8))
    ax1 = fig.add_subplot(211)
    fig = sm.graphics.tsa.plot_acf(df, lags=60, ax=ax1)
    ax2 = fig.add_subplot(212)
    fig = sm.graphics.tsa.plot_pacf(df, lags=60, ax=ax2)
    plt.show()


def train(df, p, q):
    arma_mod = sm.tsa.ARMA(df, (p, q)).fit()
    #print(arma_mod.aic, arma_mod.bic, arma_mod.hqic)
    predict_sunspots = arma_mod.predict(df.index[-1], '2017-11-19', dynamic=True)
    return predict_sunspots


if __name__ == "__main__":
    file = "seattle.csv"
    test_data = get_raw_weekly_data(file)
    test_sh = test_data["sh_order"]
    pred_data = arima_weekly(file, 5, 3)
    pred_sh = pred_data + test_sh
    pred_sh = pred_sh.dropna()
    pred_sh[0] = test_sh[pred_sh.index[0]]
    draw(test_sh, pred_sh)
    metrice(test_sh, pred_sh)
