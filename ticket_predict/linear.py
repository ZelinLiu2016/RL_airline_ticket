import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn import metrics
import numpy as np
import matplotlib.pyplot as plt


def get_data(file_name):
    data = pd.read_csv(file_name)
    data['date'] = pd.to_datetime(data['date'])
    data.set_index("date", inplace=True)
    data = data[["sh_order", "bj_order"]]
    data_w = data.resample('W').sum()
    print data_w.corr()
    X_parameter = []
    Y_parameter = []
    for single_square_feet, single_price_value in zip(data_w['bj_order'], data_w['sh_order']):
       X_parameter.append(float(single_square_feet))
       Y_parameter.append(float(single_price_value))
    return X_parameter, Y_parameter


def resample(X, days):
    s = len(X)
    re_X = []
    new_s = s/days
    for i in range(new_s):
        sum = 0
        for j in range(days):
            sum+=X[i*days+j]
        re_X.append(sum)
    return re_X


def linear_train(x_train, y_train, x_test, y_test):
    linreg = LinearRegression()
    linreg.fit(x_train, y_train)
    print "Linear Regression:Y = %.4f * X + %.4f\n"%(linreg.coef_, linreg.intercept_)
    y_pred = linreg.predict(x_test)
    print "RMSE:", np.sqrt(metrics.mean_squared_error(y_test, y_pred))
    rmse = np.sqrt(metrics.mean_squared_error(y_test, y_pred)).tolist()

    sum = 0
    for i in range(len(y_test)):
        sum = sum + y_test[i]
    avg = sum / float(len(y_test))
    value = rmse / avg
    print "RMSE / AVG(Y) = %.4f" % value
    y_test_list = np.array(y_test)
    y_pred_list = np.array(y_pred)
    fig, ax = plt.subplots()
    ax.scatter(y_test_list, y_pred_list)
    ax.plot([y_test_list.min(), y_test_list.max()], [y_test_list.min(), y_test_list.max()], 'k--', lw=4)
    ax.set_xlabel('Measured')
    ax.set_ylabel('Predicted')
    plt.show()


if __name__ == "__main__":
    X, Y = get_data("seattle.csv")
    train_size = int(len(X)/float(10)*9)
    X_train = X[:train_size]
    X_train = [[_]for _ in X_train]
    X_test = X[train_size:]
    X_test = [[_]for _ in X_test]
    Y_train = Y[:train_size]
    Y_test = Y[train_size:]

    linear_train(X_train, Y_train, X_test, Y_test)

