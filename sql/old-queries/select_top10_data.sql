select 
    total,
	a.riskid,
    pct,
    a.pluginid,
    b.vulname
from 
	carddata a, plugin b
where 
	a.pluginid = b.pluginid
    and a.dtkey = '0921'
    and a.riskid = 3
    
order by 
    a.riskid, total desc