#!/usr/bin/env python
import argparse, pickle, re, sys, os

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))

from types import MethodType, FunctionType
from random import choice

import zmq

from message import Message
from util import check_if_key_exists


class Structurarium(object):

    def __init__(self, port):
        self.port = port
        self.dict = dict()
        self._structures = []
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.location = 'tcp://*:%s' % port
        self.socket.bind(self.location)

    def start(self):
        print 'Server running on 127.0.0.1:%s' % self.port
        while True:
            message = self.socket.recv()
            message = Message.loads(message)

            # fetch method and call it see :method:`Server._add_structure`
            method = getattr(self, message.action, None)
            if method is not None:
                value = method(*message.args)
                if isinstance(value, list):
                    response = Message('RESPONSE', *value)
                else:
                    response = Message('RESPONSE', value)
            else:
                # it might be a value method
                key = message.args[0]
                if key in self.dict:
                    value = self.dict[key]
                    method = getattr(value, message.action, None)
                    if method is not None:
                        value = method(*message.args[1:])
                        if isinstance(value, list):
                            response = Message('RESPONSE', *value)
                        else:
                            response = Message('RESPONSE', value)
                    else:
                        response = Message('ERROR', 'no such action')
                else:
                    response = Message('ERROR', 'no such action')
            message = response.dumps()
            self.socket.send(message)

    def add_structure(self, structure_class, **kwargs):
        """Adds ``structure_class`` as an available structure in the instance. The 
        structure should at least provide a staticmethod to initialise the key"""
        structure_class.init(self, **kwargs)

        for action_name in dir(structure_class):
            if action_name.isupper():
                function = getattr(structure_class, action_name)
                if isinstance(function, FunctionType):
                    # it's a staticmethod
                    bound_action_method = MethodType(function, self, type(self))
                    setattr(self, action_name, bound_action_method)

    def DEL(self, *args):
        for key in args:
            if key in self.dict:
                del self.dict[key]
        return 'OK'

    def EXISTS(self, key):
        return key in self.dict

    @check_if_key_exists
    def EXPIRE(self, key, seconds):
        value = self.dict[key]
        value.ttl = seconds
        return value.expiration_time 

    @check_if_key_exists
    def EXPIREAT(self, key, timestamp):
        value.expire_at(timestamp)
        return 'OK'

    def KEYS(self, pattern=None):
        if pattern is None:
            return self.dict.keys()
        matched = []
        pattern = re.compile(pattern)
        for key in self.dict.keys():
            match = pattern.match(key)
            if match is not None:
                if key == match.group():
                    matched.append(key)
        return matched

    @check_if_key_exists
    def PERSIST(self, key):
        value = self.dict[key]
        if not value.is_dead:
            value.max_age = None
            return 'OK'

    def RANDOMKEY(self):
        # FIXME the value could be dead...
        keys = self.dict.keys()
        if keys:
            return choice(self.dict.keys())
        else:
            None

    def RENAME(self, key, newkey):
        if key == newkey:
            return None
        if key in self.dict:
            value = self.dict[key]
            if not value.id_dead:
                del self.dict[key]
                self.dict[newkey] = value
                return 'OK'
        return 'KEY DOES NOT EXITS'

    def RENAMENX(self, key, newkey):
        if key == newkey:
            return None
        if key in self.dict:
            if newkey in self.dict:
                newkey_value = self.dict[newkey]
                if not newkey_value.is_dead:
                    return 'NEWKEY ALREADY EXISTS'
            value = self.dict[key]
            if not value.id_dead:
                del self.dict[key]
                self.dict[newkey] = value
                return 'OK'
        return 'KEY DOES NOT EXITS'

    def STRUCTURES(self):
        return self._structures
