from structurarium.routines import loop
from structurarium.structurarium import Structurarium
from structurarium.structure.suggest import Suggest


@loop.routine
def main():
    structurarium = Structurarium(port=8000)
    structurarium.add(Suggest)
    yield structurarium.start()

loop.run()
