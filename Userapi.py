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


def Usergetinfo():
    Failflag=False

    tolog("Get user info by api")

    res = server.webapiurlbody("get", "user")
    tolog(str(res["response"]))
    view = json.loads(res["text"])
    if "200" in str(res["response"]):
        tolog("Get user info is succesfully.")

        tolog(str(view))
    else:
        Failflag = True
        tolog("Get user info failed.")


    if Failflag:
        tolog(Fail)
    else:
        tolog(Pass)

def Useradd():
    Failflag=False

    tolog("Add user by api")
    bodypara={"id":"testabc","email":"1@2.com","status":1,"privilege":"View","passwd":"1234"}
    res = server.webapiurlbody("post", "user",body=bodypara)
    tolog(str(res["response"]))
    #view = json.loads(res["text"])
    if "200" in str(res["response"]):
        tolog("Get user info is succesfully.")

        #tolog(str(view))
    else:
        Failflag = True
        tolog("Get user info failed.")


    if Failflag:
        tolog(Fail)
    else:
        tolog(Pass)

def extUsergetinfo():
    Failflag=False

    tolog("Get user info by api")

    res = server.webapiurlbody("get", "user")
    tolog(str(res["response"]))
    view = json.loads(res["text"])
    if "200" in str(res["response"]):
        tolog("Get user info is succesfully.")

        tolog(str(view))
    else:
        Failflag = True
        tolog("Get user info failed.")


    return Failflag,view

