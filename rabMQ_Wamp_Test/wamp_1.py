#wamp
from twisted.internet.defer import inlineCallbacks
from twisted.logger import Logger
from autobahn.twisted.util import sleep
from autobahn.twisted.wamp import ApplicationSession,ApplicationRunner
from autobahn.wamp.exception import ApplicationError
from os import environ
#rabbmq
import pika
username = 'admin'   #指定远程rabbitmq的用户名密码
pwd = 'admin'
user_pwd = pika.PlainCredentials(username, pwd)
connection =pika.BlockingConnection(pika.ConnectionParameters('172.16.100.189' ,credentials=user_pwd))
channel =connection.channel()
channel.queue_declare(queue='hello')

# pub WAMP
class AppSession(ApplicationSession):
    @inlineCallbacks
    def onJoin(self, details):
        print('running')
        while True:
            i = []
            #rabbitMQ pub
            def callback(ch,method,properties,body):
                print("Received %r" %(body,))
                i.append(body)
                channel.stop_consuming()
            channel.basic_consume(callback,
                              queue='hello',
                              no_ack=True)
            channel.start_consuming()

            counter =i
            yield self.publish('result', counter)
            self.log.info("published to 'result' with counter {counter}",
                          counter=counter)
            yield sleep(1)
wampCon = ApplicationRunner(environ.get("AUTOBAHN_DEMO_ROUTER", u"ws://172.16.100.188:8080/ws"),u"realm1",)
wampCon.run(AppSession)

