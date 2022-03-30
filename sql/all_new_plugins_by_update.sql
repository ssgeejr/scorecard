select
count(a.pluginid) as total,
b.vulname
from
    sep21 a,
	plugin b
where
	a.riskid = 0
	and b.pluginid > 99588
    and a.pluginid = b.pluginid
group by
	a.pluginid
