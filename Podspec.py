class Podspec:

  def __init__(self,
               name,
               version,
               license,
               summary,
               homepage,
               authors,
               source,
               iosDeploymentTarget):
    self.name = name
    self.version = version
    self.license = license
    self.summary = summary
    self.homepage = homepage
    self.authors = authors
    self.source = source
    self.iosDeploymentTarget = iosDeploymentTarget

  @property
  def description(self):
    return 'Name: ' + self.name + '\n' \
        + 'Version: ' + self.version + '\n' \
        + 'License: ' + self.license + '\n' \
        + 'Summary: ' + self.summary + '\n' \
        + 'Homepage: ' + self.homepage + '\n' \
        + 'Authors: ' + self.authors + '\n' \
        + 'Source: ' + self.source + '\n' \
        + 'iOS Deployment Target: ' + self.iosDeploymentTarget
