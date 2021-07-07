# scorecard
Import Data and Calcuate monthly scorecard

Setup the environment

`pip install mysql-connector-python`

PHASE I (Complete)
Extract the file, place it in the corrosponding folder, state the database using docker with the command `docker-compose up -d`

Run the ETL and load the data using the command:  `./dataloader.py`

Connect to the database using MySQL Workbench or using the mysql client inside the docker container `./dbconn`

Once you have connect, you should be able to run the queries you need to extract the data.  Below lists a few of the items you may want to use: 


PHASE II (in progress)
This will include a dockerized version of tomcat which will run the UI 


QUERIES
``` select
b.risk AS 'Risk',
count(*)
from
jun21 a,
risk b
where a.riskid >= 0
and a.riskid = b.riskid
group by a.riskid
```
``` select
	count(*) as 'Total',
	b.risk as 'Risk'
from 
	rawdata a, risk b
where
	a.riskid = b.riskid
group by
	b.riskid
order by
    b.riskid asc
```

``` select
host,
count(*) as 'total'
from
jun21
where
pluginid in(
select
pluginid
from
plugin
where
vulname like '%Adobe Reader%'
and riskid = 0
)
and riskid = 0
group by 
host
```

``` select count(*)
from jun21
where 
riskid = 3
and
datakey not in (
select datakey
from
may21
where 
riskid = 3)
```

``` select
	distinct(host)
from 
	rawdata
where
	riskid = 0
    and host like '%temp%wmmc%'
```

``` select 
a.pluginid, count(*) as cnt,
b.risk as risk, b.vulname as vulnerability
from rawdata a, plugin b 
where 
a.pluginid = b.pluginid 
and b.risk != 'None'
group by 
a.pluginid
order by 
b.riskid, cnt desc 
```


