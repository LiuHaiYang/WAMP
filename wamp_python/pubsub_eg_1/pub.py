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
        # PUBLISH and CALL every second .. forever
        counter = 0
        while True:
            # PUBLISH an event
            #publish
            #
            yield self.publish('result', counter)
            self.log.info("published to 'result' with counter {counter}",
                          counter=counter)
            counter += 1

            yield sleep(1)
if __name__ == '__main__':
    runner = ApplicationRunner(
        environ.get("AUTOBAHN_DEMO_ROUTER", u"ws://172.16.100.188:8080/ws"),
        u"realm1",
    )
    runner.run(AppSession)