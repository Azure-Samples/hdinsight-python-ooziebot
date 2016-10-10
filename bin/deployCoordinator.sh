#Check Usage Syntax
if [ $# -lt 3 ]; then
    echo "Usage: source deployCoordinator <FREQUENCY> <WORKFLOW_TYPE> <WASB_PATH> <SOURCE_FILE> [<SPARK_JAR>]"
    echo "EXAMPLE: source deployCoordinator hive sample ../examples/hiveSample.hql"
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