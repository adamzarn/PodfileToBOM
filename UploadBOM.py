import PodspecKeys
import Podspec
import Pod
import ParsingHelpers
import re
import urllib2
import sys

pods = []
with file(sys.argv[1]) as podfile:
    print("\nParsing Podfile...")
    podfileLines = podfile.readlines()
    for line in podfileLines:
        pattern = '.*pod.*:git.*:tag.*'
        match = re.search(pattern, line)
        if match is None:
            continue
        podText = match.group().strip()
        pod = Pod.Pod(podText)
        pods.append(pod)

print("\nFound " + str(len(pods)) + " pod(s)\n")

def getSpecs(pods):

    for pod in pods:

        # Download .podspec file
        podspecFile = urllib2.urlopen(pod.podspecUrl)

        # Split .podspec file into lines
        podspecs = podspecFile.readlines()

        dict = {}

        def handleLicense(i, podspecs):
            licenseString = podspecs[i]
            j = 1
            while podspecs[i + j] and 's.' not in podspecs[i + j]:
                licenseString += podspecs[i + j]
                j += 1
            pattern = PodspecKeys.Keys.licenseType + ' => .*,'
            match = re.search(pattern, licenseString).group()
            license = ParsingHelpers.getArray(match, '=>')[1][:-1]
            dict[PodspecKeys.Keys.license] = license

        for i, spec in enumerate(podspecs):

            array = ParsingHelpers.getArray(spec, "=")
            if len(array) > 1:
                key = array[0]
                value = array[1]

            # Handle License when it's represented as a dictionary
            if key == PodspecKeys.Keys.license and value[0] == '{':
                handleLicense(i, podspecs)

            # Handle simple case of {string: string}
            else:
                dict[array[0]] = array[1]

        podspec = Podspec.Podspec(ParsingHelpers.val(PodspecKeys.Keys.name, dict),
                                  ParsingHelpers.val(PodspecKeys.Keys.version, dict),
                                  ParsingHelpers.val(PodspecKeys.Keys.license, dict),
                                  ParsingHelpers.val(PodspecKeys.Keys.summary, dict),
                                  ParsingHelpers.val(PodspecKeys.Keys.homepage, dict),
                                  ParsingHelpers.val(PodspecKeys.Keys.authors, dict),
                                  ParsingHelpers.val(PodspecKeys.Keys.source, dict),
                                  ParsingHelpers.val(PodspecKeys.Keys.iosDeploymentTarget, dict))

        print(podspec.description + '\n')


getSpecs(pods)
