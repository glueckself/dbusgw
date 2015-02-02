import ConfigParser

def ConfigSectionMap(section):
    dict1 = {}
    options = config.options(section)
    for option in options:
        try:
            dict1[option] = config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

config = ConfigParser.ConfigParser()
config.read("dbusgw.conf")

dbusConf = ConfigSectionMap("dbus")
netConf = ConfigSectionMap("net")