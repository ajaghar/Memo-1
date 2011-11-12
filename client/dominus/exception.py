class DominusException(Exception):
    
    def __init__(self, message):
        super(DominusException, self).__init__(self, message)


class DominusServerError(DominusException):
    
    def __init__(self, args):
        self.args = args
        message = "Server raised an error, don't know what to do"
        super(DominusException, self).__init__(self, message)


class DominusBadResponse(DominusException):
    
    def __init__(self, payload):
        self.payload = payload
        super(DominusException, self).__init__(self)
    