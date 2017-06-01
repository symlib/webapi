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


def PerfStatsgetinfo():
    Failflag=False

    tolog("Get perfstats info by api")
    server.webapiurlbody("post", "perfstatsstart")
    time.sleep(10)
    res = server.webapiurlbody("get", "perfstats")
    tolog(str(res["response"]))
    view = json.loads(res["text"])
    if "200" in str(res["response"]):
        tolog("Get perfstats info is succesfully.")

        tolog(str(view))
    else:
        Failflag = True
        tolog("Get perfstats info failed.")


    if Failflag:
        tolog(Fail)
    else:
        tolog(Pass)
