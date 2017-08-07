from twisted.internet.defer import inlineCallbacks
from twisted.logger import Logger
from autobahn.twisted.util import sleep
from autobahn.twisted.wamp import ApplicationSession,ApplicationRunner
from autobahn.wamp.exception import ApplicationError
from os import environ
from flask import Flask
from flask_restful import Resource,Api,reqparse
import pymysql

app = Flask(__name__)
api = Api(app)
conn =pymysql.connect(host="127.0.0.1",user="root",passwd="843800695",db="pachong",charset='utf8')

class AppSession(ApplicationSession):

    log = Logger()

    @inlineCallbacks
    def onJoin(self, details):
        # PUBLISH and CALL every second .. forever
        counter = 0
        while True:
            # PUBLISH an event
            #publish
            cur = conn.cursor()
            cur.execute("SELECT * FROM xsbk")
            for i in cur.fetchall():
                yield self.publish('pages', i)
                self.log.info("published to 'result' with counter {i}",
                          i=i)
                print('==========================================================')
                yield sleep(5)

            yield sleep(1)
if __name__ == '__main__':
    runner = ApplicationRunner(
        environ.get("AUTOBAHN_DEMO_ROUTER", u"ws://172.16.100.188:8080/ws"),
        u"realm1",
    )
    runner.run(AppSession)
