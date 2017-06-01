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


def Dateinfo():
    res = server.webapi("get", "date")
    view = json.loads(res["text"])


    return view

import collections

def convert(data):
    if isinstance(data, basestring):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data


def SetDate():


    Failflag = False
    date=Dateinfo()
    # view=dict()
    # view = {'hour': 13, 'min': 56, 'month': 5, 'sec': 52, 'year': 2016, 'day': 18}
    view=date[0].copy()
    view['year']=date[0]['year']-1

    view=convert(view)

    server.webapiurlbody("post", "date",body=view)

    newview = Dateinfo()


    if view['year']!=newview[0]['year']:
        Failflag=True
        tolog("Change year failed")
    else:
        tolog("Change year from %s to %s" %(date[0]['year'],newview[0]['year']))

    if Failflag:
        tolog(Fail)
    else:
        tolog(Pass)
