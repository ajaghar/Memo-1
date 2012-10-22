====
Memo
====


Kezako Memo ?
=============

Memo is a free-software, networked, in-memory, key-value store written in python.
Yes it's a Redis clone but scriptable in Python!


- tested with python >= 2.7


Documentation
-------------

Memo has no executable you have to build one yourself using don't panik
it's really easy you have to use the ``memo.Memo`` class and register
the structures you need, here is an example Memo server::

  from memo import Memo
  from memo.structures.suggest import Suggest


  server = Memo(address='127.0.0.1', port=8008)
  server.add_structure(Suggest)
  server.start()

This a server for suggesting spelling correction see the implementation
in ``memo.structures.suggest``.

So how to use it
----------------

Redis before scripting was implemented you were implementing complexe
the data-structures outside of Redis by making calls to the needed COMMANDS.
In Memo you won't do that. Instead you build structures classes that will be the
entry points of your application. The benefit is similar to Redis scripting you
won't need the same number of network round-trip to do the achieve the same,
but this will be done using Python.

Creating a new datastructure is straightforward, see the following example FIFO 
datastructure::

  from memo.structures.base import Base
  from util import check_if_key_exists

  class FIFO(Base):

      def __init__(self, server, key):
          super(Suggest, self).__init__(server, key)
          self.fifo = list()

      @staticmethod
      def FIFOADD(server, key, *values):
          """Add an element in the fifo list create fifo
          if it does not exists"""
          if key in server.dict:
              if server.dict[key].is_dead:
                  server.dict[key] = FIFO(server, key)
              else:
                  if not isinstance(server.dict[key], Suggest):
                      return 'WRONG VALUE'
          else:
              server.dict[key] = FIFO(server, key)
          # the key exists and is not dead
          dict_value = server.dict[key]
          for value in values:
              dict_value.fifo.append(value)
          return 'OK'

      @check_if_key_exists
      def POP(self):
          value = self.fifo[0]
          self.fifo.remove(value)
          return value

This data structure has 2 methods:

- ``FIFOADD`` is a staticmethod which means it's probably will have in charge
  of creating the key value if it does not exists, indeed that's what it does.
  If the requested key doesn't exists or expired, it create a new FIFO and add
  the value. Structures staticmethod must have a unique name among all the 
  structures registred against a Memo server.
- ``POP`` will return the first value of the FIFO if the FIFO did not expire.

This structure can be used in the client like so::

  client.FIFOADD('task queue', 42)
  client.FIFOADD('task queue', 42, 43)
  client.POP('task queue')

The client doesn't discover the available methods, it sends every COMMAND to 
the server and the servers answers a tuple with the first value being 
``RESPONSE`` if the command exists the element of the tuple being the result of
the command, or ``ERROR`` if it doesn't exists. Mind the fact that if you call
a command that exists but the key expired or doesn't exists it will still 
return an ``ERROR``.

A pattern that might come handy are *pure static methods structures* that in 
fact reuse structures registred against the server but this methods are the 
only methods that the client will need to call. This is usefull if you need 
to make use of expiration.

For instance the following data-structure use ``memo.structures.List`` to 
store and retrieve search results for a given search index. Since we are in 
Python we can use any Python library, given a ``search(index, query)`` function that returns 
a list of dictionnary describing search results, a search results cache can be 
implemented using the following class:

  from memo.structures.base import Base
  from util import check_if_key_exists

  class SearchCache(Base):

      @staticmethod
      def SEARCH(server, index, query):
          key = '%s:%s' % (index, query)
          # try to retrieve cached results
          response = server.play(('GET', (key,))
          if response[0] == 'ERROR':
              results = search(index, query)
              server.play(('LSET', results))
              # persist for 15 minutes
              server.play(('EXPIRE', (60*15,)))
              return results
          else:
              return response[1]

Happy hacking!

License
=======

- Memo server: AfferoGPLv3
- Client: LGPLv3

Link
====

- `forge <https://github.com/amirouche/Memo>`_
- `documentation <http://memo.readthedocs.org/>`_

Author
======

`Amirouche Boubekki <amirouche.boubekki@gmail.com>`_
