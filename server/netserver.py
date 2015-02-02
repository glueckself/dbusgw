import socket
import sys
import json
from threading import Thread

class GwNetClientHandler(Thread):
    def __init__(self, sock, addr, method, disconnect):
        Thread.__init__(self)
        self.sock = sock
        self.method = method
        self.addr = addr
        self.disconnect = disconnect
        
    def run(self):
        try:
            while True:
                inbuf = self.sock.recv(2048)
                if not inbuf:
                    self.disconnect(self)
                    return
                
                cmd = inbuf[0:4]
                data = inbuf[4:].rstrip()
                
                if cmd == "meth":
                    resp=self.method(data)
                elif cmd == "pros":
                    propType = data[0:1]
                    prop = data[1:].split("=")
                    self.method(":SET", propType, prop[0], prop[1])
                    resp="OK"
                elif cmd == "prog":
                    resp=self.method(":GET", data)
                self.sock.send("resp"+str(resp)+"\n")
          
        except:
              print("Error in client " + str(self.addr)+ ": " +str(sys.exc_info()))
              self.disconnect(self)
    
    def signal_callback(self, data):
        self.sock.send("sign"+data+"\n")
        
    def close(self):
        print("Closing connection to " + str(self.addr))
        self.sock.close()

class GwNetServer(Thread):
    def __init__(self, host, port, method, bus_introspection):
        Thread.__init__(self)
        
        if not port:
            port=5005
        if not host:
            host=''
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((host, int(port)))
        print("Listening on " + host + ":" +port)
        
        self.clientList = list()
        self.method = method
        self.bus_introspection = json.dumps(bus_introspection)
        
    def run(self):
        self.sock.listen(5)
        print("Server online")
        while True:
            clSock, addr = self.sock.accept()
            print("New client: " + str(addr))
            clSock.send("init"+self.bus_introspection+"\n")
            
            clientHandler = GwNetClientHandler(clSock, addr, self.method, self.disconnectClient)
            clientHandler.start()
            self.clientList.append(clientHandler)
        print("Server offline")
            
    def disconnectClient(self, client):
        client.close()
        self.clientList.remove(client)
            
    def signal_callback(self, signal, data):
        text=str(signal)+str(json.dumps(data))
        for client in self.clientList:
            try:
                client.signal_callback(text)
            except:
                print("Could not reach client, removing")
                self.disconnectClient(client)
    
    def stop(self):
        self.sock.close()
