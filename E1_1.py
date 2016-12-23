import MDB
import BizeeCons
import configUtilities
import pika

class PushData2RMQ:
    mdb = None
    Q_server = configUtilities.getProperties('QUEUE-RMQ', 'Q.server')
    rmq_connection = None
    rmq_channel = None
    rmq_queue = 'RMQ1'


    def __init__(self):
        self.mdb = MDB.MdbClient("GISP")

        self.Get_Publish_URLs("F_URLs")
        self.Get_Publish_URLs("C_URLs")
        self.Get_Publish_URLs("H_URLs")

        self.mdb.close()

    def Get_Publish_URLs(self, collection):
        try:
            self.mdb.Collection(collection)
            cursor = self.mdb.find({ "eps": BizeeCons.CONS_EPS_NEW})
            try:
                iCtr = 0
                #self.getRMQ_Channel()
                for doc in cursor:
                    iCtr += 1
                    url = doc['url']
                    _id = self.mdm.ObjectId_toString(doc['_id'])

                    message = url + ","+ str(_id)
                    print(message)
                    #self.publish_queue(message)
                #self.close_RMQ()
            except Exception as e:
                print( "Error while connecting RMQ Server: ", e)
        except Exception as e:
            print("Error while quaring Database: ", e)

    def getRMQ_Channel(self):
        self.rmq_connection = pika.BlockingConnection(pika.ConnectionParameters(self.Q_server))
        self.rmq_channel    = self.rmq_connection.channel()
        self.rmq_channel.queue_declare(queue=self.rmq_queue, durable=True)

    def close_RMQ(self):
        self.rmq_connection.close()

    def publish_queue(self, message):
        self.rmq_channel.basic_publish(exchange='', routing_key=self.rmq_queue, body=message, properties=pika.BasicProperties(delivery_mode = 2,))



PushData2RMQ()