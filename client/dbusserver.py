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
            self.parent.method_void(name)
        method.__name__ = str(name)
        print("Created func object " + str(method.__name__) + ": " + str(method))
        return method
    
    methods=dict()
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
            
        self.bussrv = get_dbus_service(self.bus, self.obj, self.interface, methods, props, self)()
        self.start()
        
    def run(self):
        self.bussrv.run()
    
    def emit_signal(self, signal, *data):
        pass
    
    def handle_properties_signal(*data):
        pass
    
    def method_void(self, name):
        self.netconn.call_method(name)