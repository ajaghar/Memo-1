#!/usr/bin/env python
from memo.memo import Memo
from structurarium.structure.suggest import Suggest


server = Memo(address='127.0.0.1', port=8008)
server.add_structure(Suggest)
server.start()
