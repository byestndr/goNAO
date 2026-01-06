import sys
sys.path.append('../goNAO')

class ConnectionDetails():
    def runFromMain(self, api):
        """ Stop talking """
        end(api)

def end(api):
    """ Connect to the NAO and stop it from talking """
    api.stopTalk()
