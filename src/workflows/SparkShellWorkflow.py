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

# create XML
wfname="sparkshellwf"
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
execElem.text="$SPARK_HOME/bin/spark-submit"
shell.append(execElem)

#Adding all arguments needed/optional for Spark-submit here
comment = etree.Comment("Adding all arguments needed/optional for Spark-submit here")
shell.append(comment)

argument=etree.Element('argument')
argument.text= "--class"
argumentValue=etree.Element('argument')
argumentValue.text= "${Spark_Driver}"
shell.append(argument)
shell.append(argumentValue)

argument=etree.Element('argument')
argument.text= "--master"
argumentValue=etree.Element('argument')
argumentValue.text= "${Spark_Master}"
shell.append(argument)
shell.append(argumentValue)

argument=etree.Element('argument')
argument.text= "--deploy-mode"
argumentValue=etree.Element('argument')
argumentValue.text= "${Spark_Mode}"
shell.append(argument)
shell.append(argumentValue)

argument=etree.Element('argument')
argument.text= "--num-executors"
argumentValue=etree.Element('argument')
argumentValue.text= "${numExecutors}"
shell.append(argument)
shell.append(argumentValue)

argument=etree.Element('argument')
argument.text= "--driver-memory"
argumentValue=etree.Element('argument')
argumentValue.text= "${driverMemory}"
shell.append(argument)
shell.append(argumentValue)

argument=etree.Element('argument')
argument.text= "--executor-memory"
argumentValue=etree.Element('argument')
argumentValue.text= "${executorMemory}"
shell.append(argument)
shell.append(argumentValue)

argument=etree.Element('argument')
argument.text= "--executor-cores"
argumentValue=etree.Element('argument')
argumentValue.text= "${executorCores}"
shell.append(argument)
shell.append(argumentValue)

jarName=etree.Element('argument')
jarName.text= "${workflowRoot}/lib/${sparkJar}"
shell.append(jarName)
#End Shell and append it to action
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
directory = "../target/sparkShellSample"
if not os.path.exists(directory):
    os.makedirs(directory)
workFlowFileName=directory+"/"+"workflow.xml"
workflowFile=open(workFlowFileName, "w")
workflowFile.write(workflowString)
workflowFile.close()


# # Enable for debugging
# s = etree.tostring(root, pretty_print=True)
# print s
