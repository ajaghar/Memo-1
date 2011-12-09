class RexException(Exception):
    pass

class RexServerError(RexException):

    def __init__(self, args):
        self.args = args
        message = "Server raised an error, don't know what to do. "
        message += 'Message was %s' % ' '.join(args)
        super(RexException, self).__init__(self, message)


class RexBadResponse(RexException):

    def __init__(self, payload):
        self.payload = payload
        super(RexException, self).__init__(self)
