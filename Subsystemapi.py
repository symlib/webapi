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


def Subsystemgetinfo():
    Failflag=False

    tolog("Get Subsystem by api")
    # urlpara="ctrl/1"
    res = server.webapiurlbody("get", "subsystem")
    tolog(str(res["response"]))
    view = json.loads(res["text"])
    
    if "200" in str(res["response"]):
        tolog("Get subsystem is succesfully.")

        tolog(str(view))
    else:
        Failflag = True
        tolog("Get subsystem info failed.")


    if Failflag:
        tolog(Fail)
    else:
        tolog(Pass)
