

import time
import remote

class Pool():
    def poolcreate(self):
        pass
    def poollistview(self):
        pass
    def poolextend(self):
        pass
    def poolmodify(self):
        pass


if __name__ == "__main__":

    start=time.clock()


    # parameters = {
    #     "name": "abc", "pds": "10,11,12", "raid_level": "raid5", "ctrl_id": 1}
    res=remote.server.webapi("get","pool")
    print res['text']