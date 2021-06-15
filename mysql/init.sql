SET GLOBAL time_zone = 'America/Chicago';

USE scorecard;

CREATE TABLE rawdata (
       	pluginid varchar(8) NOT NULL,
	host varchar(15) NOT NULL,
	rptdate DATE NOT NULL
);
