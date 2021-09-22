#  coding: utf-8 
from os import DirEntry
import socketserver
from os import path

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

# Copyright 2021 Shiyu Xiu
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
class MyWebServer(socketserver.BaseRequestHandler):
    def handle(self):
        self.base_url = "http://127.0.0.1:8080"
        self.response = "HTTP/1.1 "#response message and reinitilize every time
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
       # self.request.sendall(bytearray("OK",'utf-8'))
        if len(self.data)>0:
           self.get()
        #print("data is "+self.response)
        self.request.sendall(bytearray(self.response,'utf-8'))
    def check_legal_path(self,dir):
        p = path.normpath("www" + dir)#nomalize the path
        #print(p+"\n")
        #print(path.exists(p) and ("www" in p))
        return path.exists(p) and ("www" in p);#handle the unsecure case  

    def get(self):
        #parse the request data into list
        data_list = self.data.decode("utf-8").split(" ")
        method = data_list[0]
        directory = data_list[1]
        if method == "GET":
            if directory[-1] == '/':#with slash
                #handle the root html file
                if self.check_legal_path(directory):
                    if path.isfile("www"+directory):
                        file_type =directory.split(".")[-1]
                        if file_type == "html":
                            self.response+="200 OK\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n"
                            file = open("www" + directory)
                            for line in file:
                                self.response += line + "\r\n"
                            file.close()
                        elif file_type == "css":
                            self.response += "200 OK\r\nContent-Type: text/css; charset=UTF-8\r\n\r\n"
                            css_file = open("www"+directory)
                            for line in css_file:
                                self.response += line + "\r\n"
                            css_file.close()
                        else:
                            #serve other file
                            self.response += "200 OK\r\nContent-Type: application/octet-stream; charset=UTF-8\r\n\r\n"
                            f = open("www"+directory)
                            for line in f:
                                self.response += line + "\r\n"
                            f.close()

                    else:
                        self.response+="200 OK\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n"
                        file = open("www"+directory+"index.html")
                        for line in file:
                            self.response += line + "\r\n"
                        file.close()
                else:
                    self.response+="404 Not Found\r\n" 
            else:#without slash
                if self.check_legal_path(directory):#path is legal
                    if path.isfile("www"+directory):#the directory leads to a file
                        file_type =directory.split(".")[-1]
                        if file_type == "html":
                            self.response+="200 OK\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n"
                            file = open("www" + directory)
                            for line in file:
                                self.response += line + "\r\n"
                            file.close()
                        elif file_type == "css":
                            self.response += "200 OK\r\nContent-Type: text/css; charset=UTF-8\r\n\r\n"
                            css_file = open("www"+directory)
                            for line in css_file:
                                self.response += line + "\r\n"
                            css_file.close()
                        else:
                             #serve other file
                            self.response += "200 OK\r\nContent-Type: application/octet-stream; charset=UTF-8\r\n\r\n"
                            f = open("www"+directory)
                            for line in f:
                                self.response += line + "\r\n"
                            f.close()
                    else:
                        self.response += "301 Moved Permanently\r\n" + "Location: " + self.base_url + directory + "/\r\n"
                else:
                    self.response+="404 Not Found\r\n" 
        else:
            self.response+="405 Method Not Allowed\r\n"


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
