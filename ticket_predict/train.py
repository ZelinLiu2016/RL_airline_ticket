import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.model_selection import GridSearchCV
from sklearn import tree
from sklearn import metrics
import numpy as np
from sklearn import preprocessing


data_path = "data/train.csv"


def resample_week(df):
    df_2016 = df[df['d'] < '2017/01/01']
    df_2017 = df[df['d'] >= '2017/01/01']
    data_2016 = df_2016.values.tolist()
    list_2016 = []
    person = 0
    quantity = 0
    for i in range(len(data_2016)):
        person += data_2016[i][2]
        quantity += data_2016[i][3]
        if (i%7 == 6):
            list_2016.append([person,quantity])
            person = 0
            quantity = 0
    data_2017 = df_2017.values.tolist()
    list_2017 = []
    person = 0
    quantity = 0
    for i in range(len(data_2017)):
        person += data_2017[i][2]
        quantity += data_2017[i][3]
        if (i % 7 == 6):
            list_2017.append([person, quantity])
            person = 0
            quantity = 0
    return list_2016, list_2017


def read_data(file):
    all_data = pd.read_csv(file)
    data_1 = all_data[all_data['cityid'] == 1]
    data_2 = all_data[all_data['cityid'] == 2]
    data_3 = all_data[all_data['cityid'] == 3]
    data_1_2016, data_1_2017 = resample_week(data_1)
    data_2_2016, data_2_2017 = resample_week(data_2)
    data_3_2016, data_3_2017 = resample_week(data_3)
    return data_1_2016, data_1_2017, data_2_2016, data_2_2017, data_3_2016, data_3_2017


def tree_train(x_train, y_train, x_test, y_test):
    # svr =GridSearchCV(SVR(kernel='rbf', gamma=0.1), cv=5,
    #                param_grid={"C": [1e0, 1e1, 1e2, 1e3],
    #                            "gamma": np.logspace(-2, 2, 5)})
    clf = tree.DecisionTreeRegressor()
    clf = clf.fit(x_train, y_train)
    y_pred = clf.predict(x_test)
    print y_pred
    mape = 0
    for i in range(len(y_test)):
        mape = mape + abs(float(y_pred[i]-y_test[i])/float(y_test[i]))
    mape = (mape/float(len(y_test)))
    print "MAPE = %.4f" % mape


def svm_train(x_train, y_train, x_test, y_test):
    svr =GridSearchCV(SVR(kernel='rbf', gamma=0.1), cv=5,
                   param_grid={"C": [1e0, 1e1, 1e2, 1e3],
                               "gamma": np.logspace(-2, 2, 5)})
    # svr =SVR(kernel='rbf')
    svr.fit(x_train, y_train)
    y_pred = svr.predict(x_test)
    print y_pred
    mape = 0
    for i in range(len(y_test)):
        mape = mape + abs(float(y_pred[i]-y_test[i])/float(y_test[i]))
    mape = (mape/float(len(y_test)))
    print "MAPE = %.4f" % mape


def linear_train(x_train, y_train, x_test, y_test):
    linreg = LinearRegression()
    linreg.fit(x_train, y_train)
    # print "Linear Regression:Y = %.4f * X + %.4f\n"%(linreg.coef_, linreg.intercept_)
    y_pred = linreg.predict(x_test)
    # print "RMSE:", np.sqrt(metrics.mean_squared_error(y_test, y_pred))
    # rmse = np.sqrt(metrics.mean_squared_error(y_test, y_pred)).tolist()
    #
    # sum = 0
    # for i in range(len(y_test)):
    #     sum = sum + y_test[i]
    # avg = sum / float(len(y_test))
    # value = rmse / avg
    # print "RMSE / AVG(Y) = %.4f" % value
    mape = 0
    for i in range(len(y_test)):
        mape = mape + abs(float(y_pred[i]-y_test[i])/float(y_test[i]))
    mape = (mape/float(len(y_test)))
    print "MAPE = %.4f" % mape
    y_test_list = np.array(y_test)
    y_pred_list = np.array(y_pred)
    fig, ax = plt.subplots()
    ax.scatter(y_test_list, y_pred_list)
    ax.plot([y_test_list.min(), y_test_list.max()], [y_test_list.min(), y_test_list.max()], 'k--', lw=4)
    ax.set_xlabel('Measured')
    ax.set_ylabel('Predicted')
    plt.show()


def Draw(file):
    Data_1_2016, Data_1_2017, Data_2_2016, Data_2_2017, Data_3_2016, Data_3_2017 = read_data(file)
    dif1 = []
    for i in range(len(Data_1_2016)):
        dif1.append(Data_1_2017[i][0]/float(Data_1_2016[i][0]))

    dif2 = []
    for i in range(len(Data_2_2016)):
        dif2.append(Data_2_2017[i][0] /float(Data_2_2016[i][0]))
    # plt.plot(dif1)
    # plt.plot(dif2)
    # plt.plot( [_[0] for _ in Data_1_2016], label='city 1, 2016')
    plt.plot([_[0] for _ in Data_1_2017], label='city 1, 2017')
    plt.plot([_[0] for _ in Data_2_2016], label='city 2, 2016')
    plt.plot([_[0] for _ in Data_2_2017], label='city 2, 2017')
    plt.legend()
    plt.show()


def Linear(file):
    Data_1_2016, Data_1_2017, Data_2_2016, Data_2_2017, Data_3_2016, Data_3_2017 = read_data(file)
    x = [[_[0]] for _ in Data_1_2017]
    y = [_[0] for _ in Data_2_2017]
    train_size = int(round(len(x) * 0.9))
    X_train = x[:train_size]
    X_test = x[train_size:]
    Y_train = y[:train_size]
    Y_test = y[train_size:]
    print train_size
    linear_train(X_train, Y_train, X_test, Y_test)


def Linear_Yearly(file):
    Data_1_2016, Data_1_2017, Data_2_2016, Data_2_2017, Data_3_2016, Data_3_2017 = read_data(file)
    Data_1_2016 = [_[0] for _ in Data_1_2016]
    Data_1_2017 = [_[0] for _ in Data_1_2017]
    Data_2_2016 = [_[0] for _ in Data_2_2016]
    Data_2_2017 = [_[0] for _ in Data_2_2017]
    data_size = len(Data_1_2016)
    X = []
    for i in range(2, data_size):
        order = Data_1_2017[i]/float(Data_1_2016[i])*Data_2_2016[i]
        dif1 = (Data_1_2017[i]-Data_1_2017[i-1])/float(Data_1_2016[i]-Data_1_2016[i-1])*(Data_2_2016[i]-Data_2_2016[i-1])
        dif2 = (Data_1_2017[i-1] - Data_1_2017[i - 2]) / float(Data_1_2016[i-1] - Data_1_2016[i - 2]) * (
        Data_2_2016[i-1] - Data_2_2016[i - 2])
        X.append([Data_1_2017[i], Data_2_2016[i],Data_2_2016[i]-Data_2_2016[i-1], Data_2_2016[i-1] - Data_2_2016[i - 2] ])
    Y = Data_2_2017[2:]
    train_size = int(round(len(X)*0.9))
    X_train = X[:train_size]
    X_test = X[train_size:]
    Y_train = Y[:train_size]
    Y_test = Y[train_size:]
    linear_train(X_train, Y_train, X_test, Y_test)


def SVM_Yearly(file):
    Data_1_2016, Data_1_2017, Data_2_2016, Data_2_2017, Data_3_2016, Data_3_2017 = read_data(file)
    Data_1_2016 = [_[0] for _ in Data_1_2016]
    Data_1_2017 = [_[0] for _ in Data_1_2017]
    Data_2_2016 = [_[0] for _ in Data_2_2016]
    Data_2_2017 = [_[0] for _ in Data_2_2017]
    data_size = len(Data_1_2016)
    X = []
    for i in range(2, data_size):
        order = Data_1_2017[i]/float(Data_1_2016[i])*Data_2_2016[i]
        dif1 = (Data_1_2017[i]-Data_1_2017[i-1])/float(Data_1_2016[i]-Data_1_2016[i-1])*(Data_2_2016[i]-Data_2_2016[i-1])
        dif2 = (Data_1_2017[i-1] - Data_1_2017[i - 2]) / float(Data_1_2016[i-1] - Data_1_2016[i - 2]) * (
        Data_2_2016[i-1] - Data_2_2016[i - 2])
        X.append([Data_1_2017[i], Data_2_2016[i], Data_2_2016[i]-Data_2_2016[i-1], Data_2_2016[i-1] - Data_2_2016[i - 2] ])
        # X.append([order, dif1, dif2])
    Y = Data_2_2017[2:]
    X = preprocessing.scale(X)
    train_size = int(round(len(X)*0.9))
    X_train = X[:train_size]
    X_test = X[train_size:]
    Y_train = Y[:train_size]
    Y_test = Y[train_size:]
    svm_train(X_train, Y_train, X_test, Y_test)


def Tree_Yearly(file):
    Data_1_2016, Data_1_2017, Data_2_2016, Data_2_2017, Data_3_2016, Data_3_2017 = read_data(file)
    Data_1_2016 = [_[0] for _ in Data_1_2016]
    Data_1_2017 = [_[0] for _ in Data_1_2017]
    Data_2_2016 = [_[0] for _ in Data_2_2016]
    Data_2_2017 = [_[0] for _ in Data_2_2017]
    data_size = len(Data_1_2016)
    X = []
    for i in range(2, data_size):
        order = Data_1_2017[i]/float(Data_1_2016[i])*Data_2_2016[i]
        dif1 = (Data_1_2017[i]-Data_1_2017[i-1])/float(Data_1_2016[i]-Data_1_2016[i-1])*(Data_2_2016[i]-Data_2_2016[i-1])
        dif2 = (Data_1_2017[i-1] - Data_1_2017[i - 2]) / float(Data_1_2016[i-1] - Data_1_2016[i - 2]) * (
        Data_2_2016[i-1] - Data_2_2016[i - 2])
        X.append([Data_1_2017[i], Data_2_2016[i], Data_2_2016[i]-Data_2_2016[i-1], Data_2_2016[i-1] - Data_2_2016[i - 2] ])
    Y = Data_2_2017[2:]
    X = preprocessing.scale(X)
    train_size = int(round(len(X)*0.9))
    X_train = X[:train_size]
    X_test = X[train_size:]
    Y_train = Y[:train_size]
    Y_test = Y[train_size:]
    tree_train(X_train, Y_train, X_test, Y_test)


if __name__ == "__main__":
    # Linear(data_path)
    # Linear_Yearly(data_path)
    SVM_Yearly(data_path)
    # Draw(data_path)
    # for i in range(10):
    #     Tree_Yearly(data_path)