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


def Importgetinfo():
    Failflag=False

    tolog("Get import info by api")

    # urlpara = str(enc['id']) + "/psu"

    # res = server.webapiurlbody("get", "import")
    # tolog(str(res["response"]))
    # view = json.loads(res["text"])
    # if view:
    #     tolog("Get import info is succesfully.")
    #
    #     tolog(str(view))
    # else:
    #     Failflag = True
    #     tolog("Get import info failed.")


    if Failflag:
        tolog(Fail)
    else:
        tolog(Pass)
