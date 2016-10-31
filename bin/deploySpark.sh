# DISCLAIMER: © 2016 Microsoft Corporation. All rights reserved. Sample scripts in this guide are not supported under any
# Microsoft standard support program or service. The sample scripts are provided AS IS without warranty of any kind.
# Microsoft disclaims all implied warranties including, without limitation, any implied warranties of merchantability or
# of fitness for a particular purpose. The entire risk arising out of the use or performance of the sample scripts and
# documentation remains with you. In no event shall Microsoft, its authors, or anyone else involved in the creation,
# production, or delivery of the scripts be liable for any damages whatsoever (including, without limitation, damages
# for loss of business profits, business interruption, loss of business information, or other pecuniary loss) arising
# out of the use of or inability to use the sample scripts or documentation, even if Microsoft has been advised of the
# possibility of such damages.

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
