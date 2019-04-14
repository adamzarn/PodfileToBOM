def parse(string, delimiter, index):
    return string.split(delimiter)[index].strip().replace('\'', '').replace('\"', '')

class Pod:

    baseUrl = 'https://raw.githubusercontent.com'

    def __init__(self, source):

        array = source.split(',')

        podComponent = parse(array[0], ' ', 1)
        gitComponent = parse(array[1], '>', 1)
        tagComponent = parse(array[2], '>', 1)

        urlComponents = gitComponent.split('/')
        length = len(urlComponents)

        self.name = urlComponents[length - 1].split('.')[0]
        self.user = urlComponents[length - 2]
        self.tag = tagComponent
        self.file = podComponent + ".podspec"

    @property
    def podspecUrl(self):
        return '/'.join([Pod.baseUrl, self.user, self.name, self.tag, self.file])
