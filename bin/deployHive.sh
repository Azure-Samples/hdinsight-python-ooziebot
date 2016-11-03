if [ $# != 2 ] ; then
    echo "Usage: deployHive <WASB_PATH> <HIVE_SCRIPT_NAME>"
    return -1
fi

wasbPath=$1
relativePath=$2
fileName=${relativePath##*/}

hostName=`hostname -f`
urlString="export OOZIE_URL=http://"
ooziePort=":11000/oozie"
oozieExportString=$urlString$hostName$ooziePort
eval $oozieExportString

python ../src/workflows/HiveWorkflow.py
python ../src/workflows/HiveJob.py $wasbPath $fileName

hdfs dfs -test -d wasb:///$wasbPath

if [ $? == 0 ] ; then
    echo "Directory already exists in wasb"
    return -1
fi

hdfs dfs -mkdir wasb:///$wasbPath
hdfs dfs -put ../target/hiveSample/workflow.xml wasb:///$wasbPath
hdfs dfs -put $relativePath wasb:///$wasbPath
#oozie job -config ../target/hiveSample/job.properties -run
