select 
	count(distinct hash) as total,
    name  
from
	scorecard
where
	dtkey = '0422A'
    and riskid = 0
group by
	name
order by
	total desc