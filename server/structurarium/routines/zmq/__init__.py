import core as zmq
zmq.Context = zmq._Context
zmq.Socket = zmq._Socket

def monkey_patch():
    """
    Monkey patches `zmq.Context` and `zmq.Socket`
    """
    ozmq = __import__('zmq')
    ozmq.Socket = zmq.Socket
    ozmq.Context = zmq.Context
