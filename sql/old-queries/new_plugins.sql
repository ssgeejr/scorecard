select
    count(*) as total_new 
#	a.*,
#    b.vulname
from 
	sep21 a,
    plugin b
where 
	a. riskid = 0
    and a.pluginid = b.pluginid
#	and lower(vulname) like '%Adobe%'
    and a.pluginid not in
        (
		select 
			pluginid
		from
			jul21
		where 
			riskid = 0
		)