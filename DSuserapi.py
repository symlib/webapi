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


def DSusergetinfo():
    Failflag=False

    tolog("Get DS user info by api")

    # urlpara="afp"
    # res = server.webapiurlbody("get", "protocol",urlparameter=urlpara)
    # tolog(str(res["response"]))
    # view = json.loads(res["text"])
    # if "200" in str(res["response"]):
    #     tolog("Get Protocol AFP info is succesfully.")
    #
    #     tolog(str(view))
    # else:
    #     Failflag = True
    #     tolog("Get Protocol AFP info failed.")


    if Failflag:
        tolog(Fail)
    else:
        tolog(Pass)
