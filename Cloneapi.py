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


def Clonegetinfo():
    Failflag=False

    tolog("Get Clone info by api")


    res = server.webapiurlbody("get", "clone")
    tolog(str(res["response"]))
    view = json.loads(res["text"])
    if "200" in str(res["response"]):
        tolog("Get clone info is succesfully.")

        tolog(str(view))
    else:
        Failflag = True
        tolog("Get clone info failed.")


    if Failflag:
        tolog(Fail)
    else:
        tolog(Pass)
