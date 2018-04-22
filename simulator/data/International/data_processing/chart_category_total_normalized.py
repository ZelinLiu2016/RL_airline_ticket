#encoding:utf-8
#导入需要的模块
import pandas as pd
import matplotlib.pyplot as plt
from pylab import mpl

mpl.rcParams['font.sans-serif'] = ['SimHei'] # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题

#读取CSV数据为numpy record array记录
data1 = pd.read_csv('E:\Ctrip\International/user/2017_weekday_1.csv')
data2 = pd.read_csv('E:\Ctrip\International/user/2017_weekday_2.csv')
data3 = pd.read_csv('E:\Ctrip\International/user/2017_weekday_3.csv')
data4 = pd.read_csv('E:\Ctrip\International/user/2017_weekday_4.csv')
data5 = pd.read_csv('E:\Ctrip\International/user/2017_weekday_5.csv')
weekday=['Total','Mon','Tue','Wed','Thu','Fri','Sat','Sun']

#绘图
fig = plt.figure()
ax = fig.add_subplot(111)
#机票价格折线
proportion_01 = [a/b for a,b in zip(data1['user_cnt'],data1['user_cnt']+data2['user_cnt']+data3['user_cnt']+data4['user_cnt']+data5['user_cnt'])]
proportion_02 = [a/b for a,b in zip(data1['user_cnt']+data2['user_cnt'],data1['user_cnt']+data2['user_cnt']+data3['user_cnt']+data4['user_cnt']+data5['user_cnt'])]
proportion_03 = [a/b for a,b in zip(data1['user_cnt']+data2['user_cnt']+data3['user_cnt'],data1['user_cnt']+data2['user_cnt']+data3['user_cnt']+data4['user_cnt']+data5['user_cnt'])]
proportion_04 = [a/b for a,b in zip(data1['user_cnt']+data2['user_cnt']+data3['user_cnt']+data4['user_cnt'],data1['user_cnt']+data2['user_cnt']+data3['user_cnt']+data4['user_cnt']+data5['user_cnt'])]
proportion_05 = [a/b for a,b in zip(data1['user_cnt']+data2['user_cnt']+data3['user_cnt']+data4['user_cnt']+data5['user_cnt'],data1['user_cnt']+data2['user_cnt']+data3['user_cnt']+data4['user_cnt']+data5['user_cnt'])]
ax.bar(data1['weekday'], proportion_05,label=u'分销商')
ax.bar(data1['weekday'], proportion_04,label=u'代理')
ax.bar(data1['weekday'], proportion_03,label=u'散团')
ax.bar(data1['weekday'], proportion_02,label=u'商旅')
ax.bar(data1['weekday'], proportion_01,label=u'直客')
plt.xticks(data1['weekday'],weekday)
proportion_1 = [a/b for a,b in zip(data1['user_cnt'],data1['user_cnt']+data2['user_cnt']+data3['user_cnt']+data4['user_cnt']+data5['user_cnt'])]
proportion_2 = [a/b for a,b in zip(data2['user_cnt'],data1['user_cnt']+data2['user_cnt']+data3['user_cnt']+data4['user_cnt']+data5['user_cnt'])]
proportion_3 = [a/b for a,b in zip(data3['user_cnt'],data1['user_cnt']+data2['user_cnt']+data3['user_cnt']+data4['user_cnt']+data5['user_cnt'])]
proportion_4 = [a/b for a,b in zip(data4['user_cnt'],data1['user_cnt']+data2['user_cnt']+data3['user_cnt']+data4['user_cnt']+data5['user_cnt'])]
proportion_5 = [a/b for a,b in zip(data5['user_cnt'],data1['user_cnt']+data2['user_cnt']+data3['user_cnt']+data4['user_cnt']+data5['user_cnt'])]
for a,b,c in zip(data1['weekday'],proportion_01,proportion_1):
    plt.text(a, b-0.02, '%.0f%%' % (c*100), ha='center', va= 'bottom',fontsize=7)
for a,b,c in zip(data1['weekday'],proportion_02,proportion_2):
    plt.text(a, b-0.02, '%.0f%%' % (c*100), ha='center', va= 'bottom',fontsize=7)
for a,b,c in zip(data1['weekday'],proportion_03,proportion_3):
    plt.text(a, b-0.015, '%.0f%%' % (c*100), ha='center', va= 'bottom',fontsize=7)
for a,b,c in zip(data1['weekday'],proportion_04,proportion_4):
    plt.text(a, b-0.02, '%.0f%%' % (c*100), ha='center', va= 'bottom',fontsize=7)
for a,b,c in zip(data1['weekday'],proportion_05,proportion_5):
    plt.text(a, b+0.01, '%.3f%%' % (c*100), ha='center', va= 'bottom',fontsize=7)

#图标的标题
ax.set_title(u"2017年各类型旅客比例归一化分布")
#线型示意说明
ax.legend(loc='lower left')

#显示图片
plt.show()

