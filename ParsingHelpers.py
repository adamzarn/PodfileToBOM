def getArray(line, delimiter):
    items = line.split(delimiter)
    rightJoined = ''.join(items[1:])
    array = [items[0], rightJoined]
    stripped = list(map(lambda x: x.strip(), array))
    return stripped

def val(key, dict):
    if key in dict:
        return dict[key].strip('\'').strip('"')
    else:
        return 'nil'
