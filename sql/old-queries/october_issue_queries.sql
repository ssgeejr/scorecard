
select
	a.pluginid as 'PluginID',
	count(a.host) as 'Host Count',
	b.vulname as 'Vulnerability'
from
	sep21 a,
	plugin b
where 
	a.pluginid = b.pluginid
	and a.pluginid in (152100, 153379, 153617,144813,136770,136806,104743,51192,42873,15901)
group by 
    a.pluginid
order by 
	a.pluginid desc



Error Code: 1055. Expression #1 of SELECT list is not in GROUP BY clause and contains 
nonaggregated column 'scorecard.a.pluginid' which is not functionally dependent 
on columns in GROUP BY clause; this is incompatible with sql_mode=only_full_group_by



select
*
from
sep21
where 
pluginid = 153379

select
* 
from
plugin
where
pluginid = 153379

select
    a.host as 'host',
	b.vulname
from
    sep21 a,
	plugin b
where
    and a.pluginid = b.pluginid
    and b.riskid = 0
group by
	a.host