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


def BgascheduleAdd():
    Failflag = False
    tolog("Verify BgascheduleAdd info by api")
    body={"bga_type":"rc","status":0,"start_time":60,"recurrence_type":1,"day_start":1,"month_start":1,
          "year_start":2017,"day_end":31,"month_end":12,"year_end":2019,"range_end":1,
          "recurrence_count":100,"interval":10}

    # bgascheduleres=server.webapi("post","bgaschedule",body)
    # bgascheduleview = json.loads(bgascheduleres["text"])
    #
    # for bgaschedule in bgascheduleview:
    #     if bgaschedule:
    #
    #         tolog(str(bgaschedule))
    #         Failflag=Bgascheduleinfo()
    #     else:
    #         Failflag=True

    if Failflag:
        tolog(Fail)
    else:
        tolog(Pass)

def Bgascheduleinfo():
    Failflag = False
    tolog("Verify Bgaschedule list info by api")
    bgascheduleres=server.webapi("get","bgaschedule")
    bgascheduleview = json.loads(bgascheduleres["text"])
    for bgaschedule in bgascheduleview:

        tolog(str(bgaschedule))

    return Failflag
