import time
from remote_imporved import server
from pool import random_key

import json
import random
from to_log import tolog
import requests

Pass = "'result': 'p'"
Fail = "'result': 'f'"

sectormap = {"512b": "512 Bytes", "1kb": "1 KB", "2kb": "2 KB", "4kb": "4 KB"}

def poolcreatewithallsettings():
    Failflag = False
    name = random_key(30)
    stripesettings = ["64kb", "128kb", "256kb", "512kb", "1mb"]
    sectorsettings = ["512b", "1kb", "2kb", "4kb"]
    force_syncsettings = [0, 1]

    stripemap = {"64kb": "64 KB", "128kb": "128 KB", "256kb": "256 KB", "512kb": "512 KB", "1mb": "1 MB"}
    force_syncmap = {0: "Disabled", 1: "Enabled"}
    raidmap = {"RAID0": 0, "RAID1": 1, "RAID5": 5, "RAID6": 6, "RAID10": 10, "RAID50": 50, "RAID60": 60}
    raids = ["RAID0","RAID1","RAID5","RAID6","RAID10","RAID50","RAID60"]
    availpdlist = getavailpd()
    for raidlevel in raids:
        for stripe in stripesettings:
            for sector in sectorsettings:
                for force_sync in force_syncsettings:
                    if raidlevel=="RAID0":
                        availpdlist=random.sample(availpdlist,2)
                    parameters = {
        "name": name, "pds": availpdlist, "raid_level": raidlevel, "ctrl_id": 1, "stripe": stripe, "sector": sector,
        "force_sync": force_sync}
                    #server.webapiurlbody("post","pool",body=parameters)
                    #print parameters
                    createobj("pool",parameters)
                    res=json.loads(viewobj("pool",0))[0]
                    getpdstr=str(res["pds"]).replace("u","")
                    parapdstr=str(parameters["pds"]).replace("[","").replace("]","").replace(" ","")
                    if res["name"]==parameters["name"] and getpdstr==parapdstr and res["stripe"]==stripemap[parameters["stripe"]]\
                            and res["sector"]==sectormap[parameters["sector"]] and res["force_sync"]==force_syncmap[parameters["force_sync"]] and \
                        res["raid_level"]==raidmap[parameters["raid_level"]]:
                        tolog("Succesfully created pool with parameters %s" %(str(parameters)))
                    else:
                        Failflag=True
                        tolog("Failed to create pool  with parameters %s" % (str(parameters)))

                    deleteobj("pool",0)

    if Failflag:
        tolog(Fail)
    else:
        tolog(Pass)

def poolcreatewithallsettings_invalid_parameters():
    Failflag = False
    name = random_key(30)
    stripesettings = ["64kb", "128kb", "256kb", "512kb", "1mb"]
    sectorsettings = ["512b", "1kb", "2kb", "4kb"]
    force_syncsettings = [0, 1]

    stripemap = {"64kb": "64 KB", "128kb": "128 KB", "256kb": "256 KB", "512kb": "512 KB", "1mb": "1 MB"}
    force_syncmap = {0: "Disabled", 1: "Enabled"}
    raidmap = {"RAID0": 0, "RAID1": 1, "RAID5": 5, "RAID6": 6, "RAID10": 10, "RAID50": 50, "RAID60": 60}
    raids = ["RAID0","RAID1","RAID5","RAID6","RAID10","RAID50","RAID60"]
    availpdlist = getavailpd()
    for raidlevel in raids:
        for stripe in stripesettings:
            for sector in sectorsettings:
                for force_sync in force_syncsettings:
                    if raidlevel=="RAID0":
                        availpdlist=random.sample(availpdlist,2)
                    parameters = {
        "name": name, "pds": availpdlist, "raid_level": raidlevel, "ctrl_id": 1, "stripe": stripe, "sector": sector,
        "force_sync": force_sync}
                    #server.webapiurlbody("post","pool",body=parameters)
                    #print parameters
                    createobj("pool",parameters)
                    res=json.loads(viewobj("pool",0))[0]
                    getpdstr=str(res["pds"]).replace("u","")
                    parapdstr=str(parameters["pds"]).replace("[","").replace("]","").replace(" ","")
                    if res["name"]==parameters["name"] and getpdstr==parapdstr and res["stripe"]==stripemap[parameters["stripe"]]\
                            and res["sector"]==sectormap[parameters["sector"]] and res["force_sync"]==force_syncmap[parameters["force_sync"]] and \
                        res["raid_level"]==raidmap[parameters["raid_level"]]:
                        tolog("Succesfully created pool with parameters %s" %(str(parameters)))
                    else:
                        Failflag=True
                        tolog("Failed to create pool  with parameters %s" % (str(parameters)))

                    deleteobj("pool",0)

    if Failflag:
        tolog(Fail)
    else:
        tolog(Pass)
def viewobj(obj,objid):

    res=server.webapiurlbody("get",obj,urlparameter=str(objid))
    return res["text"]

def PoolCreateListExtendModifyDelete():
    Failflag = False

    name = random_key(10)

    availpdlist = getavailpd()
    pdnum = len(availpdlist)
    stripe = random.choice(["64kb", "128kb", "256kb", "512kb", "1mb"])
    sector = random.choice(["512b", "1kb", "2kb", "4kb"])
    raidlevel=""
    force_sync = random.choice([0, 1])


    stripemap = {"64kb": "64 KB", "128kb": "128 KB", "256kb": "256 KB", "512kb": "512 KB", "1mb": "1 MB"}
    force_syncmap = {0: "Disabled", 1: "Enabled"}
    #raidmap = {"RAID0": 0,"RAID1": 1, "RAID5": 5, "RAID6": 6}
    # new raidlevel will be added soon
    # 2017 -5 -15

    # 2017-6-2
    raidmap = {"RAID0": 0, "RAID1": 1, "RAID5": 5, "RAID6": 6,"RAID10": 10, "RAID50": 50, "RAID60": 60}
    if pdnum >= 1:
        if len(availpdlist)==1:
            raidlevel="RAID0"
        if len(availpdlist) == 2:
            raidlevel = "RAID1"
        elif len(availpdlist) == 3:
            raidlevel = "RAID5"
        elif len(availpdlist) >= 4:
            raidlevel = random.choice(["RAID5", "RAID6"])
        elif len(availpdlist) >= 6:
            raidlevel = "RAID50"
        elif len(availpdlist) >= 8:
            raidlevel = random.choice(["RAID50", "RAID60"])
        pds = random.choice(availpdlist)

        parameters = {
            "name": name, "pds": availpdlist, "raid_level": raidlevel, "ctrl_id": 1, "stripe": stripe, "sector": sector,
            "force_sync": force_sync}

        poolcreateres = server.webapiurlbody("post", "pool", body=parameters)

        if poolcreateres["text"] != "":
            tolog("Creating pool %s with pds %s, raidlevel %s, stripe %s, sector %s, force_sync %s failed" % (
            name, str(availpdlist), raidlevel, stripe, sector, force_sync))
            Failflag = True
        else:

            tolog("Creating pool %s with pds %s, raidlevel %s, stripe %s, sector %s, force_sync %s  sucessfully" % (
                name, str(availpdlist), raidlevel, stripe, sector, force_sync))

        poollistview = server.webapiurlbody("get", "pool")

        # server.webapiurl("delete", "pool", "0?force=0")
        poolview = json.loads(poollistview["text"])

        poolid = ""
        for pool in poolview:

            if pool["name"] == name:
                poolid = str(pool["id"])
                Failflag=CI_VolumeCreateListExtendModifyDelete(pool["id"])
                if pool["sector"] != sectormap[sector] or pool["stripe"] != stripemap[stripe] or pool["raid_level"] != \
                        raidmap[raidlevel] or pool["force_sync"] != force_syncmap[force_sync]:

                    tolog("Verifying the created pool %s failed" % name)
                    Failflag = True
                else:
                    tolog("Verifying the created pool %s sucessfully by api view." % name)
                    # June 23,2017, remove the transfer pool feature
                    # tolog("Verifying transfer the pool %s to different controller by api view.." % name)
                    # transferpara =poolid+ "/transfer"
                    # pooltransferres = server.webapiurlbody("put", "pool", urlparameter=transferpara)
                    # if pooltransferres["text"] != "":
                    #     Failflag = True
                    #     tolog("Pool Transfer failed by api transfer")
                    # else:
                    #     tolog("Pool Transfer successfully by api transfer")

                    newname = {"name":random_key(20)}
                    renameurl = poolid + "/rename"
                    server.webapiurlbody("put", "pool", urlparameter=renameurl,body=newname)

                    poolrenameres = server.webapiurlbody("get", "pool")
                    poolrenameres=json.loads(poolrenameres["text"])
                    #print poolrenameres,poolrenameres["name"]
                    if poolrenameres[0]["name"]!= newname["name"]:
                        Failflag = True
                        tolog("Pool rename failed by api rename")
                    else:
                        tolog("Pool rename successfully by api rename")


                    urlparameter = poolid + "?force=1"
                    pooldeleteres = server.webapiurlbody("delete", "pool", urlparameter=urlparameter)
                    if pooldeleteres["text"] != "":
                        Failflag = True
                        tolog("Pool delete failed by api delete.")
                    else:
                        tolog("Pool delete sucessfully by api delete.")

                    tolog("Verifying extend the pool %s." % name)
                    # 2017-5-12
                    # need create a pool with less disk
                    # extend to more disks
                    # verify the pds in the pool before and after the extend operation

    else:
        tolog("You should have at least one disk to create a pool")

    if Failflag:
        tolog(Fail)
    else:
        tolog(Pass)


def VolumeCreateListExtendModifyDelete(poolid):
    Failflag = False

    name = random_key(10)

    poollistview = server.webapiurlbody("get", "pool")


    poolview = json.loads(poollistview["text"])
    # create volume for each pool

    blocksizelst = ["512b", "1kb", "2kb", "4kb", "8kb", "16kb", "32kb", "64kb", "128kb"]
    sectorsizelst = ["512b", "1kb", "2kb", "4kb"]
    mincapacity = 16
    maxcapacity = 1000000
    compresslst=["off", "lzjb","gzip","gzip1","gzip2","gzip3","gzip4","gzip5","gzip6","gzip7","gzip8","gzip9","zle","lz4"]
    synclst=["standard","always","disabled"]
    thin_provlst=[0,1]

    blocksizemap={"512b":"512 Bytes", "1kb":"1 KB", "2kb":"2 KB", "4kb":"4 KB", "8kb":"8 KB", "16kb":"16 KB", "32kb": "32 KB", "64kb":"64 KB", "128kb":"128 KB"}
    thinmap={0:"Disabled",1: "Enabled"}
    #for pool in poolview:
    blocksize = random.choice(blocksizelst)
    sectorsize = random.choice(sectorsizelst)

    capacity = str(random.randint(mincapacity, maxcapacity)) + "GB"
    compress = random.choice(compresslst)
    compress="off"
    sync = random.choice(synclst)
    thin_prov = random.choice(thin_provlst)
    parameters=dict()
    parameters = {
        "name": name, "pool_id": poolid, "capacity": capacity, "block": blocksize, "sector": sectorsize,
        #"compress": compress,
        "sync": sync, "thin_prov": thin_prov}
    #print parameters
    volumecreateres = server.webapiurlbody("post", "volume", body=parameters)

    if volumecreateres["text"] != "":
        tolog("Creating volume %s failed" % name)
        Failflag = True
    else:

        tolog("Creating volume %s successfully" % name)


        volumelistview = server.webapiurlbody("get", "volume")

    # server.webapiurl("delete", "pool", "0?force=0")
        volumeview = json.loads(volumelistview["text"])
        volumeid = ""
        for volume in volumeview:

            if volume["name"] == name:
                volumeid = str(volume["id"])

            #{u'sector': u'512 Bytes', u'create_date': u'2017-05-11 07:48:16', u'logbias': u'latency', u'sync': u'disabled',
                # u'snapshots': [], u'redundant_md': u'all', u'id': 1, u'ctrl_id': 2, u'export_id': 1, u'operational_status':
                # u'OK, Synchronizing', u'copies': 1, u'thin_prov': u'Enabled', u'used_capacity': 8192, u'written_capacity':
                # u'8.19 KB', u'status': u'Exported', u'pool_name': u'subsystem', u'snapshot_count': u'0', u'used_snapshot': u'0 Byte',
                # u'export_wwn': u'2237000155d6f1dd', u'name': u'xqWrYK8NOL',
                # u'total_capacity': 528594999999488, u'max_snapshot_count': u'1024', u'pool_id': 0, u'used_child': u'0 Byte', u'pool_avail': u'140.42 GB', u'block': u'1 KB'}
                if volume["sector"] != sectormap[sectorsize] or volume["block"] != blocksizemap[blocksize] or volume["sync"] != sync:

                    tolog("Verifying the created volume %s failed" % name)
                    Failflag = True
                else:
                    tolog("Verifying the created volume %s sucessfully by api." % name)

                if volume["status"]=="Exported":
                    tolog("Verifying volume unexport")
                    urlpara=volumeid+"/unexport"
                    unexportres=server.webapiurlbody("post","volume",urlparameter=urlpara)
                    #unexportres = json.loads(unexportres["text"])
                    if unexportres["text"]!="":
                        tolog("Verifying volume unexport failed.")
                        Failflag=True
                    else:
                        tolog("Verifying volume unexport successfully.")
                elif volume["status"]=="Un-exported":
                    tolog("Verifying volume export")
                    urlpara = volumeid + "/export"
                    exportres = server.webapiurlbody("post", "volume", urlparameter=urlpara)
                    # unexportres = json.loads(unexportres["text"])
                    if exportres["text"] != "":
                        tolog("Verifying volume export failed.")
                        Failflag = True

                if volume["status"]=="Un-exported":
                    tolog("Verifying volume export")
                    urlpara=volumeid+"/export"
                    unexportres=server.webapiurlbody("post","volume",urlparameter=urlpara)
                    #unexportres = json.loads(unexportres["text"])
                    if unexportres["text"]!="":
                        tolog("Verifying volume export failed.")
                        Failflag=True
                    else:
                        tolog("Verifying volume export successfully.")
                elif volume["status"]=="Exported":
                    tolog("Verifying volume unexport")
                    urlpara = volumeid + "/unexport"
                    exportres = server.webapiurlbody("post", "volume", urlparameter=urlpara)
                    # unexportres = json.loads(unexportres["text"])
                    if exportres["text"] != "":
                        tolog("Verifying volume unexport failed.")
                        Failflag = True

                newname = {"name": random_key(20)}
                tolog("Verifying modify the volume name from %s to %s by api view." %(name,newname["name"]))
                urlpara =volumeid
                volumerenameres = server.webapiurlbody("put", "volume", urlparameter=urlpara)
                if volumerenameres["text"] != "":
                    Failflag = True
                    tolog("Volume rename failed by api")
                else:

                    # To be added 2017-5-15
                    # Body Parameters
                    #
                    # Body paramemters

                    urlpara=volumeid
                    volumerenameres=server.webapiurlbody("get","volume",urlparameter=urlpara)

                    volumerenameres=json.loads(volumerenameres)
                    if volumerenameres["name"]!=newname:
                        Failflag = True
                        tolog("Volume rename failed by api")

                    else:
                        tolog("Volume rename successfully by api")


                tolog("Verifying volume delete.")
                urlparameter = volumeid + "?force=1"
                volumedeleteres = server.webapiurlbody("delete", "volume", urlparameter=urlparameter)
                if volumedeleteres["text"] != "":
                    Failflag = True
                    tolog("volume delete failed by api delete.")
                else:
                    tolog("volume delete sucessfully by api delete.")

    if Failflag:
        tolog(Fail)
    else:
        tolog(Pass)

def CI_VolumeCreateListExtendModifyDelete(poolid):
    Failflag = False

    name = random_key(10)

    poollistview = server.webapiurlbody("get", "pool")


    poolview = json.loads(poollistview["text"])
    # create volume for each pool

    blocksizelst = ["512b", "1kb", "2kb", "4kb", "8kb", "16kb", "32kb", "64kb", "128kb"]
    sectorsizelst = ["512b", "1kb", "2kb", "4kb"]
    mincapacity = 1
    maxcapacity = 10
    compresslst=["off", "lzjb","gzip","gzip1","gzip2","gzip3","gzip4","gzip5","gzip6","gzip7","gzip8","gzip9","zle","lz4"]
    synclst=["standard","always","disabled"]
    thin_provlst=[0,1]

    blocksizemap={"512b":"512 Bytes", "1kb":"1 KB", "2kb":"2 KB", "4kb":"4 KB", "8kb":"8 KB", "16kb":"16 KB", "32kb": "32 KB", "64kb":"64 KB", "128kb":"128 KB"}
    thinmap={0:"Disabled",1: "Enabled"}
    #for pool in poolview:
    blocksize = random.choice(blocksizelst)
    sectorsize = random.choice(sectorsizelst)

    capacity = str(random.randint(mincapacity, maxcapacity)) + "GB"
    compress = random.choice(compresslst)
    compress="off"
    sync = random.choice(synclst)
    thin_prov = random.choice(thin_provlst)
    parameters=dict()
    parameters = {
        "name": name, "pool_id": poolid, "capacity": capacity, "block": blocksize, "sector": sectorsize,
        #"compress": compress,
        "sync": sync, "thin_prov": thin_prov}

    volumecreateres = server.webapiurlbody("post", "volume", body=parameters)

    if volumecreateres["text"] != "":
        tolog("Creating volume %s failed" % name)
        Failflag = True
    else:

        tolog("Creating volume %s successfully" % name)


        volumelistview = server.webapiurlbody("get", "volume")

    # server.webapiurl("delete", "pool", "0?force=0")
        volumeview = json.loads(volumelistview["text"])
        volumeid = ""
        for volume in volumeview:

            if volume["name"] == name:
                volumeid = str(volume["id"])
                # print volume

            #{u'sector': u'512 Bytes', u'create_date': u'2017-05-11 07:48:16', u'logbias': u'latency', u'sync': u'disabled',
                # u'snapshots': [], u'redundant_md': u'all', u'id': 1, u'ctrl_id': 2, u'export_id': 1, u'operational_status':
                # u'OK, Synchronizing', u'copies': 1, u'thin_prov': u'Enabled', u'used_capacity': 8192, u'written_capacity':
                # u'8.19 KB', u'status': u'Exported', u'pool_name': u'subsystem', u'snapshot_count': u'0', u'used_snapshot': u'0 Byte',
                # u'export_wwn': u'2237000155d6f1dd', u'name': u'xqWrYK8NOL',
                # u'total_capacity': 528594999999488, u'max_snapshot_count': u'1024', u'pool_id': 0, u'used_child': u'0 Byte', u'pool_avail': u'140.42 GB', u'block': u'1 KB'}
                if volume["sector"] != sectormap[sectorsize] or volume["block"] != blocksizemap[blocksize] or volume["sync"] != sync:

                    tolog("Verifying the created volume %s failed" % name)
                    Failflag = True
                else:
                    tolog("Verifying the created volume %s sucessfully by api view." % name)

                for i in range(2):
                    volumelistview = server.webapiurlbody("get", "volume")

                    volumeview = json.loads(volumelistview["text"])
                    for volume1 in volumeview:

                        if volume1["status"]=="Exported":
                            tolog("Verifying volume unexport")
                            urlpara=volumeid+"/unexport"
                            server.webapiurlbody("post","volume",urlparameter=urlpara)
                            #unexportres = json.loads(unexportres["text"])

                            volumelistview = server.webapiurlbody("get", "volume")

                            volumeview = json.loads(volumelistview["text"])
                            for volume2 in volumeview:
                                # print volume1

                                if volume2["name"] == volume["name"] and volume2["status"]=="Un-Exported":
                                    tolog("Verifying volume unexport successfully.")

                                else:
                                    tolog("Verifying volume unexport failed.")
                                    Failflag=True

                        elif volume1["status"]=="Un-Exported":
                            tolog("Verifying volume export")
                            urlpara = volumeid + "/export"
                            server.webapiurlbody("post", "volume", urlparameter=urlpara)
                            volumelistview = server.webapiurlbody("get", "volume")

                            volumeview = json.loads(volumelistview["text"])
                            for volume2 in volumeview:

                                if volume2["name"] == volume["name"] and volume2["status"] == "Exported":
                                    tolog("Verifying volume export successfully.")

                                else:
                                    tolog("Verifying volume export failed.")
                                    Failflag = True

                newname = {"name": random_key(20)}
                tolog("Verifying modify the volume name from %s to %s by api view." %(name,newname["name"]))
                urlpara =volumeid
                server.webapiurlbody("put", "volume", urlparameter=urlpara,body=newname)  # To be added 2017-5-15


                urlpara = volumeid
                volumerenameres = server.webapiurlbody("get", "volume", urlparameter=urlpara)

                volumerenameres = json.loads(volumerenameres["text"])
                
                if volumerenameres[0]["name"] != newname:
                    Failflag = True
                    tolog("Volume rename failed by api")

                else:
                    tolog("Volume rename successfully by api")


                tolog("Verifying volume delete.")
                urlparameter = volumeid + "?force=1"
                volumedeleteres = server.webapiurlbody("delete", "volume", urlparameter=urlparameter)
                if volumedeleteres["text"] != "":
                    Failflag = True
                    tolog("volume delete failed by api delete.")
                else:
                    tolog("volume delete sucessfully by api delete.")


        return Failflag

def snapshotstatus(id,op):
    pass


def SnapshotCreateListModifyDelete(sourceid):

    Failflag = False

    name = random_key(10)

    volumelistview = server.webapi("get", "volume")


    volumeview = json.loads(volumelistview["text"])
    # create snapshot for each volume
    type=random.choice({"volume","filesystem"})
    # do not support filesysrtem
    # as to 2017-5-15
    type="volume"

    parameters=dict()
    parameters = {
        "name": name, "source_id": sourceid,"type":type}

    volumecreateres = server.webapiurlbody("post", "snapshot", body=parameters)

    if volumecreateres["text"] != "":
        tolog("Creating snapshot %s failed" % name)
        Failflag = True
    else:

        tolog("Creating snapshot %s successfully" % name)

        snapshotlistview = server.webapiurlbody("get", "snapshot")

    # server.webapiurl("delete", "pool", "0?force=0")
        snapshotview = json.loads(snapshotlistview["text"])
        volumeid = ""
        for snapshot in snapshotview:

            if snapshot["name"] == name:
                snapshotid = str(snapshot["id"])


                if snapshot["type"] != type or snapshot["source_id"] != sourceid:

                    tolog("Verifying the created snapshot %s failed" % name)
                    Failflag = True
                else:
                    tolog("Verifying the created snapshot %s sucessfully by api view." % name)

                if snapshot["status"]=="Exported":
                    tolog("Verifying snapshot unexport")
                    urlpara=snapshotid+"/unexport"
                    unexportres=server.webapiurlbody("post","snapshot",urlparameter=urlpara)
                    #unexportres = json.loads(unexportres["text"])
                    if unexportres["text"]!="":
                        tolog("Verifying snapshot unexport failed.")
                        Failflag=True
                    else:
                        tolog("Verifying volume unexport successfully.")
                elif snapshot["status"]=="Un-exported":
                    tolog("Verifying snapshot export")
                    urlpara = snapshotid + "/export"
                    exportres = server.webapiurlbody("post", "snapshot", urlparameter=urlpara)
                    # unexportres = json.loads(unexportres["text"])
                    if exportres["text"] != "":
                        tolog("Verifying snapshot export failed.")
                        Failflag = True

                if snapshot["status"]=="Un-exported":
                    tolog("Verifying snapshot export")
                    urlpara=volumeid+"/export"
                    unexportres=server.webapiurlbody("post","snapshot",urlparameter=urlpara)
                    #unexportres = json.loads(unexportres["text"])
                    if unexportres["text"]!="":
                        tolog("Verifying snapshot export failed.")
                        Failflag=True
                    else:
                        tolog("Verifying snapshot export successfully.")
                elif snapshot["status"]=="Exported":
                    tolog("Verifying snapshot unexport")
                    urlpara = snapshotid + "/unexport"
                    exportres = server.webapiurlbody("post", "snapshot", urlparameter=urlpara)
                    # unexportres = json.loads(unexportres["text"])
                    if exportres["text"] != "":
                        tolog("Verifying snapshot unexport failed.")
                        Failflag = True
                if snapshot["status"]=="Exported":
                    tolog("Verifying snapshot unexport")
                    urlpara=snapshotid+"/unexport"
                    unexportres=server.webapiurlbody("post","snapshot",urlparameter=urlpara)
                    #unexportres = json.loads(unexportres["text"])
                    if unexportres["text"]!="":
                        tolog("Verifying snapshot unexport failed.")
                        Failflag=True
                    else:
                        tolog("Verifying volume unexport successfully.")
                elif snapshot["status"]=="Un-exported":
                    tolog("Verifying snapshot export")
                    urlpara = snapshotid + "/export"
                    exportres = server.webapiurlbody("post", "snapshot", urlparameter=urlpara)
                    # unexportres = json.loads(unexportres["text"])
                    if exportres["text"] != "":
                        tolog("Verifying snapshot export failed.")
                        Failflag = True

                if snapshot["status"]=="Un-exported":
                    tolog("Verifying snapshot export")
                    urlpara=volumeid+"/export"
                    unexportres=server.webapiurlbody("post","snapshot",urlparameter=urlpara)
                    #unexportres = json.loads(unexportres["text"])
                    if unexportres["text"]!="":
                        tolog("Verifying snapshot export failed.")
                        Failflag=True
                    else:
                        tolog("Verifying snapshot export successfully.")
                elif snapshot["status"]=="Exported":
                    tolog("Verifying snapshot unexport")
                    urlpara = snapshotid + "/unexport"
                    exportres = server.webapiurlbody("post", "snapshot", urlparameter=urlpara)
                    # unexportres = json.loads(unexportres["text"])
                    if exportres["text"] != "":
                        tolog("Verifying snapshot unexport failed.")
                        Failflag = True


                newname = {"name": random_key(20)}
                tolog("Verifying modify the snapshot name from %s to %sby api view." %(name,newname))
                urlpara =snapshotid
                renameres = server.webapiurlbody("put", "snapshot", urlparameter=urlpara)
                if renameres["text"] != "":
                    Failflag = True
                    tolog("snapshot rename failed by api")
                else:

                    # To be added 2017-5-15
                    # Body Parameters
                    #
                    # Body paramemters

                    urlpara=snapshotid
                    renameres=server.webapiurlbody("get","snapshot",urlparameter=urlpara)

                    renameres=json.loads(renameres)
                    if renameres["name"]!=newname:
                        Failflag = True
                        tolog("snapshot rename failed by api")

                    else:
                        tolog("snapshot rename successfully by api")


                tolog("Verifying snapshot delete.")
                urlparameter = snapshotid + "?force=1"
                deleteres = server.webapiurlbody("delete", "snapshot", urlparameter=urlparameter)
                if deleteres["text"] != "":
                    Failflag = True
                    tolog("snapshot delete failed by api delete.")
                else:
                    tolog("snapshot delete sucessfully by api delete.")

    if Failflag:
        tolog(Fail)
    else:
        tolog(Pass)

def CloneCreateListModifyDelete(sourceid):

    Failflag = False

    name = random_key(10)

    volumelistview = server.webapiurlbody("get", "volume")


    volumeview = json.loads(volumelistview["text"])
    # create snapshot for each volume
    type=random.choice({"volume","filesystem"})
    # do not support filesysrtem
    # as to 2017-5-15
    type="volume"

    parameters=dict()
    parameters = {
        "name": name, "source_id": sourceid,"type":type}

    volumecreateres = server.webapiurlbody("post", "snapshot", body=parameters)

    if volumecreateres["text"] != "":
        tolog("Creating snapshot %s failed" % name)
        Failflag = True
    else:

        tolog("Creating snapshot %s successfully" % name)

        snapshotlistview = server.webapi("get", "snapshot")

    # server.webapiurl("delete", "pool", "0?force=0")
        snapshotview = json.loads(snapshotlistview["text"])
        volumeid = ""
        for snapshot in snapshotview:

            if snapshot["name"] == name:
                snapshotid = str(snapshot["id"])


                if snapshot["type"] != type or snapshot["source_id"] != sourceid:

                    tolog("Verifying the created snapshot %s failed" % name)
                    Failflag = True
                else:
                    tolog("Verifying the created snapshot %s sucessfully by api view." % name)

                if snapshot["status"]=="Exported":
                    tolog("Verifying snapshot unexport")
                    urlpara=snapshotid+"/unexport"
                    unexportres=server.webapiurlbody("post","snapshot",urlparameter=urlpara)
                    #unexportres = json.loads(unexportres["text"])
                    if unexportres["text"]!="":
                        tolog("Verifying snapshot unexport failed.")
                        Failflag=True
                    else:
                        tolog("Verifying volume unexport successfully.")
                elif snapshot["status"]=="Un-exported":
                    tolog("Verifying snapshot export")
                    urlpara = snapshotid + "/export"
                    exportres = server.webapiurlbody("post", "snapshot", urlparameter=urlpara)
                    # unexportres = json.loads(unexportres["text"])
                    if exportres["text"] != "":
                        tolog("Verifying snapshot export failed.")
                        Failflag = True

                if snapshot["status"]=="Un-exported":
                    tolog("Verifying snapshot export")
                    urlpara=volumeid+"/export"
                    unexportres=server.webapiurlbody("post","snapshot",urlparameter=urlpara)
                    #unexportres = json.loads(unexportres["text"])
                    if unexportres["text"]!="":
                        tolog("Verifying snapshot export failed.")
                        Failflag=True
                    else:
                        tolog("Verifying snapshot export successfully.")
                elif snapshot["status"]=="Exported":
                    tolog("Verifying snapshot unexport")
                    urlpara = snapshotid + "/unexport"
                    exportres = server.webapiurlbody("post", "snapshot", urlparameter=urlpara)
                    # unexportres = json.loads(unexportres["text"])
                    if exportres["text"] != "":
                        tolog("Verifying snapshot unexport failed.")
                        Failflag = True
                if snapshot["status"]=="Exported":
                    tolog("Verifying snapshot unexport")
                    urlpara=snapshotid+"/unexport"
                    unexportres=server.webapiurlbody("post","snapshot",urlparameter=urlpara)
                    #unexportres = json.loads(unexportres["text"])
                    if unexportres["text"]!="":
                        tolog("Verifying snapshot unexport failed.")
                        Failflag=True
                    else:
                        tolog("Verifying volume unexport successfully.")
                elif snapshot["status"]=="Un-exported":
                    tolog("Verifying snapshot export")
                    urlpara = snapshotid + "/export"
                    exportres = server.webapiurlbody("post", "snapshot", urlparameter=urlpara)
                    # unexportres = json.loads(unexportres["text"])
                    if exportres["text"] != "":
                        tolog("Verifying snapshot export failed.")
                        Failflag = True

                if snapshot["status"]=="Un-exported":
                    tolog("Verifying snapshot export")
                    urlpara=volumeid+"/export"
                    unexportres=server.webapiurlbody("post","snapshot",urlparameter=urlpara)
                    #unexportres = json.loads(unexportres["text"])
                    if unexportres["text"]!="":
                        tolog("Verifying snapshot export failed.")
                        Failflag=True
                    else:
                        tolog("Verifying snapshot export successfully.")
                elif snapshot["status"]=="Exported":
                    tolog("Verifying snapshot unexport")
                    urlpara = snapshotid + "/unexport"
                    exportres = server.webapiurlbody("post", "snapshot", urlparameter=urlpara)
                    # unexportres = json.loads(unexportres["text"])
                    if exportres["text"] != "":
                        tolog("Verifying snapshot unexport failed.")
                        Failflag = True


                newname = {"name": random_key(20)}
                tolog("Verifying modify the snapshot name from %s to %sby api view." %(name,newname))
                urlpara =snapshotid
                renameres = server.webapiurlbody("put", "snapshot", urlparameter=urlpara)
                if renameres["text"] != "":
                    Failflag = True
                    tolog("snapshot rename failed by api")
                else:

                    # To be added 2017-5-15
                    # Body Parameters
                    #
                    # Body paramemters

                    urlpara=snapshotid
                    renameres=server.webapiurlbody("get","snapshot",urlparameter=urlpara)

                    renameres=json.loads(renameres)
                    if renameres["name"]!=newname:
                        Failflag = True
                        tolog("snapshot rename failed by api")

                    else:
                        tolog("snapshot rename successfully by api")


                tolog("Verifying snapshot delete.")
                urlparameter = snapshotid + "?force=1"
                deleteres = server.webapiurlbody("delete", "snapshot", urlparameter=urlparameter)
                if deleteres["text"] != "":
                    Failflag = True
                    tolog("snapshot delete failed by api delete.")
                else:
                    tolog("snapshot delete sucessfully by api delete.")

    if Failflag:
        tolog(Fail)
    else:
        tolog(Pass)


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

        if eachpd["op_status"] == "OK" and ("Pool" in eachpd["cfg_status"] or  "Spare" in eachpd["cfg_status"] ) and eachpd["type"] == "SAS HDD":
            pdlist.append(eachpd["id"])

    return pdlist


def cleanpool():
    res = server.webapiurlbody("get", "pool")
    poollist = list()
    cleanrestext = json.loads(res["text"])

    for eachpool in cleanrestext:
        urlpara=str(eachpool["id"])+"?force=1"
        res=server.webapiurlbody("delete","pool",urlparameter=urlpara)
        print str((res["text"]))

def createobj(obj,setting):
    Failflag=False
    createres = server.webapiurlbody("post", obj, body=setting)

    if createres["text"] != "":
        tolog("Creating %s with %s failed" % (obj,str(setting)))
        Failflag = True
    else:
        tolog("Creating %s with %s successfully" % (obj, str(setting)))

    return Failflag
def deleteobj(obj,objid):
    Failflag = False
    urlpara=str(objid)+"?force=1"
    res = server.webapiurlbody("delete", obj, urlparameter=urlpara)
    if res["text"] != "":
        tolog("Deleting %s %s failed" % (obj,str(objid)))
        Failflag = True
    else:
        tolog("Deleting %s %s successfully" % (obj, str(objid)))

    return Failflag



if __name__ == "__main__":

    cleanpool()
    poolcreatewithallsettings()

    cleanpool()