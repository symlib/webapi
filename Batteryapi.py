import time
from remote_imporved import server
from pool import random_key

import json
import random
from to_log import tolog
import requests

Pass = "'result': 'p'"
Fail = "'result': 'f'"


def Batteryinfo():
    Failflag = False

    batteryres=server.webapi("get","battery")
    batteryview = json.loads(batteryres["text"])
    for battery in batteryview:
        if battery['id']!="":
            tolog("Verify the battery info by api")
            tolog(str(battery))
            Failflag =Batteryrecondition(battery['id'])
        else:
            Failflag=True

    if Failflag:
        tolog(Fail)
    else:
        tolog(Pass)


def Batteryrecondition(batteryid):
    Failflag = False
    tolog("Verify battery recondition by api")
    urlpara=str(batteryid)
    batteryreconditionres=server.webapiurl("post","batteryrecondition",urlpara)
    if batteryreconditionres["text"]!="":
        Failflag=True
        tolog("Failed on recondiction battery %s,error is %s" %(urlpara ,batteryreconditionres["text"]))

    return Failflag

