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


def Discoveryinfo():
    Failflag=False

    urlpara="?usercache=1"

    res = server.webapiurlbody("get", "discovery",urlparameter=urlpara)
    view = json.loads(res["text"])
    if view:
        tolog("Discovery %s succesfully."%view['hosts'])
        tolog(str(view))
    else:
        Failflag=True
        tolog("Discovery failed.")


    if Failflag:
        tolog(Fail)
    else:
        tolog(Pass)
