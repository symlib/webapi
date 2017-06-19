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


def Iscsinodegetinfo():
    Failflag = False
    Faillist = list()

    tolog("Get iscsinode info by api")

    # urlpara = str(enc['id']) + "/psu"

    res = server.webapiurlbody("get", "iscsinode")

    tolog(str(res["response"]))
    view = json.loads(res["text"])
    if "200" in str(res["response"]):
        tolog("Get iscsinode info is succesfully.")

        tolog(str(view))
        for each in view:
            for key,value in each.items():
                if key=="id":
                    # print "value,",value
                    Faillist.append(Iscsinodegetbyidinfo(value))

                    # Iscsisetnode(value)

    else:
        aillist.append(True)
        tolog("Get iscsinode info failed.")

    for flag in Faillist:
        if flag:
            Failflag = True
            break

    if Failflag:
        tolog(Fail)
    else:
        tolog(Pass)

def Iscsinodegetbyidinfo(id):
    Failflag = False

    tolog("Get iscsinode info by id")
    urlpara=str(id)
    res = server.webapiurlbody("get", "iscsinode",urlparameter=urlpara)
    tolog(str(res["response"]))
    view = json.loads(res["text"])
    if "200" in str(res["response"]):
        tolog("Get iscsinode info by id is succesfully.")
        tolog(str(view))
    else:
        Failflag=True

    return Failflag

def Iscsisetnode(id):
    Failflag = False

    tolog("Set iscsinode info by api")
    urlpara = str(id)
    bodypara={"alias":"test","header_digest":1,"data_digest":1,"bi_chap_auth":0,"uni_chap_auth":0,"assn_portal_ids":"1,2"}
    res = server.webapiurlbody("put", "iscsinode", urlparameter=urlpara,body=bodypara)
    Iscsinodegetbyidinfo(id)


def Iscsiportal_add_phyvlan():
    Failflag=False
    Faillist=list()
    tolog("Add portal by api")
    # max portal number 32
    bodypara_phy = {"if_type": "Physical", "tcp_port": 3260, "ip_type": "IPv4", "dhcp": 1, "port_id": 1, "ctrl_id": 2}

    bodypara_vlan = {"if_type": "Vlan", "tcp_port": 3260, "ip_type": "IPv4", "dhcp": 1, "port_id": 2, "ctrl_id": 2,"vlan_tag":1}
    bodypara=(bodypara_phy,bodypara_vlan)
    #bodypara_trunk = {"if_type": "Trunk", "tcp_port": 3260, "ip_type": "IPv4", "dhcp": 1, "trunk_id": 1}
    for i in range(32):
        para=random.choice(bodypara)
        res=server.webapiurlbody("post","iscsiportal",body=para)
        tolog(str(res["response"]))
        #view = json.loads(res["text"])
        if "200" in str(res["response"]):
            tolog("Add portal succesfully.")
            #tolog(str(view))
        else:
            Faillist.append(True)
            tolog("Add portal failed." + str(para))

    for flag in Faillist:
        if flag:
            Failflag=True
            break

    if Failflag:
        tolog(Fail)
    else:
        tolog(Pass)

def Iscsiportal_add_trunk():
    Failflag=False
    Faillist=list()
    tolog("Add portal by api")
    # max portal number 32

    bodypara_trunk = {"if_type": "Trunk", "tcp_port": 3260, "ip_type": "IPv4", "dhcp": 1, "trunk_id": 1}
    for i in range(32):

        res=server.webapiurlbody("post","iscsiportal",body=bodypara_trunk)
        tolog(str(res["response"]))
        #view = json.loads(res["text"])
        if "200" in str(res["response"]):
            tolog("Add portal succesfully.")
            #tolog(str(view))
        else:
            Faillist.append(True)
            tolog("Add portal failed." + str(para))

    for flag in Faillist:
        if flag:
            Failflag=True
            break

    if Failflag:
        tolog(Fail)
    else:
        tolog(Pass)

def Iscsitrunk_create():
    Failflag=False
    tolog("Add iscsitrunk by api")
    bodypara={"ctrl_id":2,"master_port":1,"trunk_type":"balance_xor","slave_ports":[2]}
    res=server.webapiurlbody("post","linkaggr",body=bodypara)
    tolog(str(res["response"]))
        #view = json.loads(res["text"])
    if "200" in str(res["response"]):
        tolog("Add trunk succesfully.")
            #tolog(str(view))
    else:
        Failflag = True
        tolog("Add portal failed." + str(bodypara))

    if Failflag:
        tolog(Fail)
    else:
        tolog(Pass)


def Iscsitrunk_delete():
    Failflag = False
    Faillist = list()
    tolog("Delete iscsitrunk by api")

    res = server.webapiurlbody("get", "linkaggr")
    tolog(str(res["response"]))
    view = json.loads(res["text"])
    if "200" in str(res["response"]):

        for each in view:
            res1=server.webapiurlbody("delete", "linkaggr",urlparameter=str(each["id"]))
            # view = json.loads(res1["text"])
            if "200" in str(res1["response"]):
                tolog("Delete iscsitrunk %d  succesfully." % each["id"])
            else:
                tolog("Delete iscsitrunk %d  failed." % each["id"])
                Failflaglist.append(True)
    else:
        Failflaglist.append(True)
        tolog("Get iscsitrunk info failed." )


    for flag in Faillist:
        if flag:
            Failflag=True
            break

    if Failflag:
        tolog(Fail)
    else:
        tolog(Pass)

def Iscsitrunk_getinfo():
    Failflag = False

    tolog("Get iscsitrunk info by api")
    # bodypara = {"ctrl_id": 2, "master_port": 1, "trunk_type": "balance_xor", "slave_ports": [1]}
    res = server.webapiurlbody("get", "linkaggr")
    tolog(str(res["response"]))
    view = json.loads(res["text"])
    if "200" in str(res["response"]):
        tolog("Get iscsitrunk info succesfully.")
        tolog(str(view))
    else:
        Failflag = True
        tolog("Get iscsitrunk info failed." + str(para))

    if Failflag:
        tolog(Fail)
    else:
        tolog(Pass)

def Iscsiportal_getanddelete():
    Failflag=False
    Failflaglist=list()
    tolog("Get portals info by api")
    res = server.webapiurlbody("get", "iscsiportal")
    tolog(str(res["response"]))
    view = json.loads(res["text"])
    portalnum=len(view)
    if "200" in str(res["response"]):
        tolog("Get portals info succesfully.")
        tolog(str(view))
        # print "type of view is ", type(view)
        for each in view:
            newres = server.webapiurlbody("get", "iscsiportal")
            newview= json.loads(newres["text"])
            num=len(newview)


            if num!=portalnum:
                Failflaglist.append(True)
                tolog("Returned portal number is %d, and it should be %d" % (num, portalnum))
            Failflaglist.append(Iscsiportal_delete(each['id']))
            portalnum-=1
    else:
        Failflaglist.append(True)
        tolog("Delete portal failed.")

    for flag in Failflaglist:
        if flag:
            Failflag=True
            break

    if Failflag:
        tolog(Fail)
    else:
        tolog(Pass)

def Iscsiportal_delete(id):
    Failflag = False
    tolog("Delete portal by api")
    urlpara=str(id)
    res=server.webapiurlbody("delete","iscsiportal",urlparameter=urlpara)
    tolog(str(res["response"]))
    #view = json.loads(res["text"])
    if "200" in str(res["response"]):
        tolog("Delete portal %d succesfully." %id)
        #tolog(str(view))
    else:
        Failflag=True

    return Failflag
# def Iscsiportal_add_Trunk():
#     pass
# def Iscsiportal_add_Vlan():
#     pass


if __name__ == "__main__":

    # Iscsinodegetinfo()

    # Iscsiportal_getanddelete()
    Iscsiportal_add_phyvlan()

    Iscsiportal_getanddelete()
    Iscsitrunk_create()

    Iscsiportal_add_trunk()
    Iscsiportal_getanddelete()
    Iscsitrunk_delete()

