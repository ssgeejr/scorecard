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
group by a.riskid ```


