#!/usr/bin/python

import sys
import time
from kazoo.client import KazooClient

PLAYER_PATH = "/players"
BOARD_PATH = "/board"

class watcher:

    def __init__(self, ip, size):
        self.ip = ip
        self.size = abs(int(size))
        self.zk = KazooClient(hosts=ip)

    def __del__(self):
        if self.zk.connected:
            self.zk.stop()

    def start_and_go(self):
        self.zk.start()
        print 'watcher started'
        while 1:
            data, stat = self.zk.get(PLAYER_PATH)
            if data == "updated":
                recent = []
                highest = []
                maps = {}
                history, stat = self.zk.get(BOARD_PATH)
                users = history.split('/')
                for i in reversed(users):
                    if len(i):
                        arr = i.split('#')
                        a = arr[1].split('+')
                        if arr[0] not in maps:
                            maps[arr[0]] = "**" if a[1] == '1' else ""
                        if len(recent) < self.size:
                            recent.append(str(arr[0]) + "    " + str(a[0]) + "  " + maps[arr[0]])
                        highest.append((int(a[0]), arr[0] + "--" + maps[arr[0]]))
                highest.sort(key=lambda tup: tup[0], reverse=True)
                highest = highest[:self.size]
                print "Most recent scores"
                print "------------------"
                for i in recent:
                    print i
                print ''
                print "Most highest scores"
                print "-------------------"
                for i in highest:
                    arr = i[1].split("--")
                    print '{}    {} {}'.format(arr[0], i[0], arr[1])
                self.zk.set(PLAYER_PATH, "")

if __name__ == "__main__":
    argv = sys.argv
    argv_len = len(argv)
    if argv_len  >= 3:
        size = int(argv[2])
        if size < 0:
            print 'invalid negative list size, exiting-----'
            sys.exit()
        if size > 25:
            print 'maximum list size is 25, reset to 25 now---'
        w = watcher(argv[1], min(size, 25))
        w.start_and_go()
    else:
        print 'input IP and maximum list size'
