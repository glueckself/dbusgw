#!/usr/bin/env python2.7

import util
import server

import signal 
import sys

def signal_handler(signal, frame):
    print("Received CTRL+C, stopping...")
    server.stop()
    
signal.signal(signal.SIGINT, signal_handler)
server.start(util.dbusConf, util.netConf)
