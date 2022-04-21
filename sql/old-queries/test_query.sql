
select
*
from
nov21
where
pluginid = '15901'
and riskid >= 0

select
*
from
plugin
where 
pluginid = '90544'

select
	count(*) as 'total'
from 
	nov21
where
	riskid >= 0
	and 
	pluginid in (
		select
		pluginid
		from
		plugin
		where vulname like '%Office%'
		and pluginid >= 0)




select 
	count(*) as 'total',
    pluginid
from 
	nov21
where 
	riskid = 1
	and
	datakey not in (
		select 
			datakey
		from
			oct21
		where 
			riskid = 1
		)
group by 
	pluginid
order by 
	count(*) desc
    
    