import socket
import sys
from threading import Thread
import json

class GwNetClient(Thread):
    def __init__(self, host, port, dbus):
        Thread.__init__(self)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((str(host), int(port)))
        self.dbus = dbus
        
    def run(self):
        dbusInit = self.sock.recv(4092)
        if dbusInit[0:4] == "init":
            self.dbus.init(self, json.loads(dbusInit[4:]))
        else:
            print("Invalid init command: " + dbusInit[0:4])
            return
        
        while True:
            data = self.sock.recv(4092)
            
    def call_method(self, name):
        self.sock.send("meth"+name)
    
    def set_property(self, propType, prop, value):
        self.sock.send("pros"+propType+prop+"="+value)
    
    def emit_signal(self, signal):
        pass

        