1、价格敏感度（0代表价格不敏感的高端用户 1代表亚高端用户 2代表普通用户 3代表价格敏感用户 -1代表缺失值）
select t2.pricesensitivity_fltn as pricesensitivity, count(distinct t1.uid) as user_cnt
from
(
    select uid
      from flt_bidb.DW_FactFltOrder 
    where dcityname='上海' and acityname='北京' and substr(takeofftime,1,4)='2017'
) t1
inner join
(
    select uid, pricesensitivity_fltn
	  from dw_fltdb.flt_cust_infoandtrans_snap
) t2
on t1.uid = t2.uid
group by t2.pricesensitivity_fltn
order by t2.pricesensitivity_fltn

2、周一不同起飞时间的订单分布
select substr(takeofftime,12,5) as take_off_time,count(distinct OrderID) as order_cnt
  from flt_bidb.DW_FactFltSegment
where dcityname='上海' and acityname='北京' and substr(takeofftime,1,4)='2017' and pmod(datediff(substr(takeofftime,1,10),'2016-12-26'),7) = 0
group by substr(takeofftime,12,5)  
order by substr(takeofftime,12,5)  

3、不同航空公司订单量分布
select airline,count(distinct OrderID) as order_cnt
  from flt_bidb.DW_FactFltSegment 
where dcityname='上海' and acityname='北京' and substr(takeofftime,1,4)='2017'
group by airline
order by order_cnt desc 

4、周一不同起飞时间的用户分类分布（1，直客；2，商旅，3，散团，4，代理,5 ，分销商）
select t1.take_off_time as take_off_time, t2.user_categorylvl1 as user_category, count(distinct t2.uid) as user_cnt
from
(
    select substr(takeofftime,12,5) as take_off_time,uid
      from flt_bidb.DW_FactFltSegment
    where dcityname='上海' and acityname='北京' and substr(takeofftime,1,4)='2017' and pmod(datediff(substr(takeofftime,1,10),'2016-12-26'),7) = 0 
) t1
inner join
(
    select uid, user_categorylvl1
	  from DW_FLTDB.FACT_FLT_USER_CATEGORY    
) t2
on t1.uid = t2.uid 
group by t1.take_off_time,t2.user_categorylvl1  
order by t1.take_off_time,t2.user_categorylvl1  

5、周一不同起飞时间直客数量分布
select t1.take_off_time,count(distinct t2.uid) as user_cnt
from
(
    select substr(takeofftime,12,5) as take_off_time,uid
      from flt_bidb.DW_FactFltSegment
    where dcityname='上海' and acityname='北京' and substr(takeofftime,1,4)='2017' and pmod(datediff(substr(takeofftime,1,10),'2016-12-26'),7) = 0 
) t1
inner join
(
    select uid
	  from DW_FLTDB.FACT_FLT_USER_CATEGORY
    where user_categorylvl1 = 1	  
) t2
on t1.uid = t2.uid 
group by t1.take_off_time
order by t1.take_off_time

6、不同起飞时间直客数量分布
select t1.take_off_time,count(distinct t2.uid) as user_cnt
from
(
    select substr(takeofftime,12,5) as take_off_time,uid
      from flt_bidb.DW_FactFltSegment
    where dcityname='上海' and acityname='北京' and substr(takeofftime,1,4)='2017' 
) t1
inner join
(
    select uid
	  from DW_FLTDB.FACT_FLT_USER_CATEGORY
    where user_categorylvl1 = 1	  
) t2
on t1.uid = t2.uid 
group by t1.take_off_time
order by t1.take_off_time

7、不同星期日直客数量分布
select t1.weekday,count(distinct t2.uid) as user_cnt
from
(
    select pmod(datediff(substr(takeofftime,1,10),'2016-12-26'),7)+1 as weekday,uid
      from flt_bidb.DW_FactFltSegment
    where dcityname='上海' and acityname='北京' and substr(takeofftime,1,4)='2017'  
) t1
inner join
(
    select uid
	  from DW_FLTDB.FACT_FLT_USER_CATEGORY
    where user_categorylvl1 = 1	  
) t2
on t1.uid = t2.uid 
group by pmod(datediff(substr(takeofftime,1,10),'2016-12-26'),7)
order by pmod(datediff(substr(takeofftime,1,10),'2016-12-26'),7)
   
