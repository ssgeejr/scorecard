select
    count(*) as total_new,
    a.pluginid,
    b.vulname
from 
	sep21 a,
    plugin b
where 
	a.pluginid = b.pluginid
    and a.riskid = 2
    and a.pluginid not in
        (
		select 
			pluginid
		from
			plugin
		where 
			riskid = 2
		)
group by
	a.pluginid
order by 
    count(*) desc