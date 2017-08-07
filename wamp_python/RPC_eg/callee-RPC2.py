

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

        
        # REGISTER a procedure for remote calling
        #register
        def add2(args):
            x = args[0]
            y = args[1]
            self.log.info("parameter called with {x} and {y}:" ,x=x, y=y)
            return x + y

        yield self.register(add2, 'RPC2')
        self.log.info("procedure RPC2 registered")
if __name__ == '__main__':
    runner = ApplicationRunner(
        environ.get("AUTOBAHN_DEMO_ROUTER", u"ws://172.16.100.188:8080/ws"),
        u"realm1",
    )
    runner.run(AppSession)
   
