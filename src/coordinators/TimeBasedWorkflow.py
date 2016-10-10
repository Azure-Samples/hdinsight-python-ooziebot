from lxml import etree
import os

wfname="oozieTimeCoordinator"
ooziens="uri:oozie:coordinator:0.1"
successClause="end"
failureClause="fail"

frequencyVar="${frequency}"
startTime="${startTime}"
endTime="${endTime}"
timeZone="${timeZone}"

root = etree.Element('coordinator-app', name=wfname, frequency=frequencyVar, start=startTime, end=endTime, timezone=timeZone, xmlns=ooziens)
controls = etree.Element('controls')
concurrency = etree.Element('concurrency')
concurrency.text = "${concurrency}"
controls.append(concurrency)
root.append(controls)
action = etree.Element('action')
workflow = etree.Element('workflow')
appPath = etree.Element('app-path')
appPath.text="${workflowRoot}"
workflow.append(appPath)
action.append(workflow)
root.append(action)

coordinatorString = etree.tostring(root, pretty_print=True)

#Write workflow to file
directory = "../target/coordinator"
if not os.path.exists(directory):
    os.makedirs(directory)
jobFileName=directory+"/"+"coordinator.xml"
jobFile=open(jobFileName, "w")
jobFile.write(coordinatorString)
jobFile.close()