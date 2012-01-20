#!/usr/bin/env python
import argparse

from structurarium.routines import loop
from structurarium.structurarium import Structurarium
from structurarium.structure.suggest import Suggest


@loop.routine
def main():
    server = Structurarium(8000)
    server.add(Suggest)
    yield server.start()

loop.run()
