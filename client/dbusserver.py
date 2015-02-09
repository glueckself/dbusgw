#!/usr/bin/env python2.7

import dbus
import dbus.service
import json
import gobject
from dbus.mainloop.glib import DBusGMainLoop
from threading import Thread
import types

def get_dbus_service(bus, obj, interface, methodList, propList, parent):
    def __init__(self):
        self.bus_loop = DBusGMainLoop(set_as_default=True)
        self.bus_name = dbus.service.BusName(bus, bus=dbus.SessionBus(mainloop=self.bus_loop))
        dbus.service.Object.__init__(self,self.bus_name,obj)
        
        self.bus = bus
        self.obj = obj
        self.interface = interface
        self.parent = parent
        
        self.loop = gobject.MainLoop()
        self.method_list = list()
        
    def run(self):
        self.loop.run()
    
    def method_void_factory(name):
        def method(self):
            self.parent.call_method(name)
        method.__name__ = str(name)
        print("Created func object " + str(method.__name__) + ": " + str(method))
        return method

    def Get(self, interface_name, property_name):
        return self.parent.get_property(property_name)

    def GetAll(self, interface_name):
        res = dict()
        for prop in propList:
            res["prop"] = Get(interface_name, prop)
        return res

    def Set(self, interface_name, property_name, value):
        self.parent.set_property(property_name, str(value))
    
    methods=dict()
    
    methods["Get"] = dbus.service.method(interface=dbus.PROPERTY_INTERFACE, in_signature="ss" out_signature="v")(Get)
    methods["GetAll"] = dbus.service.method(interface=dbus.PROPERTY_INTERFACE, in_signature="s" out_signature="a(sv)")(GetAll)
    methods["Set"] = dbus.service.method(interface=dbus.PROPERTY_INTERFACE, in_signature="ssv" out_signataure="")(Set)
    
    for method in methodList:
        if '@arg' in method:
            print("Skipping " + str(method))
            continue
        else:
            print("Creating method " + method['@name'])
            methods[method['@name']]=dbus.service.method(interface)(method_void_factory(method['@name']))

    
    methods.update({'__init__':__init__, 'run':run})
    
    return type("GwDBusServerC", (dbus.service.Object,), methods);

class GwDBusServer(Thread):
    def __init__(self, bus, obj, interface):
        Thread.__init__(self)
        self.bus=bus
        self.obj=obj
        self.interface=interface
    
    def init(self, netconn, busmap):
        self.netconn = netconn
        if 'method' in busmap:
            methods=busmap['method']
        else:
            methods=None
            
        print("Methods: " + str(methods))
            
        if 'property' in busmap:
            props=busmap['property']
        else:
            props=None
            
        self.bussrv = get_dbus_service(self.bus, self.obj, self.interface, methods, props, self.netconn)()
        self.start()
        return self.bussrv
        
    def run(self):
        self.bussrv.run()
