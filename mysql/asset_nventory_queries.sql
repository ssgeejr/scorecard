
'' 1291

select
	Count( distinct hostname )
from
	assetinv;

select
	hostname
from
	assetinv;


select
	distinct host
from
	scorecard
where
	dtkey = '0824A'
limit 10;
    
SELECT DISTINCT scorecard.host
FROM scorecard
INNER JOIN assetinv ON scorecard.host = assetinv.ip;
	

select
	Count(*)
from
	scorecard
where
	dtkey = '0824A';



