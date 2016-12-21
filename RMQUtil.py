import ConfigParser

config=ConfigParser.RawConfigParser()
config.read('RabbitMQ.properties')

def getRMQProperties(section,variable):
    val=config.get(section,variable)
    return val