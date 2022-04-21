CREATE INDEX indx_riskid
ON scorecard (riskid);

CREATE INDEX indx_dtkey
ON scorecard (dtkey);

CREATE INDEX indx_hash
ON scorecard (hash);

CREATE INDEX indx_dtkey_rid
ON scorecard (dtkey,riskid);