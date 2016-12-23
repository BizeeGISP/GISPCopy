import pika
import time
import configUtilities

class RMQ_Client:
    ipAddress =None
    q_name = None
    connection = None
    channel = None
    msgBody = None

    queue_name = None

    Q_server = configUtilities.getProperties('QUEUE-RMQ', 'Q.server')


    def __init__(self, queue_name):
        self.queue_name = queue_name
        self.connection = self.getConnection()
        self.channel    = self.getChannel()
        self.declQueue(self.channel,self.q_name)

    def setMsgBody(self,msgBody):
        self.msgBody=msgBody

    def getConnection(self):
        return pika.BlockingConnection(pika.ConnectionParameters(self.Q_server))

    def getChannel(self):
        return self.connection.channel()

    def queue_declare(self,q_name):
        self.queue_name = q_name
        return self.channel.queue_declare(queue=self.queue_name)


    def basic_publish(self, msgBody):
        return self.channel.basic_publish(exchange='',
                              routing_key=self.queue_name,
                              body=msgBody)


    def callback(self, ch, method, properties, body):
        print(" [x] Received %r" % body)

    def consume(self):
        self.channel.basic_consume(self.callback,
                              queue=self.q_name,
                              no_ack=True)
        self.channel.start_consuming()

    def close(self):
        self.connection.close()





RMQTransaction()