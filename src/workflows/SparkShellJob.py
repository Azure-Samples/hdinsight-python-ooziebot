# DISCLAIMER: © 2016 Microsoft Corporation. All rights reserved. Sample scripts in this guide are not supported under any
# Microsoft standard support program or service. The sample scripts are provided AS IS without warranty of any kind.
# Microsoft disclaims all implied warranties including, without limitation, any implied warranties of merchantability or
# of fitness for a particular purpose. The entire risk arising out of the use or performance of the sample scripts and
# documentation remains with you. In no event shall Microsoft, its authors, or anyone else involved in the creation,
# production, or delivery of the scripts be liable for any damages whatsoever (including, without limitation, damages
# for loss of business profits, business interruption, loss of business information, or other pecuniary loss) arising
# out of the use of or inability to use the sample scripts or documentation, even if Microsoft has been advised of the
# possibility of such damages.

from lxml import etree
import os
import sys


def getNameNode():
    str = os.popen("sed -n '/<name>fs.default/,/<\/value>/p' /etc/hadoop/conf/core-site.xml "
                   "| grep value | cut -f2 -d'>' | cut -f1 -d '<'").read().rstrip('\n')
    if (str):
        return str
    else:
        return "NAMENODE_ADDRESS"


def getJobTracker():
    str = os.popen("hostname -f").read().rstrip('\n')
    if (str):
        return str + ':8050'
    else:
        return "JOBTRACKER_ADDRESS"


def getWfPath(wasbPath):
    nameNodePath = getNameNode();
    wfPath = nameNodePath + "/" + wasbPath
    return wfPath


def addProperty(name, value):
    result = name + "=" + value + "\n";
    return result


numArgs = len(sys.argv)

global wasbPath, sparkClassName, sparkJar

if (numArgs > 1):
    wasbPath = str(sys.argv[1])
    sparkClassName = str(sys.argv[2])
    sparkJar = str(sys.argv[3])

else:
    wasbPath = "WASB_PATH"
    sparkClassName = "CLASS_NAME"
    sparkJar = "SPARK_JAR_FILE"

# Static definitions to ease deployment
numExecutors = "2"
driverMemory = "4G"
executorMemory = "2G"
executorCores = "2"

configuration = ""
configuration += addProperty("nameNode", getNameNode())
configuration += addProperty("jobTracker", getJobTracker())
configuration += addProperty("queueName", "default")
configuration += addProperty("oozie.use.system.libpath", "true")
configuration += addProperty("Spark_Master", "yarn")
configuration += addProperty("Spark_Mode", "cluster")
configuration += addProperty("Spark_Driver", sparkClassName)
configuration += addProperty("numExecutors", numExecutors)
configuration += addProperty("driverMemory", driverMemory)
configuration += addProperty("executorMemory", executorMemory)
configuration += addProperty("executorCores", executorCores)
configuration += addProperty("workflowRoot", getWfPath(wasbPath))
configuration += addProperty("oozie.wf.application.path", getWfPath(wasbPath))
configuration += addProperty("sparkJar", sparkJar)

# Write Xml to file
directory = "../target/sparkShellSample"
if not os.path.exists(directory):
    os.makedirs(directory)
jobFileName = directory + "/" + "job.properties"
jobFile = open(jobFileName, "w")
jobFile.write(configuration)
jobFile.close()

# print(etree.tostring(configuration, encoding='utf-8', xml_declaration=True, pretty_print=True))
