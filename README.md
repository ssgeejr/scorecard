# scorecard
Import Data and Calcuate monthly scorecard

Setup the environment

`pip install mysql-connector-python`

Update Docker to the latest version 

`curl -fsSL https://get.docker.com -o get-docker.sh && ./get-docker.sh`

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

CONFIGURATION 

```#!/bin/bash

UNAME=""

echo "%devops ALL=(ALL) NOPASSWD: LOG_INPUT: ALL"  > /etc/sudoers.d/wmmc-devops
groupadd devops


apt-get update
apt-get install -y apt-transport-https ca-certificates curl gnupg2 software-properties-common python-pip
pip install -U pip
# pip install docker-compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
echo "alias dc='docker-compose'" >> /etc/profile
. /etc/profile
curl -fsSL https://get.docker.com -o get-docker.sh && sh ./get-docker.sh

adduser --disabled-password --gecos "" {$UNAME}
mkdir /home/{$UNAME}/.ssh
cat << EOF > /home/{$UNAME}/.ssh/config
Host *
    StrictHostKeyChecking no
Host github.com
     Hostname github.com
     IdentityFile ~/.ssh/${SSH_GITHUB_KEY}
EOF
cat << EOF >> /home/{$UNAME}/.ssh/authorized_keys
{$USER_PUB_KEY}
EOF
chown -R {$UNAME}.{$UNAME} /home/{$UNAME}/.ssh
chmod 600 /home/{$UNAME}/.ssh/*
chmod 700 /home/{$UNAME}/.ssh

usermod -aG devops {$UNAME}
usermod -aG docker {$UNAME}
```
pvcreate /dev/xvdb 
vgcreate appvg /dev/xvdb
lvcreate --name lv01 -l 100%FREE appvg
mkfs.ext4 /dev/appvg/lv01
mkdir /opt/apps
mount /dev/appvg/lv01 /opt/apps
echo "/dev/appvg/lv01 /opt/apps ext4 defaults 0 0" >> /etc/fstab

chgrp -R devops /opt
chmod -R 775 /opt
