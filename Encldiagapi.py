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

from Enclosureapi import ExternalEnclosureinfo
def EnclDiagPSUinfo():
    Failflag=False
    tolog("Get EnclDiagPSUinfo by api")
    Failflag,enclousreinfo=ExternalEnclosureinfo()
    for enc in enclousreinfo:
        print enc["id"]

        tolog("Enclosure %d "%(enc["id"]))

        urlpara=str(enc['id'])+"/psu"

        res = server.webapiurlbody("get", "encldiag", urlparameter=urlpara)
        tolog(str(res["response"]))
        view = json.loads(res["text"])
        if view:
            tolog("Get psu is succesfully.")

            tolog(str(view))
        else:
            Failflag = True
            tolog("Get psu failed.")


    if Failflag:
        tolog(Fail)
    else:
        tolog(Pass)
