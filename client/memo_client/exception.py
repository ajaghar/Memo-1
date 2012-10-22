class MemoException(Exception):
    pass

class MemoServerError(MemoException):

    def __init__(self, args):
        self.args = args
        message = "Server raised an error, don't know what to do. "
        message += 'Message was: %s' % args
        super(MemoException, self).__init__(self, message)
