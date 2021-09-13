select 
	a.*,
    b.vulname
from 
	jul21 a,
    plugin b
where 
	a. riskid = 1
    and a.pluginid = b.pluginid
	and vulname like '%Adobe%'
    and a. pluginid not in
        (
		select 
			pluginid
		from
			jun21
		where 
			riskid = 1
		)