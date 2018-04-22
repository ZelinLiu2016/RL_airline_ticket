#encoding:utf-8
#导入需要的模块
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdate

#读取CSV数据为numpy record array记录
unrate = pd.read_csv('E:/Ctrip/2016/avg_prc_day.csv')
unrate['fdate'] = pd.to_datetime(unrate['fdate'])

#绘图
fig = plt.figure()
ax = fig.add_subplot(111)
#机票价格折线
ax.plot(unrate['fdate'], unrate['avg_prc'],label='avg_prc')
#ax.plot(unrate['fdate'], unrate['max_prc'],color='red',label='max_prc')
#ax.plot(unrate['fdate'], unrate['min_prc'],color='yellow',label='min_prc')

#图标的标题
ax.set_title(u"Average tickets price each day in 2016")
#线型示意说明
ax.legend(loc='upper right')
#将X轴格式化为日期形式
ax.xaxis.set_major_formatter(mdate.DateFormatter('%Y-%m'))
plt.xticks(pd.date_range('2016-01-01','2017-01-01',freq='31d'),rotation=30)
fig.autofmt_xdate()

#显示图片
plt.show()

