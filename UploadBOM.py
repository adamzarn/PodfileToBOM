import PodspecKeys
import Podspec
import Pod
import ParsingHelpers
import re
import urllib2
import sys

inputFile = 'TestPodfile.txt' if len(sys.argv) == 1 else sys.argv[1]

def createPod(line):
    pattern = '.*pod.*:git.*:tag.*'
    match = re.search(pattern, line)
    if match is None:
        return None
    podText = match.group().strip()
    return Pod.Pod(podText)

def getPrefix(podspecs):
    for spec in podspecs:
        pattern = 'Pod::Spec.new do \|.*\|.*'
        match = re.search(pattern, spec)
        if match is None:
            continue
        else:
            return match.group().rstrip().split('|')[-2] + '.'
    return None

def handleLicense(i, podspecs, dict, prefix):
    licenseString = podspecs[i]
    j = 1
    while podspecs[i + j] and prefix not in podspecs[i + j]:
        licenseString += podspecs[i + j]
        j += 1
    pattern = PodspecKeys.Keys.licenseType + ' => .*,'
    match = re.search(pattern, licenseString).group()
    license = ParsingHelpers.getArray(match, '=>')[1][:-1]
    dict[PodspecKeys.Keys.license] = license

def createPods():
    pods = []
    with file(inputFile) as podfile:
        fileName = inputFile.split('/')[-1]
        print("\nParsing " + fileName + "...")
        podfileLines = podfile.readlines()
        for line in podfileLines:
            pod = createPod(line)
            if pod is not None:
                pods.append(pod)
    text = ' pod' if len(pods) == 1 else ' pods'
    print("\nFound " + str(len(pods)) + text + "\n")
    return pods

def createDictionary(podspecs, prefix):
    dict = {}
    for i, spec in enumerate(podspecs):
        array = ParsingHelpers.getArray(spec, '=')
        if len(array) > 1:
            key = ParsingHelpers.getArray(array[0], '.')[1]
            value = array[1]

            # Handle License when it's represented as a dictionary
            if key == PodspecKeys.Keys.license and value[0] == '{':
                handleLicense(i, podspecs, dict, prefix)

            # Handle simple case of string = string
            else:
                dict[key] = value
    return dict

def getSpecs():

    for pod in createPods():

        # Download .podspec file
        podspecFile = urllib2.urlopen(pod.podspecUrl)

        # Split .podspec file into lines
        podspecs = podspecFile.readlines()

        # Get prefix (usually s, but could be f, spec, etc.)
        prefix = getPrefix(podspecs)
        if prefix is None:
            print('.podspec file is badly formatted')
            continue

        # Create dictionary spec names and values
        dict = createDictionary(podspecs, prefix)

        # Create podspec from dictionary
        podspec = Podspec.Podspec(dict)
        print(podspec.description + '\n')


getSpecs()
