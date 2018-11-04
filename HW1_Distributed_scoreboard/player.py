#!/usr/bin/python

import sys
import time
from kazoo.client import KazooClient
from scipy.stats import truncnorm

PLAYER_PATH = "/players"
BOARD_PATH = "/board"
DEFAULT_COUNT = 20
DEFAULT_DELAY = 1
DEFAULT_MEAN = 500

class player:

    def __init__(self, ip, name, count, delay, mean):
        self.ip = ip
        self.name = name
        self.path = PLAYER_PATH + '/' + name
        self.counter = abs(int(count))
        self.delay = abs(float(delay))
        self.mean = abs(float(mean))
        self.up = self.mean * 2
        self.zk = KazooClient(hosts=self.ip)

    def __del__(self):
        self.leave()

    def leave(self):
        if self.zk.connected:
            data, stat = self.zk.get(self.path)
            data = data.split('+')[0] + '+0'
            self.zk.set(self.path, data)
            d, s = self.zk.get("/board")
            self.zk.set("/board", d + '/' + self.name + '#' + data)
            self.zk.stop()

    def check_and_go(self):
        self.zk.start()
        self.zk.ensure_path(PLAYER_PATH)
        self.zk.ensure_path(BOARD_PATH)
        if self.zk.exists(self.path):
            data, stat = self.zk.get(self.path)
            data = data.decode("utf-8")
            if len(data) and data.split('+')[1] == '1':
                self.zk.stop()
                print 'duplicate player name, please reEnter'
                sys.exit()
            else:
                ZK = self.zk
                @ZK.DataWatch(self.path)
                def watch_node(data, stat):
                    ZK.set(PLAYER_PATH, 'updated')
        else:
            self.zk.create(self.path)
            ZK = self.zk
            @ZK.DataWatch(self.path)
            def watch_node(data, stat):
                ZK.set(PLAYER_PATH, 'updated')
        self.post_score()

    def post_score(self):
        while self.counter > 0:
            num = int(self.normal_distribution(self.mean, self.mean / 100, 0, self.up))
            value = str(num) + '+1'
            self.zk.set(self.path, value)
            print self.name + ' post score: ' + str(num)
            d = self.normal_distribution(self.delay, float(self.delay) / 10, 0, self.delay * 2)
            print 'delay ' + str(d) + ' s'
            print ''
            history, stat = self.zk.get(BOARD_PATH)
            self.zk.set(BOARD_PATH, history + '/' + self.name + '#' + value)
            time.sleep(d)
            self.counter -= 1
        print 'reach to maximum count for this player, exiting--'
        self.leave()

    def normal_distribution(self, mean=DEFAULT_MEAN, sd=10, low=0, upp=1000):
        return truncnorm((low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd).rvs()


if __name__ == "__main__":
    argv = sys.argv
    argv_len = len(argv)
    if argv_len  >= 3:
        counter = int(argv[3] if argv_len >= 4 else DEFAULT_COUNT)
        delay = float(argv[4] if argv_len >= 5 else DEFAULT_DELAY)
        mean = float(argv[5] if argv_len >= 6 else DEFAULT_MEAN)
        if counter < 0 or delay < 0 or mean < 0:
            print 'invalid negative input, exiting------'
            sys.exit()
        if mean > sys.maxsize - mean / 100:
            print 'exceed the maximum range, exiting-----'
            sys.exit()
        p = player(argv[1], argv[2], counter, delay, mean)
        p.check_and_go()
    else:
        print 'input at least IP and username'
