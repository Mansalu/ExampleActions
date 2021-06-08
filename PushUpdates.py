"""
Python script used by Git Actions automation to apply changes to SLATE instances
described by a Git repository.
"""

import re
import requests
import sys

PathToChangedFiles = sys.argv[1]
slateToken = sys.argv[2]

try:
    ChangedFiles = open(PathToChangedFiles, 'r').read().split('\n')
except Exception as e:
    print("Failed to open temp file", PathToChangedFiles, e)

for Entry in ChangedFiles:
    if (Entry == ''):
        continue
    FileStatus = Entry.split()[0]
    if (FileStatus == ''):
        continue
    FileName = Entry.split()[1]
    containerName = FileName.split('/values.yaml')[0]
    if (containerName.__contains__('.')):
        continue
    print(FileName, FileStatus, containerName)
    instanceDetails = open(containerName + '/' + 'instance.yaml').readlines()
    clusterName = instanceDetails[0].split(':')[1]
    groupName = instanceDetails[1].split(':')[1]
    appName = instanceDetails[2].split(':')[1]
    """
    valuesString = open(containerName + '/', 'values.yaml').read()
    response = requests.post('https://api.slateci.io:443/v1alpha3/apps/' + appName, 
                            params={'token' : slateToken}, 
                            body={'apiVersion' : 'v1alpha3',
                                  'group': groupName,
                                  'cluster': clusterName,
                                  'configuration': valuesString})
    print(response)
    if (response.status_code == 200):
        instanceID = response.json()['metadata']['id']
    """
