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


def ReadCacheinfo():

    res=server.webapi("get","rcache")
    view = json.loads(res["text"])



    return view

def ReadCacheAttach():
    Failflag=False
    origsetting=dict()
    tolog("Verify original read cache setting")
    origsetting=ReadCacheinfo()
    tolog(str(origsetting))

    pdlist=getavailpd()


    body={"pd_list":pdlist}
    urlpara="attach"
    server.webapiurlbody("post","rcache",urlpara,body)
    modifiedsetting=ReadCacheinfo()
    tolog(str(modifiedsetting))


    if Failflag:
        tolog(Fail)
    else:
        tolog(Pass)
