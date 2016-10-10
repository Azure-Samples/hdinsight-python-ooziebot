from lxml import etree
import os

# create XML
wfname="shellscriptwf"
ooziens="uri:oozie:workflow:0.3"
shellns="uri:oozie:shell-action:0.1"
successClause="end"
failureClause="fail"

root = etree.Element('workflow-app', name=wfname, xmlns=ooziens)

# Indicates where the workflow should begin execution
start = etree.Element('start', to=wfname)
root.append(start)

#Creating the action sequence to run the hive script
action = etree.Element('action', name=wfname)

#Creating the hive child inside action.
shell = etree.Element('shell', xmlns=shellns)

#Adding jobtracker to Hive Child
jobTracker=etree.Element('job-tracker')
jobTracker.text="${jobTracker}"
shell.append(jobTracker)

#Adding namenode to Hive Child
namenode=etree.Element('name-node')
namenode.text="${nameNode}"
shell.append(namenode)

#Additional Configurations like queue , memory etc
configuration=etree.Element('configuration')

property=etree.Element('property')

#Additional configuarations can be added inside this property clause.
name=etree.Element('name')
name.text="mapred.job.queue.name"
value=etree.Element('value')
value.text="${queueName}"
property.append(name)
property.append(value)

configuration.append(property)
shell.append(configuration)

#Adding exec element to shell child
execElem=etree.Element('exec')
execElem.text="${EXEC}"
shell.append(execElem)

#Adding associated shell script to be executed
scriptFile=etree.Element('file')
scriptFile.text="${EXEC}#${EXEC}"
comment = etree.Comment("Copy the executable to compute node's current working directory")
shell.append(comment)
shell.append(scriptFile)

#End Hive and append it to action
action.append(shell)

#What to do on success
success = etree.Element('ok', to=successClause)
action.append(success)

#What to do on failure
failure = etree.Element('error', to=failureClause)
action.append(failure)

#End action
root.append(action)

#Printing error message in failure Clause
kill = etree.Element('kill', name=failureClause)
errorMessage=etree.Element('message')
errorMessage.text="Job failed, error message[${wf:errorMessage(wf:lastErrorNode())}] "
kill.append(errorMessage)
root.append(kill)

#Defines the successClause mentioned above. In this case NOOP.
end = etree.Element('end', name=successClause)
root.append(end)

# pretty string
workflowString = etree.tostring(root, pretty_print=True)

#Write Xml to file
directory = "../target/shellScriptSample"
if not os.path.exists(directory):
    os.makedirs(directory)
workFlowFileName=directory+"/"+"workflow.xml"
workflowFile=open(workFlowFileName, "w")
workflowFile.write(workflowString)
workflowFile.close()

# # pretty string
# s = etree.tostring(root, pretty_print=True)
# print s
