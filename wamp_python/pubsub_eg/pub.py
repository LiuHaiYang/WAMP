
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
#conn =pymysql.connect(host="127.0.0.1",user="root",passwd="843800695",db="pachong",charset='utf8')
#cur = conn.cursor()
#app.config['MYSQL_DATABASE_USER'] = 'root'
#app.config['MYSQL_DATABASE_PASSWORD'] = '843800695'
#app.config['MYSQL_DATABASE_DB'] = 'pachone'
#app.config['MYSQL_DATABASE_TABLE'] = 'pages'
#app.config['MYSQL_DATABASE_HOST'] = 'localhost'
#mysql.init_app(app)

#conn = mysql.connect()
#cursor = conn.cursor()
#n = cur.execute("SELECT * FROM pages")
#print(n)

class AppSession(ApplicationSession):

    log = Logger()

    @inlineCallbacks
    def onJoin(self, details):
        # PUBLISH and CALL every second .. forever
        #
        counter = 0
        while True:
            # PUBLISH an event
            #publish
            #
            counter = { "baseTopic": "LTC-base1", "src": "2", "dst": "_1", "seq": "9", "SNR": "-9", "RSSIpkt": "-54", "BW": "125", "CR": "4/5", "SF": "12", "sensor_id": "1", "version": "1", "command_id": "1", "data_length": "4", "data": "Ping", "mote_lon": "114.513122", "mote_lat": "36.577103", "time": "2017-06-24 09:38:19"}
            yield self.publish('pages', counter)
            self.log.info("published to 'result' with counter {counter}",
                          counter=counter)

            yield sleep(1)
if __name__ == '__main__':
    runner = ApplicationRunner(
        environ.get("AUTOBAHN_DEMO_ROUTER", u"ws://www.wugeek.cn:8090/ws"),
        u"realm1",
    )
    runner.run(AppSession)
