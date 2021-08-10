select 
	a.pluginid,
    total,
    pct,
    b.vulname
from 
	scorecard a, plugin b
where 
	a.pluginid = b.pluginid
    and a.dtkey = '0721'
order by 
    riskid