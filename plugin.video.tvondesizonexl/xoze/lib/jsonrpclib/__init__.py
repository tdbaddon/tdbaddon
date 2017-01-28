from xoze.lib.jsonrpclib.config import Config
config = Config.instance()
from xoze.lib.jsonrpclib.history import History
history = History.instance()
from xoze.lib.jsonrpclib.jsonrpc import Server, MultiCall, Fault
from xoze.lib.jsonrpclib.jsonrpc import ProtocolError, loads, dumps
