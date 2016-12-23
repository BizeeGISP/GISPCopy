import MDB
import BizeeCons
import configUtilities
import pika
import time
import datetime

class PushData2RMQ:
    mdb = None
    Q_server = configUtilities.getProperties('QUEUE-RMQ', 'Q.server')
    Q_port   = configUtilities.getProperties('QUEUE-RMQ', 'Q.port')
    Q_user   = configUtilities.getProperties('QUEUE-RMQ', 'Q.user')
    Q_pass   = configUtilities.getProperties('QUEUE-RMQ', 'Q.pass')
    rmq_connection = None
    rmq_channel = None
    iCtr = 0


    def __init__(self):
        startTicks = time.time()
        self.mdb = MDB.MdbClient("GISP")

        self.Get_Publish_URLs(BizeeCons.CONS_FOREIGN_LINK_TABLE)
        self.Get_Publish_URLs(BizeeCons.CONS_CONTACT_LINK_TABLE)
        self.Get_Publish_URLs(BizeeCons.CONS_HOME_LINK_TABLE)

        self.mdb.close()

        print( "Time consumed to publish" + str(self.iCtr) + " message on the queue: " + BizeeCons.CONS_E1_1_QUEUE + " : ", time.time() - startTicks + " seconds...")

    def Get_Publish_URLs(self, collection):
        try:
            self.mdb.Collection( collection + "_URLs")
            cursor = self.mdb.find({ "eps": BizeeCons.CONS_EPS_NEW})
            try:
                startTime = time.time()
                self.iCtr = 0
                ids = []
                self.getRMQ_Channel()
                for doc in cursor:
                    self.iCtr += 1
                    url = doc['url']
                    obj_id = doc['_id']
                    _id = self.mdb.ObjectId(obj_id)
                    ids.append(_id)

                    message = collection + "," + url + ","+ str(_id)
                    if ( self.iCtr % 1000 ) == 0:
                        print("Published: " + str(self.iCtr) + " message in queue: " + BizeeCons.CONS_E1_1_QUEUE + " in " + str(round(time.time()-startTime,2)) + " seconds...")
                    self.publish_queue(message)
                    dateTimeNow = datetime.datetime.now()
                    self.mdb.update_one({"_id" : obj_id}, {'$set': {"eps": BizeeCons.CONS_EPS_MESSAGE_PUSHED_TO_QUEUE, "eps_dt": dateTimeNow}})
                self.close_RMQ()
            except Exception as e:
                print( "Error while connecting RMQ Server: ", e)
        except Exception as e:
            print("Error while quaring Database: ", e)

    def getRMQ_Channel(self):
        credentials = pika.PlainCredentials(self.Q_user, self.Q_pass)
        self.rmq_connection = pika.BlockingConnection(pika.ConnectionParameters(self.Q_server, int(self.Q_port), '/', credentials))
        self.rmq_channel    = self.rmq_connection.channel()
        self.rmq_channel.queue_declare(queue=BizeeCons.CONS_E1_1_QUEUE, durable=True)

    def close_RMQ(self):
        self.rmq_connection.close()

    def publish_queue(self, message):
        self.rmq_channel.basic_publish(exchange='', routing_key=BizeeCons.CONS_E1_1_QUEUE, body=message, properties=pika.BasicProperties(delivery_mode = 2,))



PushData2RMQ()