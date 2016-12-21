import configparser
config = configparser.RawConfigParser()
config.read('ConfigFile.properties')


def getProperties(section, variable):
    value = config.get(section, variable)
    return value