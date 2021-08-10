select 
	a.pluginid,
    a.riskid,
    total,
    pct,
    b.vulname
from 
	carddata a, plugin b
where 
	a.pluginid = b.pluginid
    and a.dtkey = '0721'
order by 
    a.riskid, total desc