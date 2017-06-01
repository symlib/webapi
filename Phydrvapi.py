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


def Phydrvgetinfo():
    Failflag=False

    tolog("Get Phydrv info by api")
    res = server.webapi("get", "phydrv")
    # pdlist = list()
    cleanrestext = json.loads(res["text"])

    # for eachpd in cleanrestext:
    #
    #     if eachpd["op_status"] == "OK" and eachpd["cfg_status"] == "Unconfigured" and eachpd["type"] == "SAS HDD":
    #         pdlist.append(eachpd["id"])
    #
    if "200" not in str(res["response"]):
        Failflag=True
        tolog(str(cleanrestext))

    if Failflag:
        tolog(Fail)
    else:
        tolog(Pass)
