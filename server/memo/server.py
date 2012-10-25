#!/usr/bin/env python
from random import choice
import re

from types import MethodType
from types import FunctionType

from setproctitle import setproctitle

from util import ServerSocket


class Memo(object):

    def __init__(self, address, port):
        setproctitle('memo')
        self.address = address
        self.port = port
        self.dict = dict()
        self.structures = []

    def play(self, message):
        """Executes the action of the message if possible and return
        a response"""
        #
        # fetch method and call it see :method:`Server._add_structure`
        #
        print message
        method = getattr(self, message[0], None)
        if method is not None:
            # it's a main dict method method aka. server method
            value = method(*message[1])
            response = ('RESPONSE', value)
        else:
            # it might be a value method
            try:
                key = message[1][0]
            except IndexError:
                response = ('ERROR', 'no such command')
            else:
                if key in self.dict:
                    value = self.dict[key]
                    method = getattr(value, message[0], None)
                    if method is not None:
                        value = method(*message[1][1:])
                        response = ('RESPONSE', value)
                    else:
                        response = ('ERROR', 'no such command')
                else:
                    response = ('ERROR', 'no such command')
        return response

    def start(self):
        sock = ServerSocket(
            self.address,
            self.port,
        )
        while True:
            message = sock.recv()
            response = self.play(message)
            sock.send(response)

    def add_structure(self, structure_class, **kwargs):
        """Adds ``structure_class`` as an available structure in the
        instance. The structure should provide a staticmethod to
        initialise the key"""
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
        return key in self.dict and self[key].is_dead

    def KEYS(self, pattern=None):
        # FIXME: the values could be dead
        if pattern is None:
            keys = list()
            for key in self.dict.keys():
                if not self.dict[key].is_dead:
                    keys.append(key)
            return key
        else:
            matched = []
            pattern = re.compile(pattern)
            for key in self.dict.keys():
                if self.dict[key].is_dead:
                    continue
                match = pattern.match(key)
                if match is not None:
                    if key == match.group():
                        matched.append(key)
            return matched

    def RANDOMKEY(self):
        keys = self.dict.keys()
        if keys:
            while True:
                key = choice(self.dict.keys())
                if not self.dict[key].is_dead:
                    return key
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
        if key in self.dict and not self.dict[key].is_dead:
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
