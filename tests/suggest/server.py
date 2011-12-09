#!/usr/bin/env python
import argparse

from structurarium.structurarium import Structurarium
from structurarium.structure.suggest import Suggest


server = Structurarium(8000)
server.add_structure(Suggest)
server.start()
