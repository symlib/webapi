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


def Controllerinfo():
    ctrlinfolist=list()
    for i in [1,2]:

        res=server.webapiurl("get","ctrl",str(i))
        view = json.loads(res["text"])
        ctrlinfolist.append(view)

    return ctrlinfolist

def ControllerSetting():
    ctrlsettinglist = list()
    for i in [1, 2]:
        res = server.webapiurl("get", "ctrl", str(i)+"/setting")
        view = json.loads(res["text"])
        ctrlsettinglist.append(view)

    return ctrlsettinglist

def SetControllerSetting():
    Failflag = False
    ctrlinfo=Controllerinfo()
    print ctrlinfo
    for ctrl in ctrlinfo:

        aliasname=ctrl[0]["alias"]
        tolog("Old alias is %s" %aliasname.decode().encode('utf-8'))
        ctrlid=ctrl[0]["id"]
        urlpara=str(ctrlid)+"/setting"
        newname=random_key(10)
        body={"alias":newname}
        res=server.webapiurlbody("put", "ctrl", urlpara,body)
        tolog(str(res["response"]))
        ctrlinfo=Controllerinfo()
        for ctrl1 in ctrlinfo:
            if ctrlid==ctrl1[0]["id"]:
                if ctrl1[0]["is_present"]==0:
                    if ctrl1[0]["alias"]!=newname:
                        # Failflag=True
                        # tolog("Change ctrlid %s alias failed" %ctrlid)
                        # break
                        pass
                    else:
                        Failflag = True
                        # tolog("Change ctrlid %s alias successfully." %ctrlid)
                else:
                    if ctrl1[0]["alias"]!=newname:
                        Failflag=True
                        tolog("Change ctrlid %s alias failed" %ctrlid)
                        break
                    else:

                        tolog("Change ctrlid %s alias successfully." %ctrlid)


    if Failflag:
        tolog(Fail)
    else:
        tolog(Pass)