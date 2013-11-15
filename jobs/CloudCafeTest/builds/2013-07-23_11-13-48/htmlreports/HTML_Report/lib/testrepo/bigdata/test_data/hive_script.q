CREATE TABLE records (year STRING, temperature INT, quality INT) ROW FORMAT DELIMITED FIELDS TERMINATED BY ',';

LOAD DATA LOCAL INPATH 'hive_data.csv' OVERWRITE INTO TABLE records;

SELECT year, MAX( temperature)  FROM records  WHERE temperature != 9999  AND (quality = 0 OR quality = 1 OR quality = 4 OR quality = 5 OR quality = 9)  GROUP BY year;
