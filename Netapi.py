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


def Netgetinfo():
    Failflag=False

    tolog("Get net info by api")

    res = server.webapiurlbody("get", "net")
    tolog(str(res["response"]))
    view = json.loads(res["text"])
    if "200" in str(res["response"]):
        tolog("Get net info is succesfully.")

        tolog(str(view))
    else:
        Failflag = True
        tolog("Get net info failed.")


    if Failflag:
        tolog(Fail)
    else:
        tolog(Pass)
