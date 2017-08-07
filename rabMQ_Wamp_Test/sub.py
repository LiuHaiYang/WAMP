from twisted.internet.defer import inlineCallbacks
from twisted.logger import Logger

from autobahn.twisted.util import sleep
from autobahn.twisted.wamp import ApplicationSession,ApplicationRunner
from autobahn.wamp.exception import ApplicationError
from os import environ

class AppSession(ApplicationSession):
    log = Logger()
    @inlineCallbacks
    def onJoin(self, details):
        def onhello(msg):
            self.log.info("event for 'onhello' received: {msg}", msg=msg)
        yield self.subscribe(onhello, 'result')
        self.log.info("subscribed to topic 'result'")

if __name__ == '__main__':
    runner = ApplicationRunner(
        environ.get("AUTOBAHN_DEMO_ROUTER", u"ws://172.16.100.188:8080/ws"),
        u"realm1",
    )
    runner.run(AppSession)