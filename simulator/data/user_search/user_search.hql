1、用户等级分布（0：普通用户 10：黄金用户 20：白金用户 30：钻石用户）
select t2.user_grade as user_grade, count(distinct t1.uid) as user_cnt
from
(
    select uid
      from dw_fltdb.fact_flt_search_detail_tktime5
    where dcityname='上海' and acityname='北京' and substr(d,1,4)='2017'
) t1
inner join
(
    select uid, user_grade 
	  from dw_fltdb.flt_cust_infoandtrans_snap
) t2
on t1.uid = t2.uid
group by t2.user_grade
order by t2.user_grade

2、价格敏感度（0代表价格不敏感的高端用户 1代表亚高端用户 2代表普通用户 3代表价格敏感用户 -1代表缺失值）
select t2.pricesensitivity_fltn as pricesensitivity, count(distinct t1.uid) as user_cnt
from
(
    select uid
      from dw_fltdb.fact_flt_search_detail_tktime5
    where dcityname='上海' and acityname='北京' and substr(d,1,4)='2017'
) t1
inner join
(
    select uid, pricesensitivity_fltn
	  from dw_fltdb.flt_cust_infoandtrans_snap
) t2
on t1.uid = t2.uid
group by t2.pricesensitivity_fltn
order by t2.pricesensitivity_fltn

3、用户价值分（介于0-100，越大价值越高）
select t2.final_pca as final_pca, count(distinct t1.uid) as user_cnt
from
(
    select uid
      from dw_fltdb.fact_flt_search_detail_tktime5
    where dcityname='上海' and acityname='北京' and substr(d,1,4)='2017'
) t1
inner join
(
    select uid, final_pca
	  from dw_fltdb.flt_cust_infoandtrans_snap
) t2
on t1.uid = t2.uid
group by t2.final_pca
order by t2.final_pca

4、是否为两舱用户（满足自2012.01.01开始有坐过一次国内两舱的用户）
select t2.is_fcclass_fltn as is_fcclass, count(distinct t1.uid) as user_cnt
from
(
    select uid
      from dw_fltdb.fact_flt_search_detail_tktime5
    where dcityname='上海' and acityname='北京' and substr(d,1,4)='2017'
) t1
inner join
(
    select uid, is_fcclass_fltn
	  from dw_fltdb.flt_cust_infoandtrans_snap
) t2
on t1.uid = t2.uid
group by t2.is_fcclass_fltn
order by t2.is_fcclass_fltn

5、上一年用户大类（1，直客；2，商旅，3，散团，4，代理,5 ，分销商）
select t2.user_categorylvl1_lastyear as user_category_lastyear, count(distinct t1.uid) as user_cnt
from
(
    select uid
      from dw_fltdb.fact_flt_search_detail_tktime5
    where dcityname='上海' and acityname='北京' and substr(d,1,4)='2017'
) t1
inner join
(
    select uid, user_categorylvl1_lastyear
	  from dw_fltdb.flt_cust_infoandtrans_snap
) t2
on t1.uid = t2.uid
group by t2.user_categorylvl1_lastyear
order by t2.user_categorylvl1_lastyear

6、上一月用户大类（1，直客；2，商旅，3，散团，4，代理,5 ，分销商）
select t2.user_categorylvl1 as user_category, count(distinct t1.uid) as user_cnt
from
(
    select uid
      from dw_fltdb.fact_flt_search_detail_tktime5
    where dcityname='上海' and acityname='北京' and substr(d,1,4)='2017'
) t1
inner join
(
    select uid, user_categorylvl1
	  from dw_fltdb.flt_cust_infoandtrans_snap
) t2
on t1.uid = t2.uid
group by t2.user_categorylvl1
order by t2.user_categorylvl1

7、是否为新用户
select t2.is_new_user as is_newuser, count(distinct t1.uid) as user_cnt
from
(
    select uid
      from dw_fltdb.fact_flt_search_detail_tktime5
    where dcityname='上海' and acityname='北京' and substr(d,1,4)='2017'
) t1
inner join
(
    select uid, is_new_user
	  from dw_fltdb.flt_cust_infoandtrans_snap
) t2
on t1.uid = t2.uid
group by t2.is_new_user
order by t2.is_new_user

8、最近半年国内机票成交订单量
select t2.domflt_last_half_year_cnt as order_last_half_year, count(distinct t1.uid) as user_cnt
from
(
    select uid
      from dw_fltdb.fact_flt_search_detail_tktime5
    where dcityname='上海' and acityname='北京' and substr(d,1,4)='2017'
) t1
inner join
(
    select uid, domflt_last_half_year_cnt
	  from dw_fltdb.flt_cust_infoandtrans_snap
) t2
on t1.uid = t2.uid
group by t2.domflt_last_half_year_cnt
order by t2.domflt_last_half_year_cnt

9、最近一年国内机票成交订单量
select t2.domflt_last_one_year_cnt as order_last_one_year, count(distinct t1.uid) as user_cnt
from
(
    select uid
      from dw_fltdb.fact_flt_search_detail_tktime5
    where dcityname='上海' and acityname='北京' and substr(d,1,4)='2017'
) t1
inner join
(
    select uid, domflt_last_one_year_cnt
	  from dw_fltdb.flt_cust_infoandtrans_snap
) t2
on t1.uid = t2.uid
group by t2.domflt_last_one_year_cnt
order by t2.domflt_last_one_year_cnt

10、是否常驻上海或北京
select t2.is_resident as is_resident, count(distinct t1.uid) as user_cnt
from
(
    select uid
      from dw_fltdb.fact_flt_search_detail_tktime5
    where dcityname='上海' and acityname='北京' and substr(d,1,4)='2017'
) t1
inner join
(
    select uid, multi_resident_cityname like '%上海%' or multi_resident_cityname like '%北京%' as is_resident
	  from dw_fltdb.flt_cust_infoandtrans_snap
) t2
on t1.uid = t2.uid
group by t2.is_resident
order by t2.is_resident

11、用户性别
select t2.gender as gender, count(distinct t1.uid) as user_cnt
from
(
    select uid
      from dw_fltdb.fact_flt_search_detail_tktime5
    where dcityname='上海' and acityname='北京' and substr(d,1,4)='2017'
) t1
inner join
(
    select uid, gender
	  from dw_fltdb.flt_cust_infoandtrans_snap
) t2
on t1.uid = t2.uid
group by t2.gender
order by t2.gender

12、用户年龄分层（0：婴儿（0-2岁）1：儿童（2-12岁）2：青少年（12-18岁）3：18-23岁 4：23-33岁 5：33-55岁 6：55岁以上）
select t2.div_age as age, count(distinct t1.uid) as user_cnt
from
(
    select uid
      from dw_fltdb.fact_flt_search_detail_tktime5
    where dcityname='上海' and acityname='北京' and substr(d,1,4)='2017'
) t1
inner join
(
    select uid, div_age
	  from dw_fltdb.flt_cust_infoandtrans_snap
) t2
on t1.uid = t2.uid
group by t2.div_age
order by t2.div_age

13、不同来源的搜索量
select search_category,count(*) as search_cnt
  from dw_fltdb.fact_flt_search_detail_tktime5
where dcityname='上海' and acityname='北京' and substr(d,1,4)='2017'
group by search_category
order by search_cnt desc 