# DISCLAIMER: © 2016 Microsoft Corporation. All rights reserved. Sample scripts in this guide are not supported under any
# Microsoft standard support program or service. The sample scripts are provided AS IS without warranty of any kind.
# Microsoft disclaims all implied warranties including, without limitation, any implied warranties of merchantability or
# of fitness for a particular purpose. The entire risk arising out of the use or performance of the sample scripts and
# documentation remains with you. In no event shall Microsoft, its authors, or anyone else involved in the creation,
# production, or delivery of the scripts be liable for any damages whatsoever (including, without limitation, damages
# for loss of business profits, business interruption, loss of business information, or other pecuniary loss) arising
# out of the use of or inability to use the sample scripts or documentation, even if Microsoft has been advised of the
# possibility of such damages.

#Check Usage Syntax
if [ $# -lt 3 ]; then
    echo "Usage: source deployCoordinator <FREQUENCY> <WORKFLOW_TYPE> <WASB_PATH> <SOURCE_FILE> [<SPARK_JAR>]"
    echo "EXAMPLE: source deployCoordinator hive sample ../resources/hiveSample.hql"
    return -1
fi

workFlowType=$2

if [ "$workFlowType" == "hive" ]; then
    echo "Working on hive workflows"
    source deployHive.sh $3 $4
    sourceProperties=$(<../target/hiveSample/job.properties)
elif [ "$workFlowType" == "shell" ]; then
    echo "Working on Shell workflows"
    source deployShell.sh $3 $4
    sourceProperties=$(<../target/shellScriptSample/job.properties)
elif [ "$workFlowType" == "spark" ] ; then
    if [ $# -ne 5 ]; then
        echo "Usage: source deployCoordinator <FREQUENCY> spark <WASB_PATH> <SPARK_CLASS> <SPARK_JAR>"
        return -1
    fi
    echo "Working on Spark workflows"
    source deploySpark.sh $3 $4 $5
    sourceProperties=$(<../target/sparkShellSample/job.properties)
else
    echo "Invalid Workflow type"
    return -1
fi

#Build Coordinator and Coordinator specific Properties
echo "Building coordinators"
python ../src/coordinators/TimeBasedWorkflow.py
python ../src/coordinators/TimeBasedJob.py $1

#Replace workflow path with coord path
origString="oozie.wf.application.path"
replaceString="oozie.coord.application.path"

#Merge coordinator properties and workflow properties
echo "${sourceProperties//$origString/$replaceString}" >> ../target/coordinator/coordinator.properties
hdfs dfs -put ../target/coordinator/coordinator.xml wasb:///$3