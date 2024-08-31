CREATE TABLE scorecard (
  scorecardid int NOT NULL AUTO_INCREMENT,
  pluginid varchar(8) NOT NULL,
  host varchar(32) NOT NULL,
  riskid int NOT NULL,
  dtkey varchar(8) NOT NULL,
  rptdate date NOT NULL,
  cve text,
  cvss text,
  protocol varchar(6) DEFAULT NULL,
  port int DEFAULT NULL,
  name text,
  synopsis text,
  description text,
  solution text,
  see_also text,
  plugin_output text,
  hash varchar(32) NOT NULL,
  PRIMARY KEY (scorecardid),
  KEY indx_riskid (riskid),
  KEY indx_dtkey (dtkey),
  KEY indx_hash (hash),
  KEY indx_dtkey_rid (dtkey,riskid)
) 

CREATE TABLE assetinv (
hostname varchar(32) NOT NULL DEFAULT '',
ip varchar(15) NOT NULL DEFAULT '')