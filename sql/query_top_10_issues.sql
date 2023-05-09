set @ dtk = '0423A';
set @ rid = 0;
set @ pid = 22024;

select
	solution,
    description 
from
	scorecard
where
	dtkey = @dtk
	and riskid = @rid
	and pluginid = @pid

 