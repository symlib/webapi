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


def Buzzerinfo():
    Failflag = False
    tolog("Verify buzzer info by api")


    buzzerres=server.webapi("get","buzzer")
    buzzerview = json.loads(buzzerres["text"])

    for buzzer in buzzerview:
        if buzzer:

            tolog(str(buzzer))
        else:
            Failflag=True

    return buzzer,Failflag

def BuzzerTurnOn():
    Failflag = False
    tolog("Verify buzzer turn on by api")
    body={"onoff":1}

    res=server.webapiurlbody("post","buzzer","status",body)

    buzzer, Failflag = Buzzerinfo()
    if buzzer["status"] == "Sounding":

        tolog("Buzzer turn on sucessfully.")
    else:
        Failflag = True
        tolog("Buzzer turn on failed.")



    if Failflag:
        tolog(Fail)
    else:
        tolog(Pass)
def BuzzerTurnOff():
    Failflag = False
    tolog("Verify buzzer turn off by api")
    body={"onoff":0}
    res=server.webapiurlbody("post","buzzer","status",body)

    buzzer, Failflag = Buzzerinfo()
    if buzzer["status"] == "Silent":

        tolog("Buzzer turn off sucessfully.")
    else:
        Failflag = True
        tolog("Buzzer turn off failed.")



    if Failflag:
        tolog(Fail)
    else:
        tolog(Pass)

def BuzzerEnable():
    Failflag = False
    tolog("Verify buzzer enable by api")
    body={"enable":1}
    res=server.webapi("post","buzzer",body)
    #resview = json.loads(res["text"])
    # if res["text"]:
    #     tolog("Buzzer enable failed.")
    #     Failflag=True

    buzzer, Failflag = Buzzerinfo()
    if buzzer["enabled"] == 1:

        tolog("Buzzer enable sucessfully.")
    else:
        Failflag = True
        tolog("Buzzer enable failed.")

    if Failflag:
        tolog(Fail)
    else:
        tolog(Pass)

def BuzzerDisable():
    Failflag = False
    tolog("Verify buzzer enable by api")
    body={"enable":0}
    res=server.webapi("post","buzzer",body)
    #resview = json.loads(res["text"])

    buzzer, Failflag = Buzzerinfo()
    if buzzer["enabled"] == 0:

        tolog("Buzzer enable sucessfully.")
    else:
        Failflag = True
        tolog("Buzzer enable failed.")

    if Failflag:
        tolog(Fail)
    else:
        tolog(Pass)