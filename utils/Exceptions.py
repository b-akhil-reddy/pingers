# Custom exception for handling SIGTERM
class SigTermException(Exception):
    pass

# Signal handler function
def handleSigterm(signum, frame):
    raise SigTermException("SIGTERM")