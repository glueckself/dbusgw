#!/usr/bin/env python2.7

import dbus
import gobject
from dbus.mainloop.glib import DBusGMainLoop
from threading import Thread
import xmltodict

class GwDBusClient(Thread):
    def __init__(self, bus, obj, interface, callback):
        Thread.__init__(self)
        gobject.threads_init()
        
        self.bus = bus
        self.obj = obj
        self.interface = interface
        self.callback = callback
        
        self.bus_loop = DBusGMainLoop(set_as_default=True)
        self.bus = dbus.SessionBus(mainloop=self.bus_loop)
        self.loop = gobject.MainLoop()
        
        self.destObj = self.bus.get_object(bus, obj)
        self.destObjMethods = dbus.Interface(self.destObj, interface)
        self.properties_manager = dbus.Interface(self.destObj, 'org.freedesktop.DBus.Properties')
        
        self.bus.add_signal_receiver(self.signal_receiver, path=obj, bus_name=bus, interface_keyword='interface', member_keyword='member')
        
    def run(self):
        self.loop.run()
    
    def signal_receiver(self, *args, **kwargs):
        if(self.callback):
            self.callback(kwargs['member'], args[1])
    
    def call_method(self, method, *args):
        if method == ":SET":
            return self.set_property(args[0], args[1], args[2])
        elif method == ":GET":
            return self.get_property(args[0])
        
        method = self.destObjMethods.get_dbus_method(method, self.interface)
        return method()
    
    def get_property(self, prop):
        return self.properties_manager.Get(self.interface, prop)
    
    def set_property(self, propType, prop, data):
        self.properties_manager.Set(self.interface, prop, castType(propType,data))
    
    def castType(propType, data):
        if propType == "d":
            return int(data)
        if propType == "s":
            return str(data)
        if propType == "b":
            return bool(data)
    
    def introspect(self):
        busData = xmltodict.parse(self.destObj.Introspect())
        for interf in busData['node']['interface']:
            if interf['@name'] == self.interface:
                return interf