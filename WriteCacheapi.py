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


def WriteCacheinfo():

    res=server.webapi("get","wcache")
    view = json.loads(res["text"])



    return view

def WriteCacheAttach():
    Failflag=False
    origsetting=dict()
    tolog("Verify original write cache setting")
    origsetting=WriteCacheinfo()
    if origsetting:
        tolog(str(origsetting))
    else:
        tolog("There's no write cache, and write cache will be added.")
        pdlist=getavailpd()

        body={"pd_list":pdlist}
        urlpara="attach"
        server.webapiurlbody("post","wcache",urlpara,body)

        modifiedsetting=WriteCacheinfo()
        if modifiedsetting:
            tolog(str(modifiedsetting))
        else:
            Failflag
            tolog("Write cache cannot be created.")


    if Failflag:
        tolog(Fail)
    else:
        tolog(Pass)
