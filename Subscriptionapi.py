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


def Subscriptiongetinfo():
    Failflag=False

    tolog("Get Subscription by api")
    bodypara={"name":"administrator"}

    res = server.webapiurlbody("post", "subscription",body=bodypara)
    tolog(str(res["response"]))
    #view = json.loads(res["text"])
    
    if "200" in str(res["response"]):
        tolog("Get subscription is succesfully.")

        #tolog(str(view))
    else:
        Failflag = True
        tolog("Get subscription info failed.")


    if Failflag:
        tolog(Fail)
    else:
        tolog(Pass)
