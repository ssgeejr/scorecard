SET GLOBAL time_zone = 'America/Chicago';

USE scorecard;

CREATE TABLE rawdata (
       	pluginid varchar(8) NOT NULL,
	host varchar(32) NOT NULL,
	rptdate DATE NOT NULL
);

CREATE TABLE plugin (
       	pluginid varchar(8) NOT NULL,
	vulname varchar(64) NOT NULL,
	risk varchar(12) NOT NULL,
	riskid int,
	PRIMARY KEY (pluginid)
);
