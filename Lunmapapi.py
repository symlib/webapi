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


def Lunmapgetinfo():
    Failflag=False

    tolog("Get Lunmap info by api")

    # urlpara = str(enc['id']) + "/psu"

    res = server.webapiurlbody("get", "lunmap")
    tolog(str(res["response"]))
    view = json.loads(res["text"])
    if "200" in str(res["response"]):
        tolog("Get lunmap info is succesfully.")

        tolog(str(view))
    else:
        Failflag = True
        tolog("Get lunmap info failed.")


    if Failflag:
        tolog(Fail)
    else:
        tolog(Pass)
