import ParsingHelpers
import PodspecKeys

class Podspec:

  def __init__(self, dict):
    self.name = ParsingHelpers.val(PodspecKeys.Keys.name, dict)
    self.version = ParsingHelpers.val(PodspecKeys.Keys.version, dict)
    self.license = ParsingHelpers.val(PodspecKeys.Keys.license, dict)
    self.summary = ParsingHelpers.val(PodspecKeys.Keys.summary, dict)
    self.homepage = ParsingHelpers.val(PodspecKeys.Keys.homepage, dict)
    self.authors = ParsingHelpers.val(PodspecKeys.Keys.authors, dict)
    self.source = ParsingHelpers.val(PodspecKeys.Keys.source, dict)
    self.iosDeploymentTarget = ParsingHelpers.val(PodspecKeys.Keys.iosDeploymentTarget, dict)

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
