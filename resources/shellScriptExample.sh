date
hdfs dfs -mkdir wasb:///newsample
hdfs dfs -ls wasb:////
hadoop fs -du wasb:///
hadoop distcp wasb:///example/data/fruits.txt wasb:///newsample/.
