from lxml import etree
import os
import sys
import datetime

global frequency, timeReturned

def addProperty(name, value):
    result=name+"="+value+"\n";
    return result

def getTime(period):
    if period == "start":
        timeReturned = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
        timeReturned = timeReturned.strftime("%Y-%m-%dT%H:%MZ")
    else:
        timeReturned = datetime.datetime.utcnow()+datetime.timedelta(days=1)
        timeReturned = timeReturned.strftime("%Y-%m-%dT%H:%MZ")
    return timeReturned

numArgs=len(sys.argv)

if(numArgs > 1 ):
    frequency = sys.argv[1]
else:
    frequency = 5

configuration = ""
configuration += addProperty("startTime", getTime("start"))
configuration += addProperty("endTime", getTime("end"))
configuration += addProperty("timeZone", "UTC")
configuration += addProperty("concurrency", "1")
configuration += addProperty("frequency", frequency)
configuration += addProperty("workflowRoot", "${oozie.coord.application.path}")

#Write properties to file
directory = "../target/coordinator"
if not os.path.exists(directory):
    os.makedirs(directory)
jobFileName=directory+"/"+"coordinator.properties"
jobFile=open(jobFileName, "w")
jobFile.write(configuration)
jobFile.close()
