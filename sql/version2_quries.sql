SELECT COUNT(*)
FROM (select distinct pluginid, host
from scorecard
where
riskid = 0
and dtkey = '0422A'
) AS criticalCount

A simpler method would be to use concatenated columns
SELECT COUNT(DISTINCT(CONCAT(DocumentId,DocumentSessionId))) FROM Table;

Method-3 If performance is a factor
Eg: you can add a new column to the table and store
MD5(CONCAT(DocumentId,DocumentSessionId)),
so you can easily count distinct on this new column going forward.

Create an INSERT TRIGGER:
//-----------------------------
CREATE TRIGGER generate_md5 BEFORE INSERT ON scorecard
       FOR EACH ROW SET NEW.hash = MD5(CONCAT(NEW.pluginid, NEW.host));


//-----------------------------
DELIMITER $$

CREATE TRIGGER generate_md5
BEFORE INSERT ON scorecard
FOR EACH ROW
BEGIN
  NEW.hash = MD5(CONCAT(NEW.pluginid, NEW.host))
END $$

DELIMITER ;
//-----------------------------

DELIMITER $$

CREATE TRIGGER generate_md5
BEFORE INSERT ON table1
FOR EACH ROW
BEGIN
  NEW.id = MD5(CONCAT(NEW.field1, NEW.field2))
END $$

DELIMITER ;

