import PodspecKeys

class Podspec:

    def __init__(self, json):

        if PodspecKeys.Keys.name in json and PodspecKeys.Keys.version in json:
            self.dependency = 'package' + ':' + json[PodspecKeys.Keys.name] + ':' + json[PodspecKeys.Keys.version]
            self.name = json[PodspecKeys.Keys.name]
        else:
            self.dependency = ''
            self.name = ''

        if PodspecKeys.Keys.license in json:
            license = json[PodspecKeys.Keys.license]
            if isinstance(license, dict):
                self.licenses = [license[PodspecKeys.Keys.licenseType]]
            else:
                self.licenses = [license]
        else:
            self.licenses = []

        if PodspecKeys.Keys.homepage in json:
            self.url = json[PodspecKeys.Keys.homepage]
        else:
            self.url = ''

        if PodspecKeys.Keys.authors in json:
            if isinstance(json[PodspecKeys.Keys.authors], dict):
                self.developers = list(json[PodspecKeys.Keys.authors].keys())
            else:
                self.developers = json[PodspecKeys.Keys.authors]
        else:
            self.developers = []

    @property
    def description(self):
        developersString = self.developers
        if isinstance(self.developers, list):
            developersString = ', '.join(self.developers)
        return    '\n' +    'Dependency: ' +    self.dependency \
                + '\n' +    'Name: '       +    self.name \
                + '\n' +    'Licenses: '   +    self.licenses \
                + '\n' +    'Url: '        +    self.url \
                + '\n' +    'Developers: ' +    developersString \
        

    
