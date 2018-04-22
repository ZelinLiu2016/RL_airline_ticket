1、2017年上海飞洛杉矶各舱位不同预定时间价格
select t1.fdate,t1.order_date,t1.airline,t1.class,t1.subclass,percentile(t2.price_tax/persons,0.5) as prc
from 
(
  select orderid,substr(takeofftime,1,10) as fdate,substr(orderdate,1,10) as order_date,airline,class,subclass
   from flt_bidb.DW_FactFltSegment 
  where substr(takeofftime,1,10) >= '2017-01-01' and substr(takeofftime,1,10) <= '2017-01-05' and dport = 'PVG' and aport = 'LAX' and orderstatus = 'S'
) t1
inner join
(
  select orderid,price_tax,persons
   from flt_bidb.DW_FactFltOrder 
) t2
on t1.orderid = t2.orderid
group by t1.fdate,t1.airline,t1.class,t1.subclass,t1.order_date
order by t1.fdate,t1.airline,t1.class,t1.subclass,t1.order_date

