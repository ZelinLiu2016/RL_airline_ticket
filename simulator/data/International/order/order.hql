1、2017各国际航线订单量排行
select dcityname,dport,acityname,aport,count(distinct OrderID) as order_cnt
  from flt_bidb.DW_FactFltSegment 
where substr(takeofftime,1,4)='2017' and dcityname = '上海' and flightclass = 'I'
group by dcityname,dport,acityname,aport
order by order_cnt desc 

2、2017年PGV飞LAX每日订单量
select substr(takeofftime,1,10) as fdate,count(distinct OrderID) as order_cnt
  from flt_bidb.DW_FactFltOrder 
where dport='PVG' and aport='LAX' and substr(takeofftime,1,4)='2017' and orderstatus = 'S'
group by substr(takeofftime,1,10)
order by substr(takeofftime,1,10)

3、2017年PGV飞LAX每日搜索量 
select substr(d,1,10) as fdate,count(*) as order_cnt
  from dw_fltdb.fact_flt_search_detail_tktime5
where dcityname='上海' and acityname='洛杉矶' and substr(d,1,4)='2017'
group by substr(d,1,10)
order by substr(d,1,10)