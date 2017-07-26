import time
from remote_imporved import server
from pool import random_key

import json
import random
from to_log import tolog
import requests

#import config
import os
import paramiko
import re
import unittest
import pip
import logging
#import vagrant

#from util.parser import OutputStr
from requests.packages.urllib3.exceptions import InsecureRequestWarning

try:
    import requests
except ImportError:
    pip.main(['install', 'requests'])
    import requests

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('crosstest.log')
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

serverip="10.84.2.164"
from requests import Request, Session

def setupsession():
    parameters = {"username": "administrator", "password": "password"}
    s=Session()
    url = "https://" + serverip + "/service/login"
    req=Request("post",url,parameters)

    prepped = s.prepare_request(req)

    return s, prepped

if __name__ == "__main__":

    s, p= setupsession()

import json
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

class Server(object):
    addition_info = None

    def __init__(self):


        parameters = {"username": "administrator", "password": "password"}
        response = self.webapiurlbody("post", "login", body=parameters)
        response_obj = response["response"].json()
        self.addition_info = response_obj[0]

    def webapiurlbody(self, method, service, urlparameter=None,body=None):
        if urlparameter is None:
            url = "https://" + serverip + "/service/" + service

        # elif "?" in urlparameter:
        #     url = "https://" + serverip + "/service/" + service + urlparameter
        else:
            url = "https://" + serverip + "/service/" + service+"/"+urlparameter
        header = dict()
        # print type(body)
        # body=json.dumps(body)
        # print type(body)
        header["Content-Type"] = "application/json"
        header["additioninfo"] = self.addition_info
        returninfo = dict()

        requests_function = getattr(requests, method)
        # header=convert(header)
        response = requests_function(url,json=body,headers=header,verify=False)


        returninfo["request"] = response.request
        returninfo["headers"] = response.headers
        returninfo["url"] = response.url
        returninfo["text"] = response.text
        returninfo["body"]=response._content
        returninfo["parameters"] = urlparameter
        returninfo["response"] = response
        try:
            if response.text != "":
                setattr(response, "data", response.json())
        except:
            raise AssertionError(response.text)

        return returninfo




def getavailpd():
    res = server.webapiurlbody("get", "phydrv")
    pdlist = list()
    cleanrestext = json.loads(res["text"])

    for eachpd in cleanrestext:

        if eachpd["op_status"] == "OK" and eachpd["cfg_status"] == "Unconfigured" and eachpd["type"] == "SAS HDD":
            pdlist.append(eachpd["id"])

    return pdlist


def getusedpd():
    res = server.webapiurlbody("get", "phydrv")
    pdlist = list()
    cleanrestext = json.loads(res["text"])

    for eachpd in cleanrestext:

        if eachpd["op_status"] == "OK" and ("Pool" in eachpd["cfg_status"] or "Spare" in eachpd["cfg_status"]) and \
                        eachpd["type"] == "SAS HDD":
            pdlist.append(eachpd["id"])

    return pdlist


def cleanpool():
    res = server.webapiurlbody("get", "pool")
    poollist = list()
    cleanrestext = json.loads(res["text"])

    for eachpool in cleanrestext:
        urlpara = str(eachpool["id"]) + "?force=1"
        res = server.webapiurlbody("delete", "pool", urlparameter=urlpara)
        print str((res["text"]))


def createobj(obj, setting):
    Failflag = False
    createres = server.webapiurlbody("post", obj, body=setting)

    if createres["text"] != "":
        #tolog("Creating %s with %s failed" % (obj, str(setting)))
        Failflag = True
    #else:
        #tolog("Creating %s with %s successfully" % (obj, str(setting)))

    return Failflag


def deleteobj(obj, objid):
    Failflag = False
    urlpara = str(objid) + "?force=1"
    res = server.webapiurlbody("delete", obj, urlparameter=urlpara)
    if res["text"] != "":
        tolog("Deleting %s %s failed" % (obj, str(objid)))
        Failflag = True
    else:
        tolog("Deleting %s %s successfully" % (obj, str(objid)))

    return Failflag


if __name__ == "__main__":

    server = Server()
    cleanpool()

    poolparameters = {
        "name": "testpool", "pds": [1], "raid_level": "RAID0", "ctrl_id": 1, "stripe": "64kb", "sector": "512b",
        "force_sync": 0}
    createobj("pool",poolparameters)

    volumeparameters = {
        "name": "testvolume", "pool_id": 0, "capacity": "1GB", "block": "512b", "sector": "512b",
        # "compress": compress,
        "sync": "standard", "thin_prov": 1}
    createobj("volume", volumeparameters)
    #
    snapshotparameters = {
        "name": "testsnapshot", "source_id": 0, "type": "volume"}
    createobj("snapshot", snapshotparameters)

    cloneparameters = {
        "name": "testclone", "source_id": 0}
    createobj("clone", cloneparameters)

    #cleanpool()