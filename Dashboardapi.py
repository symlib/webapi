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


def Dashboardinfo():
    Failflag=False

    urlpara="pool"

    res = server.webapiurlbody("get", "dashboard",urlparameter=urlpara)
    view = json.loads(res["text"])
    if view:
        tolog("Dashboard get pool status succesfully.")
        tolog(str(view))
    else:
        Failflag=True
        tolog("Dashboard get pool status failed.")


    if Failflag:
        tolog(Fail)
    else:
        tolog(Pass)
