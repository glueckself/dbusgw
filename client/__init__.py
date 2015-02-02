from dbusserver import GwDBusServer
from netclient import GwNetClient

def start(dbusConf, netConf):
    gw_dbus = GwDBusServer(dbusConf['busname'], dbusConf['path'], dbusConf['interface'])
    gw_net = GwNetClient(netConf['host'], netConf['port'], gw_dbus)
    
    gw_net.start()
    
    
def stop():
    pass

if __name__ == '__main__':
    start(None, None)