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

import BGAapi
def Factorydefaults():
    Failflag=False

    tolog("Factory defaults restore by api")
    # type 	1 : db, 2 : event, 3 : servicereport, 4 : config
    body =  {"type":"bga"}
    tolog("Check original BGA setting info")
    orires=BGAapi.BGAinfo()
    tolog(str(orires))
    tolog("Restore BGA setting to factory default ")
    res = server.webapiurlbody("post", "factorydefaults",body=body)

    tolog(str(res["response"]))
    tolog("Check default BGA setting info")
    defaultres = BGAapi.BGAinfo()
    tolog(str(defaultres))

    tolog("Check modified BGA setting info")
    Failflag=BGAapi.BGAset()
    modifiedres=BGAapi.BGAinfo()
    tolog(str(modifiedres))



    if Failflag:
        tolog(Fail)
    else:
        tolog(Pass)
