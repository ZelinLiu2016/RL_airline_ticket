import datetime as dt


def str2date(time_str, format="%Y-%m-%d"):
    return dt.datetime.strptime(time_str, format).date()


def date2str(d, format="%Y-%m-%d"):
    return d.strftime(format)


if __name__ == "__main__":
    print str2date("2018-05-07").weekday()
    # print date2str(d)
