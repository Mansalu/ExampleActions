"""
Python script used by Git Actions automation to apply changes to SLATE instances
described by a Git repository.
"""
import requests
import sys

PathToChangedFiles = sys.argv[1]
slateToken = sys.argv[2]

try:
    ChangedFiles = open(PathToChangedFiles, 'r').read().split('\n')
except Exception as e:
    print("Failed to open temp file", PathToChangedFiles, e)

for FileName in ChangedFiles:
    containerName = FileName.split('/')[0]
    if (containerName == '' or containerName[0] == '.'):
        continue
    instanceDetails = open(containerName + '/' + 'instance.yaml').readlines()
    clusterName = instanceDetails[0].split(':')[1].strip()
    groupName = instanceDetails[1].split(':')[1].strip()
    appName = instanceDetails[2].split(':')[1].strip()
    valuesString = open(containerName + '/' + 'values.yaml').read()
    url = 'https://api.slateci.io:443/v1alpha3/apps/' + appName
    print(url)
    response = requests.post(url, 
                            params={'token' : slateToken}, 
                            data={'apiVersion' : 'v1alpha3',
                                  'group': groupName,
                                  'cluster': clusterName,
                                  'configuration': valuesString})
    print(response, response.text)
