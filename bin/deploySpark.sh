if [ $# != 3 ]; then
    echo "Usage: deploySpark <WASB_PATH> <SPARK_DRIVER_CLASS> <SPARK_JAR>"
    return -1
fi

wasbPath=$1
sparkClass=$2
relativePath=$3
fileName=${relativePath##*/}

hostName=`hostname -f`
urlString="export OOZIE_URL=http://"
ooziePort=":11000/oozie"
oozieExportString=$urlString$hostName$ooziePort
eval $oozieExportString

python ../src/workflows/SparkShellWorkflow.py
python ../src/workflows/SparkShellJob.py $wasbPath $sparkClass $fileName

hdfs dfs -test -d wasb:///$wasbPath
if [ $? == 0 ] ; then
    echo "Directory already exists in wasb"
    return -1
fi

hdfs dfs -mkdir wasb:///$wasbPath
hdfs dfs -mkdir wasb:///$wasbPath/lib
hdfs dfs -put ../target/sparkShellSample/workflow.xml wasb:///$wasbPath
hdfs dfs -put $relativePath wasb:///$wasbPath/lib/.
#oozie job -config ../target/sparkShellSample/job.properties -run
