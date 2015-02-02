from dbusclient import GwDBusClient
from netserver import GwNetServer
import sys
import socket

gw_server=None
gw_dbus=None

def start(dbusConf, netConf):
    def signal_callback(signal, data):
        gw_server.signal_callback(signal, data)

    print("Creating dbus...")
    gw_dbus = GwDBusClient(dbusConf['busname'], dbusConf['path'], dbusConf['interface'], signal_callback)

    print("Creating server...")
    try:
        gw_server = GwNetServer(netConf['host'], netConf['port'], gw_dbus.call_method, gw_dbus.introspect())
    except socket.error as err:
        print("Failed to start server: " + str(err))
        sys.exit(1)
        
    gw_dbus.start()
    gw_server.start()
    
    gw_server.join()

def stop():
    gw_dbus.stop()
    gw_server.stop()