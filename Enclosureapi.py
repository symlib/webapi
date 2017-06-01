import time
from remote_imporved import server
from pool import random_key
from Poolapi import getavailpd
import json
import random
from to_log import tolog
import requests

Pass = "'result': 'p'"
Fail = "'result': 'f'"

def ExternalEnclosureinfo():
    Failflag=False

    # urlpara="?usercache=1"

    res = server.webapiurlbody("get", "enclosure")
    tolog(str(res["response"]))
    view = json.loads(res["text"])
    if view:
        tolog("Get enclosure is succesfully.")

        tolog(str(view))
    else:
        Failflag=True
        tolog("Get enclosure failed.")


    return Failflag,view

def Enclosureinfo():
    Failflag=False

    # urlpara="?usercache=1"

    res = server.webapiurlbody("get", "enclosure")
    tolog(str(res["response"]))
    view = json.loads(res["text"])
    if view:
        tolog("Get enclosure is succesfully.")

        tolog(str(view))
    else:
        Failflag=True
        tolog("Get enclosure failed.")


    if Failflag:
        tolog(Fail)
    else:
        tolog(Pass)
