
import select
import collections
import time
import types
import functools


class Return(object):

    def __init__(self, value=None):
        self.value = value


reschedule = object()


class Loop(object):

    def __init__(self):
        self.running = True
        self.epoll = select.epoll()
        self.fileno_events = dict()
        self.routines = collections.deque()
        self.inbox = collections.deque()
        self.call_tree = {}

    def register(self, fileno):
        self.epoll.register(fileno)

    def queue(self, routine, to=None):
        self.routines.append((routine, to))

    def routine(self, generator):
        self.queue(generator())
        return generator

    def handle_result(self, routine, result, to=None):
        if result == reschedule:
            self.queue(routine, to)
            return
        if isinstance(result, types.GeneratorType):
            self.queue(result, routine)
            self.call_tree[result] = routine
            return
        if isinstance(result, Return):
            routine.close()
            if to is not None:
                self.inbox.append((to, result.value))
                self.call_tree.pop(routine, None)

    def run1(self):
        events = self.epoll.poll(1)
        for fileno, event in events:
            self.fileno_events[fileno] = event

        if self.routines:
            routine, to = self.routines.popleft()
            try:
                result = routine.next()
            except StopIteration:
                routine.close()
            else:
                self.handle_result(routine, result, to)
            return

        if self.inbox:
            routine, value = self.inbox.popleft()
            try:
                if value == 3:
                    import pdb; pdb.set_trace()
                result = routine.send(value)
            except StopIteration:
                routine.close()
            else:
                caller = self.call_tree.get(routine, None)
                self.handle_result(routine, result, caller)
            return

    def run(self):
        while self.running:
            self.run1()

    def wait_fileno(self, fileno):
        while True:
            event = self.fileno_events.pop(fileno, None)
            if event is not None:
                yield Return(event)
            else:
                yield reschedule


loop = Loop()
