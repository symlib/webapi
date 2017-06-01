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


def Smartgetinfo():
    Failflag=False

    tolog("Get smart by api")
    urlpara="1"
    res = server.webapiurlbody("get", "smart",urlparameter=urlpara)
    tolog(str(res["response"]))
    view = json.loads(res["text"])
    
    if "200" in str(res["response"]):
        tolog("Get smart is succesfully.")

        tolog(str(view))
    else:
        Failflag = True
        tolog("Get smart info failed.")


    if Failflag:
        tolog(Fail)
    else:
        tolog(Pass)
