import time
from remote_imporved import server
from pool import random_key
from Poolapi import getusedpd
import json
import random
from to_log import tolog
import requests

Pass = "'result': 'p'"
Fail = "'result': 'f'"


def BBMinfo():
    Failflag = False
    tolog("Verify BBM info by api")
    urlpara=str(random.choice(getusedpd()))
    bbmres=server.webapiurl("get","bbm",urlpara)
    bbmview = json.loads(bbmres["text"])

    for bbm in bbmview:
        if bbm['id']!="":

            tolog(str(bbm))
        else:
            Failflag=True

    if Failflag:
        tolog(Fail)
    else:
        tolog(Pass)



