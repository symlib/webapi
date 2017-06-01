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

def PoolCreateListExtendModifyDelete():
    Failflag = False

    name = random_key(10)

    availpdlist = getavailpd()
    pdnum = len(availpdlist)
    stripe = random.choice(["64kb", "128kb", "256kb", "512kb", "1mb"])
    sector = random.choice(["512b", "1kb", "2kb", "4kb"])

    force_sync = random.choice([0, 1])


    stripemap = {"64kb": "64 KB", "128kb": "128 KB", "256kb": "256 KB", "512kb": "512 KB", "1mb": "1 MB"}
    force_syncmap = {0: "Disabled", 1: "Enabled"}
    raidmap = {"RAID0": 0,"RAID1": 1, "RAID5": 5, "RAID6": 6}
    # new raidlevel will be added soon
    # 2015 -5 -15
    if pdnum >= 2:
        if len(availpdlist)==1:
            raidlevel="RAID0"
        if len(availpdlist) == 2:
            raidlevel = "RAID1"
        elif len(availpdlist) == 3:
            raidlevel = "RAID5"
        elif len(availpdlist) >= 4:
            raidlevel = random.choice(["RAID5", "RAID6"])

        pds = random.choice(availpdlist)

        parameters = {
            "name": name, "pds": availpdlist, "raid_level": raidlevel, "ctrl_id": 1, "stripe": stripe, "sector": sector,
            "force_sync": force_sync}

        poolcreateres = server.webapi("post", "pool", parameters)

        if poolcreateres["text"] != "":
            tolog("Creating pool %s with pds %s, raidlevel %s, stripe %s, sector %s, force_sync %s failed" % (
            name, str(availpdlist), raidlevel, stripe, sector, force_sync))
            Failflag = True
        else:

            tolog("Creating pool %s with pds %s, raidlevel %s, stripe %s, sector %s, force_sync %s  sucessfully" % (
                name, str(availpdlist), raidlevel, stripe, sector, force_sync))

        poollistview = server.webapi("get", "pool")

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

                    tolog("Verifying transfer the pool %s to different controller by api view.." % name)
                    transferpara =poolid+ "/transfer"
                    pooltransferres = server.webapiurl("put", "pool", transferpara)
                    if pooltransferres["text"] != "":
                        Failflag = True
                        tolog("Pool Transfer failed by api transfer")
                    else:
                        tolog("Pool Transfer successfully by api transfer")

                    newname = {"name":random_key(20)}
                    renameurl = poolid + "/rename"
                    server.webapiurlbody("put", "pool", renameurl,newname)

                    poolrenameres = server.webapi("get", "pool")
                    poolrenameres=json.loads(poolrenameres["text"])
                    #print poolrenameres,poolrenameres["name"]
                    if poolrenameres[0]["name"]!= newname["name"]:
                        Failflag = True
                        tolog("Pool rename failed by api rename")
                    else:
                        tolog("Pool rename successfully by api rename")


                    urlparameter = poolid + "?force=1"
                    pooldeleteres = server.webapiurl("delete", "pool", urlparameter)
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
        tolog("You should have at least two disks to create a pool")

    if Failflag:
        tolog(Fail)
    else:
        tolog(Pass)


def VolumeCreateListExtendModifyDelete(poolid):
    Failflag = False

    name = random_key(10)

    poollistview = server.webapi("get", "pool")


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
    print parameters
    volumecreateres = server.webapi("post", "volume", parameters)

    if volumecreateres["text"] != "":
        tolog("Creating volume %s failed" % name)
        Failflag = True
    else:

        tolog("Creating volume %s successfully" % name)


        volumelistview = server.webapi("get", "volume")

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
                    tolog("Verifying the created volume %s sucessfully by api view." % name)

                if volume["status"]=="Exported":
                    tolog("Verifying volume unexport")
                    urlpara=volumeid+"/unexport"
                    unexportres=server.webapiurl("post","volume",urlpara)
                    #unexportres = json.loads(unexportres["text"])
                    if unexportres["text"]!="":
                        tolog("Verifying volume unexport failed.")
                        Failflag=True
                    else:
                        tolog("Verifying volume unexport successfully.")
                elif volume["status"]=="Un-exported":
                    tolog("Verifying volume export")
                    urlpara = volumeid + "/export"
                    exportres = server.webapiurl("post", "volume", urlpara)
                    # unexportres = json.loads(unexportres["text"])
                    if exportres["text"] != "":
                        tolog("Verifying volume export failed.")
                        Failflag = True

                if volume["status"]=="Un-exported":
                    tolog("Verifying volume export")
                    urlpara=volumeid+"/export"
                    unexportres=server.webapiurl("post","volume",urlpara)
                    #unexportres = json.loads(unexportres["text"])
                    if unexportres["text"]!="":
                        tolog("Verifying volume export failed.")
                        Failflag=True
                    else:
                        tolog("Verifying volume export successfully.")
                elif volume["status"]=="Exported":
                    tolog("Verifying volume unexport")
                    urlpara = volumeid + "/unexport"
                    exportres = server.webapiurl("post", "volume", urlpara)
                    # unexportres = json.loads(unexportres["text"])
                    if exportres["text"] != "":
                        tolog("Verifying volume unexport failed.")
                        Failflag = True

                newname = {"name": random_key(20)}
                tolog("Verifying modify the volume name from %s to %s by api view." %(name,newname["name"]))
                urlpara =volumeid
                volumerenameres = server.webapiurl("put", "volume", urlpara)
                if volumerenameres["text"] != "":
                    Failflag = True
                    tolog("Volume rename failed by api")
                else:

                    # To be added 2017-5-15
                    # Body Parameters
                    #
                    # Body paramemters

                    urlpara=volumeid
                    volumerenameres=server.webapi("get","volume",urlpara)

                    volumerenameres=json.loads(volumerenameres)
                    if volumerenameres["name"]!=newname:
                        Failflag = True
                        tolog("Volume rename failed by api")

                    else:
                        tolog("Volume rename successfully by api")


                tolog("Verifying volume delete.")
                urlparameter = volumeid + "?force=1"
                volumedeleteres = server.webapiurl("delete", "volume", urlparameter)
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

    poollistview = server.webapi("get", "pool")


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
    print parameters
    volumecreateres = server.webapi("post", "volume", parameters)

    if volumecreateres["text"] != "":
        tolog("Creating volume %s failed" % name)
        Failflag = True
    else:

        tolog("Creating volume %s successfully" % name)


        volumelistview = server.webapi("get", "volume")

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
                    tolog("Verifying the created volume %s sucessfully by api view." % name)

                if volume["status"]=="Exported":
                    tolog("Verifying volume unexport")
                    urlpara=volumeid+"/unexport"
                    unexportres=server.webapiurl("post","volume",urlpara)
                    #unexportres = json.loads(unexportres["text"])
                    if unexportres["text"]!="":
                        tolog("Verifying volume unexport failed.")
                        Failflag=True
                    else:
                        tolog("Verifying volume unexport successfully.")
                elif volume["status"]=="Un-exported":
                    tolog("Verifying volume export")
                    urlpara = volumeid + "/export"
                    exportres = server.webapiurl("post", "volume", urlpara)
                    # unexportres = json.loads(unexportres["text"])
                    if exportres["text"] != "":
                        tolog("Verifying volume export failed.")
                        Failflag = True

                if volume["status"]=="Un-exported":
                    tolog("Verifying volume export")
                    urlpara=volumeid+"/export"
                    unexportres=server.webapiurl("post","volume",urlpara)
                    #unexportres = json.loads(unexportres["text"])
                    if unexportres["text"]!="":
                        tolog("Verifying volume export failed.")
                        Failflag=True
                    else:
                        tolog("Verifying volume export successfully.")
                elif volume["status"]=="Exported":
                    tolog("Verifying volume unexport")
                    urlpara = volumeid + "/unexport"
                    exportres = server.webapiurl("post", "volume", urlpara)
                    # unexportres = json.loads(unexportres["text"])
                    if exportres["text"] != "":
                        tolog("Verifying volume unexport failed.")
                        Failflag = True

                newname = {"name": random_key(20)}
                tolog("Verifying modify the volume name from %s to %sby api view." %(name,newname))
                urlpara =volumeid
                volumerenameres = server.webapiurl("put", "volume", urlpara)
                if volumerenameres["text"] != "":
                    Failflag = True
                    tolog("Volume rename failed by api")
                else:

                    # To be added 2017-5-15
                    # Body Parameters
                    #
                    # Body paramemters

                    urlpara=volumeid
                    volumerenameres=server.webapi("get","volume",urlpara)

                    volumerenameres=json.loads(volumerenameres)
                    if volumerenameres["name"]!=newname:
                        Failflag = True
                        tolog("Volume rename failed by api")

                    else:
                        tolog("Volume rename successfully by api")


                tolog("Verifying volume delete.")
                urlparameter = volumeid + "?force=1"
                volumedeleteres = server.webapiurl("delete", "volume", urlparameter)
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

    volumecreateres = server.webapi("post", "snapshot", parameters)

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
                    unexportres=server.webapiurl("post","snapshot",urlpara)
                    #unexportres = json.loads(unexportres["text"])
                    if unexportres["text"]!="":
                        tolog("Verifying snapshot unexport failed.")
                        Failflag=True
                    else:
                        tolog("Verifying volume unexport successfully.")
                elif snapshot["status"]=="Un-exported":
                    tolog("Verifying snapshot export")
                    urlpara = snapshotid + "/export"
                    exportres = server.webapiurl("post", "snapshot", urlpara)
                    # unexportres = json.loads(unexportres["text"])
                    if exportres["text"] != "":
                        tolog("Verifying snapshot export failed.")
                        Failflag = True

                if snapshot["status"]=="Un-exported":
                    tolog("Verifying snapshot export")
                    urlpara=volumeid+"/export"
                    unexportres=server.webapiurl("post","snapshot",urlpara)
                    #unexportres = json.loads(unexportres["text"])
                    if unexportres["text"]!="":
                        tolog("Verifying snapshot export failed.")
                        Failflag=True
                    else:
                        tolog("Verifying snapshot export successfully.")
                elif snapshot["status"]=="Exported":
                    tolog("Verifying snapshot unexport")
                    urlpara = snapshotid + "/unexport"
                    exportres = server.webapiurl("post", "snapshot", urlpara)
                    # unexportres = json.loads(unexportres["text"])
                    if exportres["text"] != "":
                        tolog("Verifying snapshot unexport failed.")
                        Failflag = True
                if snapshot["status"]=="Exported":
                    tolog("Verifying snapshot unexport")
                    urlpara=snapshotid+"/unexport"
                    unexportres=server.webapiurl("post","snapshot",urlpara)
                    #unexportres = json.loads(unexportres["text"])
                    if unexportres["text"]!="":
                        tolog("Verifying snapshot unexport failed.")
                        Failflag=True
                    else:
                        tolog("Verifying volume unexport successfully.")
                elif snapshot["status"]=="Un-exported":
                    tolog("Verifying snapshot export")
                    urlpara = snapshotid + "/export"
                    exportres = server.webapiurl("post", "snapshot", urlpara)
                    # unexportres = json.loads(unexportres["text"])
                    if exportres["text"] != "":
                        tolog("Verifying snapshot export failed.")
                        Failflag = True

                if snapshot["status"]=="Un-exported":
                    tolog("Verifying snapshot export")
                    urlpara=volumeid+"/export"
                    unexportres=server.webapiurl("post","snapshot",urlpara)
                    #unexportres = json.loads(unexportres["text"])
                    if unexportres["text"]!="":
                        tolog("Verifying snapshot export failed.")
                        Failflag=True
                    else:
                        tolog("Verifying snapshot export successfully.")
                elif snapshot["status"]=="Exported":
                    tolog("Verifying snapshot unexport")
                    urlpara = snapshotid + "/unexport"
                    exportres = server.webapiurl("post", "snapshot", urlpara)
                    # unexportres = json.loads(unexportres["text"])
                    if exportres["text"] != "":
                        tolog("Verifying snapshot unexport failed.")
                        Failflag = True


                newname = {"name": random_key(20)}
                tolog("Verifying modify the snapshot name from %s to %sby api view." %(name,newname))
                urlpara =snapshotid
                renameres = server.webapiurl("put", "snapshot", urlpara)
                if renameres["text"] != "":
                    Failflag = True
                    tolog("snapshot rename failed by api")
                else:

                    # To be added 2017-5-15
                    # Body Parameters
                    #
                    # Body paramemters

                    urlpara=snapshotid
                    renameres=server.webapi("get","snapshot",urlpara)

                    renameres=json.loads(renameres)
                    if renameres["name"]!=newname:
                        Failflag = True
                        tolog("snapshot rename failed by api")

                    else:
                        tolog("snapshot rename successfully by api")


                tolog("Verifying snapshot delete.")
                urlparameter = snapshotid + "?force=1"
                deleteres = server.webapiurl("delete", "snapshot", urlparameter)
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

    volumecreateres = server.webapi("post", "snapshot", parameters)

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
                    unexportres=server.webapiurl("post","snapshot",urlpara)
                    #unexportres = json.loads(unexportres["text"])
                    if unexportres["text"]!="":
                        tolog("Verifying snapshot unexport failed.")
                        Failflag=True
                    else:
                        tolog("Verifying volume unexport successfully.")
                elif snapshot["status"]=="Un-exported":
                    tolog("Verifying snapshot export")
                    urlpara = snapshotid + "/export"
                    exportres = server.webapiurl("post", "snapshot", urlpara)
                    # unexportres = json.loads(unexportres["text"])
                    if exportres["text"] != "":
                        tolog("Verifying snapshot export failed.")
                        Failflag = True

                if snapshot["status"]=="Un-exported":
                    tolog("Verifying snapshot export")
                    urlpara=volumeid+"/export"
                    unexportres=server.webapiurl("post","snapshot",urlpara)
                    #unexportres = json.loads(unexportres["text"])
                    if unexportres["text"]!="":
                        tolog("Verifying snapshot export failed.")
                        Failflag=True
                    else:
                        tolog("Verifying snapshot export successfully.")
                elif snapshot["status"]=="Exported":
                    tolog("Verifying snapshot unexport")
                    urlpara = snapshotid + "/unexport"
                    exportres = server.webapiurl("post", "snapshot", urlpara)
                    # unexportres = json.loads(unexportres["text"])
                    if exportres["text"] != "":
                        tolog("Verifying snapshot unexport failed.")
                        Failflag = True
                if snapshot["status"]=="Exported":
                    tolog("Verifying snapshot unexport")
                    urlpara=snapshotid+"/unexport"
                    unexportres=server.webapiurl("post","snapshot",urlpara)
                    #unexportres = json.loads(unexportres["text"])
                    if unexportres["text"]!="":
                        tolog("Verifying snapshot unexport failed.")
                        Failflag=True
                    else:
                        tolog("Verifying volume unexport successfully.")
                elif snapshot["status"]=="Un-exported":
                    tolog("Verifying snapshot export")
                    urlpara = snapshotid + "/export"
                    exportres = server.webapiurl("post", "snapshot", urlpara)
                    # unexportres = json.loads(unexportres["text"])
                    if exportres["text"] != "":
                        tolog("Verifying snapshot export failed.")
                        Failflag = True

                if snapshot["status"]=="Un-exported":
                    tolog("Verifying snapshot export")
                    urlpara=volumeid+"/export"
                    unexportres=server.webapiurl("post","snapshot",urlpara)
                    #unexportres = json.loads(unexportres["text"])
                    if unexportres["text"]!="":
                        tolog("Verifying snapshot export failed.")
                        Failflag=True
                    else:
                        tolog("Verifying snapshot export successfully.")
                elif snapshot["status"]=="Exported":
                    tolog("Verifying snapshot unexport")
                    urlpara = snapshotid + "/unexport"
                    exportres = server.webapiurl("post", "snapshot", urlpara)
                    # unexportres = json.loads(unexportres["text"])
                    if exportres["text"] != "":
                        tolog("Verifying snapshot unexport failed.")
                        Failflag = True


                newname = {"name": random_key(20)}
                tolog("Verifying modify the snapshot name from %s to %sby api view." %(name,newname))
                urlpara =snapshotid
                renameres = server.webapiurl("put", "snapshot", urlpara)
                if renameres["text"] != "":
                    Failflag = True
                    tolog("snapshot rename failed by api")
                else:

                    # To be added 2017-5-15
                    # Body Parameters
                    #
                    # Body paramemters

                    urlpara=snapshotid
                    renameres=server.webapi("get","snapshot",urlpara)

                    renameres=json.loads(renameres)
                    if renameres["name"]!=newname:
                        Failflag = True
                        tolog("snapshot rename failed by api")

                    else:
                        tolog("snapshot rename successfully by api")


                tolog("Verifying snapshot delete.")
                urlparameter = snapshotid + "?force=1"
                deleteres = server.webapiurl("delete", "snapshot", urlparameter)
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
    res = server.webapi("get", "phydrv")
    pdlist = list()
    cleanrestext = json.loads(res["text"])

    for eachpd in cleanrestext:

        if eachpd["op_status"] == "OK" and eachpd["cfg_status"] == "Unconfigured" and eachpd["type"] == "SAS HDD":
            pdlist.append(eachpd["id"])

    return pdlist

def getusedpd():
    res = server.webapi("get", "phydrv")
    pdlist = list()
    cleanrestext = json.loads(res["text"])

    for eachpd in cleanrestext:

        if eachpd["op_status"] == "OK" and ("Pool" in eachpd["cfg_status"] or  "Spare" in eachpd["cfg_status"] ) and eachpd["type"] == "SAS HDD":
            pdlist.append(eachpd["id"])

    return pdlist


serverip = "10.84.2.164"
from requests import Request, Session


# url='https://10.84.2.164/serivce/'

def setupsession():
    data = {"username": "administrator", "password": "password"}
    s = requests.Session()

    url = "https://" + serverip + "/service/login"
    header = dict()
    header["Content-Type"] = "application/json"
    req = s.post(url, data=json.dumps(data), headers=header, verify=False)
    addinfo = req.text.find(",")

    header["additioninfo"] = req.text[2:addinfo - 1]

    return s, header

    # prepped = req.prepare()
    # prepped = s.prepare_request(req)

    # return s, prepped


def webapibody(method, service, body):
    pass


def webapiurlparams(method, service, urlpara):
    pass


if __name__ == "__main__":


    PoolCreateListExtendModifyDelete()
