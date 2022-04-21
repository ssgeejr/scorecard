select
	count(*) as 'total',
    a.pluginid as 'plugin',
    b.risk as 'risk',
    b.vulname as 'vulname'
from
	nov21 a,
    plugin b
where
	a.pluginid = b.pluginid
    and a.pluginid >= 0
    and a.pluginid in (
		'103784',
		'121035',
        '112116',
        '15901',
        '42873',
        '51192',
        '62758',
        '59196',
        '137754',
        '65057',
        '90544',
        '104743'
    )
group by 
	a.pluginid, 
    b.risk,
    b.vulname
order by 
	count(*) desc
    