

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

        
        x = 0
        while True:

            
            # CALL a remote procedure
            #call
            try:
                res = yield self.call('RPC1', [x,0])
                self.log.info("the RPC1 result: {result}",
                              result=res)
            except ApplicationError as e:
                # ignore errors due to the frontend not yet having
                # registered the procedure we would like to call
                if e.error != 'RPC1 error:':
                    raise e
            try:        
                res = yield self.call('RPC2', [x, 100])
                self.log.info("the RPC2 result: {result}",
                              result=res)
            except ApplicationError as e:
                # ignore errors due to the frontend not yet having
                # registered the procedure we would like to call
                if e.error != 'RPC2 error:':
                    raise e    
            x += 1        

            yield sleep(1)
if __name__ == '__main__':
    runner = ApplicationRunner(
        environ.get("AUTOBAHN_DEMO_ROUTER", u"ws://172.16.100.188:8080/ws"),
        u"realm1",
    )
    runner.run(AppSession)
