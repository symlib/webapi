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


def Sysloggetinfo():
    Failflag=False

    tolog("Get syslog by api")
    # urlpara="Administrator"
    res = server.webapiurlbody("get", "syslog")
    tolog(str(res["response"]))
    view = json.loads(res["text"])
    
    if "200" in str(res["response"]):
        tolog("Get syslog is succesfully.")

        tolog(str(view))
    else:
        Failflag = True
        tolog("Get syslog info failed.")


    if Failflag:
        tolog(Fail)
    else:
        tolog(Pass)
