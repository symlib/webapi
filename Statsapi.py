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


def StatsCtrlgetinfo():
    Failflag=False

    tolog("Get stats by api")
    # urlpara="ctrl/2"
    res = server.webapiurlbody("get", "statsctrl")
    tolog(str(res["response"]))
    view = json.loads(res["text"])
    
    if "200" in str(res["response"]):
        tolog("Get stats is succesfully.")

        tolog(str(view))
    else:
        Failflag = True
        tolog("Get stats info failed.")


    if Failflag:
        tolog(Fail)
    else:
        tolog(Pass)
