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


def Exportinfo():
    Failflag=False

    tolog("Export Service report by api")
    # type 	1 : db, 2 : event, 3 : servicereport, 4 : config
    urlpara =  "?type=3"

    res = server.webapiurlbody("get", "export",urlparameter=urlpara)
    tolog(str(res["response"]))
    #view = json.loads(res["text"])
    if "200" in str(res["response"]):
        tolog("Export Service report is succesfully.")

    else:
        Failflag = True
        tolog("Export Service report failed.")


    if Failflag:
        tolog(Fail)
    else:
        tolog(Pass)
