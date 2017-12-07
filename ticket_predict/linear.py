import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn import metrics
import numpy as np
import matplotlib.pyplot as plt


def get_data(file_name):
    data = pd.read_csv(file_name)
    X_parameter = []
    Y_parameter = []
    for single_square_feet, single_price_value in zip(data['bj_order'], data['sh_order']):
       X_parameter.append([float(single_square_feet)])
       Y_parameter.append(float(single_price_value))
    return X_parameter, Y_parameter


def linear_train(x_train, y_train, x_test, y_test):
    linreg = LinearRegression()
    linreg.fit(x_train, y_train)
    print linreg.intercept_
    print linreg.coef_
    y_pred = linreg.predict(x_test)
    print "MSE:", metrics.mean_squared_error(y_test, y_pred)
    print "RMSE:", np.sqrt(metrics.mean_squared_error(y_test, y_pred))
    y_test_list = np.array(y_test)
    y_pred_list = np.array(y_pred)
    fig, ax = plt.subplots()
    ax.scatter(y_test_list, y_pred_list)
    ax.plot([y_test_list.min(), y_test_list.max()], [y_test_list.min(), y_test_list.max()], 'k--', lw=4)
    ax.set_xlabel('Measured')
    ax.set_ylabel('Predicted')
    plt.show()


if __name__ == "__main__":
    X, Y = get_data("data.csv")
    ONE_YEAR = 364
    X = X[:686]
    Y = Y[:686]
    X_train = X[:ONE_YEAR]
    X_test = X[ONE_YEAR:]
    Y_train = Y[:ONE_YEAR]
    Y_test = Y[ONE_YEAR:]
    linear_train(X_train, Y_train, X_test, Y_test)

