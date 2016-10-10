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

global wasbPath, shellScriptName, userNameArg

if (numArgs > 1):
    wasbPath = str(sys.argv[1])
    shellScriptName = str(sys.argv[2])

else:
    wasbPath = "WASB_PATH"
    shellScriptName = "SHELL_SCRIPT_NAME"

configuration = ""
configuration += addProperty("nameNode", getNameNode())
configuration += addProperty("jobTracker", getJobTracker())
configuration += addProperty("queueName", "default")
configuration += addProperty("oozie.use.system.libpath", "true")
configuration += addProperty("oozie.wf.application.path", getWfPath(wasbPath))
configuration += addProperty("EXEC", shellScriptName)

#Write Xml to file
directory = "../target/shellScriptSample"
if not os.path.exists(directory):
    os.makedirs(directory)
jobFileName = directory + "/" + "job.properties"
jobFile = open(jobFileName, "w")
jobFile.write(configuration)
jobFile.close()

#Debug Print
#print configuration
