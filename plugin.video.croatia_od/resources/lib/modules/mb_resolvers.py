import json
import xbmcaddon


def resolve(params):

    type = params["type"]
    exec "from resolvers import " + type
    
    data = params["data"]
    #try:
    resolved_url = eval(type + ".parse_" + type + "(data)")
    return resolved_url
    #except:
    #    return ""