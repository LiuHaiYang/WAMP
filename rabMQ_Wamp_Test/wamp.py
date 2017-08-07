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
        counter = i
        # print('revice', counter)
        yield self.publish('result', counter)
        self.log.info("published to 'result' with counter {counter}",
                      counter=counter)
wampCon = ApplicationRunner(environ.get("AUTOBAHN_DEMO_ROUTER", u"ws://172.16.100.188:8080/ws"),u"realm1",)
# wampCon.run(AppSession)

# sub RabbitMQ
i = []
def callback(ch,method,properties,body):
    print("Received %r" %(body,))
    message = body
    i.append(message)
    # print('send:', i)
    wampCon.run(AppSession)


channel.basic_consume(callback,
                  queue='hello',
                  no_ack=True)
print('running')
channel.start_consuming()
