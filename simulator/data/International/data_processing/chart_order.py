#encoding:utf-8
#导入需要的模块
import pandas as pd
import matplotlib.pyplot as plt
from pylab import mpl

mpl.rcParams['font.sans-serif'] = ['SimHei'] # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题

#读取CSV数据为numpy record array记录
data1 = pd.read_csv('E:\Ctrip\International\order\PVG-LAX/2016_flt_time_Sun_processed.csv')

#绘图
fig = plt.figure()
ax = fig.add_subplot(111)
#机票价格折线
ax.bar(data1['take_off_time'], data1['order_cnt'],label=u'订单量')
plt.xticks(rotation=90)
for a,b in zip(data1['take_off_time'],data1['order_cnt']):
    plt.text(a, b+10, '%.0f' % b, ha='center', va= 'bottom',fontsize=7)

#图标的标题
ax.set_title(u"2016年周日不同时间段订单量")
#线型示意说明
ax.legend(loc='upper right')

#显示图片
plt.show()

