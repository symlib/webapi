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


def Ntpgetinfo():
    Failflag=False

    tolog("Get ntp info by api")

    res = server.webapiurlbody("get", "ntp")
    tolog(str(res["response"]))
    view = json.loads(res["text"])
    if "200" in str(res["response"]):
        tolog("Get ntp info is succesfully.")

        tolog(str(view))
    else:
        Failflag = True
        tolog("Get ntp info failed.")


    if Failflag:
        tolog(Fail)
    else:
        tolog(Pass)
