select
	count(*) as total,
	b.risk
from
    sep21 a,
	plugin b
where
	a.pluginid > 99588
    and a.pluginid = b.pluginid
    and b.riskid > -1
group by
	b.risk