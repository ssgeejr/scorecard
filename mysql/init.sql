SET GLOBAL time_zone = 'America/Chicago';

USE scorecard;

CREATE TABLE rawdata (
       	pluginid varchar(8) NOT NULL,
	host varchar(32) NOT NULL,
	riskid int NOT NULL,
	rptdate DATE NOT NULL
);

CREATE TABLE plugin (
       	pluginid varchar(8) NOT NULL,
	vulname varchar(64) NOT NULL,
	risk varchar(12) NOT NULL,
	riskid int NOT NULL,
	PRIMARY KEY (pluginid)
);

CREATE TABLE risk(
	riskid int NOT NULL,
	risk VARCHAR(12) NOT NULL,
	PRIMARY KEY (riskid)
);

insert into risk (riskid,risk) values
	(0,'Critical'),
	(1,'High'),
	(2,'Medium'),
	(3,'Low'),
	(-1,'None'),
	(-99,'Undefined');

