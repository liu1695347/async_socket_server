#!/usr/bin python
#-*- coding:utf-8 -*-
#!/usr/bin/env python
#
# -*- coding:utf-8 -*-
# File: async_socket_server.py
#
import time
import random
import traceback
import threading
import SocketServer


class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        try:
            data = self.request.recv(1024)
            cur_thread = threading.current_thread()
            print "data: ", data, cur_thread
            while True:
                time.sleep(0.5)
                self.request.send(random.randint(0, 100))
        except:
            traceback.print_exc()
            print "client close"

    def finish(self):
        self.request.close()
        print "close.........."


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = "localhost", 9873

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address

    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    server.serve_forever()
    #server.shutdown()
