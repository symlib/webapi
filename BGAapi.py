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


def BGAinfo():
    Failflag = False

    bgares=server.webapi("get","bga")
    bgaview = json.loads(bgares["text"])
    bgasetting=dict()
    for bga in bgaview:

        bgasetting["rebuild_rate"]=bga["rebuild_rate"]
        bgasetting["rc_rate"]=bga["rc_rate"]

    return bgasetting

def BGAset():
    Failflag=False
    origsetting=dict()
    origsetting=BGAinfo()
    tolog(str(origsetting))
    body={"rebuild_rate":"Medium","rc_rate":"High"}
    server.webapi("post","bga",body)
    modifiedsetting=BGAinfo()
    tolog(str(modifiedsetting))
    if modifiedsetting["rebuild_rate"]==body["rebuild_rate"] and modifiedsetting["rc_rate"]==body["rc_rate"]:
        tolog("BGA setting updated sucessfully.")
    else:
        tolog("BGA setting updated failed.")
        Failflag=True

    if Failflag:
        tolog(Fail)
    else:
        tolog(Pass)

def extBGAset():
    Failflag=False
    origsetting=dict()
    origsetting=BGAinfo()
    tolog(str(origsetting))
    body={"rebuild_rate":"Medium","rc_rate":"High"}
    server.webapi("post","bga",body)
    modifiedsetting=BGAinfo()
    tolog(str(modifiedsetting))
    if modifiedsetting["rebuild_rate"]==body["rebuild_rate"] and modifiedsetting["rc_rate"]==body["rc_rate"]:
        tolog("BGA setting updated sucessfully.")
    else:
        tolog("BGA setting updated failed.")
        Failflag=True

    return Failflag