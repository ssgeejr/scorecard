SET @rid = 0;
SET @old = '0922B';
SET @new = '1022B';

select 
	riskid as rid,
	count(distinct hash) as total
from
	scorecard
where
	dtkey = @old
    and riskid = @rid
    and hash not in (
		select
			distinct hash
		from 
			scorecard
		where
			dtkey = @new
            and riskid = @rid
	)
group by 
	rid