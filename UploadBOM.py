import PodspecKeys
import Podspec
import re
import sys
import os
import json
import requests
from urllib import urlencode

directory = '/Users/adamzarn/Documents/iOSProjects/mlab.boschnext-ios'
dirsToIgnore = ['Pods.xcodeproj', '.DS_Store', 'Manifest.lock', 'Local Podspecs', 'Headers', 'Target Support Files']

def getPathOfFolder(folderToFind):
    for subdir, dirs, files in os.walk(directory):
        if folderToFind in dirs:
            return os.path.join(subdir, folderToFind)
    return None

def getSpecs():

    #projectName = raw_input('Project Name: ')
    projectName = 'bosch-next-ios'
    print('Finding Dependencies for ' + projectName + '...\n')

    podspecs = []

    print('Looking for Local Podspecs...')

    localPodspecsDirectory = getPathOfFolder('Local Podspecs')
    if localPodspecsDirectory is None:
        print('Found 0 Local Podspecs')
    else:
        files = os.listdir(localPodspecsDirectory)
        s = '' if len(files) == 1 else 's'
        print('Found ' + str(len(files)) + ' Local Podspec File' + s + '\n')
        for file in files:
            with open(localPodspecsDirectory + '/' + file) as jsonFile:
                data = json.load(jsonFile)
                podspecs.append(Podspec.Podspec(data))

    print('Looking for other pods...')

    localPodspecsCount = len(podspecs)
    podsDirectory = getPathOfFolder('Pods')
    for dir in os.listdir(podsDirectory):
        existingPods = list(map(lambda x: x.dependency.split(':')[1], podspecs))
        if dir not in dirsToIgnore and dir not in existingPods:
            data =  {
                        'name': dir,
                        'version': '1.0'
                    }
            podspecs.append(Podspec.Podspec(data))
    new = len(podspecs) - localPodspecsCount
    s = '' if new == 1 else 's'
    print('Found ' + str(new) + ' more pod' + s + '\n')

    print('Uploading Depndencies...\n')

    dependenciesToUpload = json.dumps([spec.__dict__ for spec in podspecs])
    print(dependenciesToUpload)

    API_ENDPOINT = 'https://androidtools.apps.us2.bosch-iot-cloud.com/bom/v1/basic/' + projectName
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
 
    upload = requests.post(API_ENDPOINT, data=data, headers=headers)
    print(upload.text)

getSpecs()
