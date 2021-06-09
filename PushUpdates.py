"""
Python script used by Git Actions automation to apply changes to SLATE instances
described by a Git repository.

Written by Mitchell Steinman

Modified June 8th, 2021
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
    print(Entry, '\n')
    # Parse entry containing file name and change status
    if (Entry == ''):
        continue
    # Status: M = Modified, A = Added, R = Removed
    FileStatus = Entry.split()[0]
    FileName = Entry.split()[1]
    # The "container" is any arbitrary path before the slate details
    # 'values.yaml' and 'instance.yaml'
    containerName = FileName.split('/values.yaml')[0]
    # Skip irrelevant files
    if (containerName.__contains__('.')):
        continue
    if (not FileName.__contains__('values.yaml')):
        if (FileName.__contains__('instance.yaml')):
            print("Not implemented: Version update")
        else:
            continue

    if (FileStatus == 'M'):
        # Update an instance
        print('M')
    elif (FileStatus == 'A'):
        # Create a new instance
        try:
            instanceDetails = open(containerName + '/' + 'instance.yaml', 'r').readlines()
        except Exception as e:
            print("Failed to open instance file for reading:", containerName + '/' + 'instance.yaml' , e)

        instanceConfig = {}
        for line in instanceDetails:
            instanceConfig.update({line.split(': ')[0] : line.split(': ')[1]})

        clusterName = instanceConfig["cluster"]
        groupName = instanceConfig["group"]
        appName = instanceConfig["app"]
        if (instanceConfig.get("appVersion")):
            appVersion = instanceConfig["appVersion"]
        else:
            appVersion = ""

        valuesString = open(containerName + '/' + 'values.yaml', 'r').read()
        url = 'https://api.slateci.io:443/v1alpha3/apps/' + appName
        print(url)
        print(clusterName, groupName, appName)
        response = requests.post(url, 
                                params={'token' : slateToken}, 
                                json={'apiVersion' : 'v1alpha3',
                                    'group': groupName,
                                    'cluster': clusterName,
                                    'configuration': valuesString})
        print(response, response.text)
        if (response.status_code == 200):
            instanceID = response.json()['metadata']['id']
            # Open instance.yaml for writing and writeback instance ID
            try:
                instanceFile = open(containerName + '/' + 'instance.yaml', 'a')
                instanceFile.write('instance: ' + instanceID)
                # Git add commit push
            except Exception as e:
                print("Failed to open instance file for ID writeback:", containerName + '/' + 'instance.yaml' , e)
    elif (FileStatus == 'D'):
        # Remove an instance
        print('D')
    else:
        print('Error: Invalid file status passed by actions')
