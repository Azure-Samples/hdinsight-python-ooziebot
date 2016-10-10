from lxml import etree
import os
import sys

global wasbPath, hiveScriptName

def getNameNode():
    str = os.popen("sed -n '/<name>fs.default/,/<\/value>/p' /etc/hadoop/conf/core-site.xml "
                   "| grep value | cut -f2 -d'>' | cut -f1 -d '<'").read().rstrip('\n')
    if(str):
        return str
    else:
        return "NAMENODE_ADDRESS"

def getJobTracker():
    str = os.popen("hostname -f").read().rstrip('\n')
    if(str):
        return str+':8050'
    else:
        return "JOBTRACKER_ADDRESS"

def getHiveScriptPath( wasbPath, hiveScript ):
    nameNodePath=getNameNode();
    hiveScriptPath=nameNodePath+"/"+wasbPath+"/"+hiveScript
    return hiveScriptPath

def getWfPath( wasbPath ):
    nameNodePath=getNameNode();
    wfPath=nameNodePath+"/"+wasbPath
    return wfPath

def addProperty(name, value):
    result=name+"="+value+"\n";
    return result

numArgs=len(sys.argv)

if(numArgs > 1 ):
    wasbPath=str(sys.argv[1])
    hiveScriptName=str(sys.argv[2])

else:
    wasbPath="WASB_PATH"
    hiveScriptName="HIVE_SCRIPT_NAME"


# configuration = etree.Element('configuration')
configuration=""
configuration+=addProperty("nameNode", getNameNode())
configuration+=addProperty("jobTracker", getJobTracker())
configuration+=addProperty("queueName", "default")
configuration+=addProperty("oozie.use.system.libpath", "true")
configuration+=addProperty("hiveScript", getHiveScriptPath(wasbPath, hiveScriptName))
configuration+=addProperty("oozie.wf.application.path", getWfPath(wasbPath))

# pretty string
#jobString = etree.tostring(configuration, encoding='utf-8', xml_declaration=True, pretty_print=True)

#Write Xml to file
directory = "../target/hiveSample"
if not os.path.exists(directory):
    os.makedirs(directory)
jobFileName=directory+"/"+"job.properties"
jobFile=open(jobFileName, "w")
jobFile.write(configuration)
jobFile.close()

#print(etree.tostring(configuration, encoding='utf-8', xml_declaration=True, pretty_print=True))
#print(configuration)
