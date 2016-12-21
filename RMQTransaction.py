import pika
import RMQUtil
import time


class RMQTransaction:
    ipAddress =None
    q_name = None
    conn = None
    channel = None
    msgBody = None


    def __init__(self):
        self.setIPAddress()
        self.setQName()
        self.conn = self.getConn(self.ipAddress)
        self.channel = self.getChannel(self.conn)
        self.declQueue(self.channel,self.q_name)
        #self.setMsgBody('Welcome to Bizee Tech.')
        #self.publish(self.channel,self.q_name,self.msgBody)
        #self.consume(self.channel,self.q_name)



    def setIPAddress(self):
        self.ipAddress = RMQUtil.getRMQProperties('RabbitMQ-Section','producer1')  # producer1_IP/name from properties file(here 'localhost')
        return self.ipAddress
    def setQName(self):
        self.q_name = RMQUtil.getRMQProperties('RabbitMQ-Section', 'queue_name')  # Queue name from properties file
    def setMsgBody(self,msgBody):
        self.msgBody=msgBody

    def getConn(self,ipaddr):
        conn = pika.BlockingConnection(pika.ConnectionParameters(ipaddr))
        return conn

    def getChannel(self,conn):
        channel=conn.channel()
        return channel

    def declQueue(self,channel,q_name):
        channel.queue_declare(queue=q_name)


    def sendMsg(self, msgBody):
        self.channel.basic_publish(exchange='',
                              routing_key=self.q_name,
                              body=msgBody)
        print(" [x] Message Sent...")


    def callback(self, ch, method, properties, body):
        time.sleep(2)

        print(" [x] Received %r" % body)

    def consume(self):
        self.channel.basic_consume(self.callback,
                              queue=self.q_name,
                              no_ack=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

    def close(self):
        self.conn.close()





RMQTransaction()