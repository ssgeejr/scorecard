-- select distinct dtkey from scorecard limit 10



select 
	riskid as rid,
	count(distinct hash) as total
from
	scorecard
where
	dtkey = '0422A'
group by
	riskid
order by
	riskid
