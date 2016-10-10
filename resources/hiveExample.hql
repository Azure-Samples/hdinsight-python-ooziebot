DROP TABLE mysampletable;
CREATE EXTERNAL TABLE mysampletable (deviceplatform string, count string) ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t' STORED AS TEXTFILE LOCATION 'wasb:///sample/data/';
INSERT OVERWRITE TABLE mysampletable SELECT deviceplatform, COUNT(*) as count FROM hivesampletable GROUP BY deviceplatform;
