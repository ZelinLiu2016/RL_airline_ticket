#encoding:utf-8
import pandas as pd
import datetime
import csv

#读取CSV数据
rd = pd.read_csv('E:\Ctrip\International\order\PVG-LAX/2016_flt_time.csv',index_col='take_off_time')
rd.index = pd.to_datetime(rd.index)

#不同时间段内订单数处理
current_time = pd.to_datetime('00:00:00')
end_time = pd.to_datetime('23:00:00')
time_interval = []
order_count = []
x = 0
temp = 0
flag = 0
begin = 0
while current_time <= end_time:
    if x >= rd.size or rd.index[x] >= current_time + datetime.timedelta(minutes=60):
        if flag != 0:
            time_interval.append(current_time)
            order_count.append(temp)
            temp = 0
            flag = 0
        current_time += datetime.timedelta(minutes=60)
    else:
        temp +=  rd['order_cnt'][x]
        x += 1
        flag = 1
        begin = 1

#格式处理
sum1 = sum(order_count)
order_temp = [i / sum1 for i in order_count]
time_temp = []
for i in time_interval:
    i = i.strftime("%H:%M")
    time_temp.append(i)

#写入新文件
csvFile = open('E:\Ctrip\International\order\PVG-LAX/2016_flt_time_processed.csv','w', newline='')
writer = csv.writer(csvFile)
writer.writerow(['take_off_time','order_cnt'])
for i in range(len(time_temp)):
    writer.writerow([time_temp[i],order_count[i]])
csvFile.close()

'''
csvFile1 = open('E:\Ctrip\simulator\data\ser\Total_proportion.csv','w', newline='')
writer1 = csv.writer(csvFile1)
writer1.writerow(['take_off_time','order_cnt'])
for i in range(len(time_temp)):
    writer1.writerow([time_temp[i],order_temp[i]])
csvFile1.close()
'''





