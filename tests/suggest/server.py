#!/usr/bin/env python
import argparse

from structurarium.structurarium import Structurarium
from structurarium.structure.suggest import Suggest


server = Structurarium(port=8000, persistent_queue_filename='/tmp/suggest.pq')
server.add_structure(Suggest)
server.start()
