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
from Userapi import Useradd,extUsergetinfo


def Passwordset():
    Failflag=False

    tolog("Get Password set info by api")
    Useradd()
    Failflag,userinfo=extUsergetinfo()
    for user in userinfo:
        if "testabc" in user['id']:
            userid=user["id"]
            urlpara=str(userid)
            bodypara={"new_passwd":"abcd"}

            res = server.webapiurlbody("put", "password",urlparameter=urlpara,body=bodypara)
            tolog(str(res["response"]))
            #view = json.loads(res["text"])
            if "200" in str(res["response"]):
                tolog("Get password set  is succesfully.")

                #tolog(str(view))
            else:
                Failflag = True
                tolog("Get password set  info failed.")


    if Failflag:
        tolog(Fail)
    else:
        tolog(Pass)
