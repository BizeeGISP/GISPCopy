import ConfigParser
config = ConfigParser.RawConfigParser()
config.read('ConfigFile.properties')


def getProperties(section, variable):
    value = config.get(section, variable)
    return value