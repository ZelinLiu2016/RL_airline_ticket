from datetime_utils import date2str
import datetime as dt


def train_conversion(start_date, end_date, predict_df, history_data):
    today = start_date
    conv_list = []
    while today <= end_date:
        today_str = date2str(today)
        predict = int(predict_df.loc[today_str][0])
        train_list = history_data[today_str]
        sum = 0
        for i in range(181):
            sum += train_list[i] * (1 - (i+0.0) / 180)
        conv = predict/sum
        conv_list.append(conv)
        today = today + dt.timedelta(days=1)
    sum = 0
    for v in conv_list:
        sum += v
    all_conv_rate = float(sum) / len(conv_list)

    last_day = date2str(end_date)
    predict = int(predict_df.loc[last_day][0])
    train_list = history_data[last_day]
    sum = 0
    for i in range(181):
        sum += train_list[i] * (1 - (i + 0.0) / 180)
    last_day_conv = predict / sum

    last_prop = 0.9
    conv_rate = last_day_conv*last_prop + all_conv_rate * (1-last_prop)
    conv_rate = 0.0041
    conv_rate_list = [conv_rate*(1 - i / 180.0) for i in range(181)]
    return conv_rate_list


