#!/usr/bin/env python3

import re
import socketserver
from feedgen.feed import FeedGenerator

class MyStreamHandler(socketserver.StreamRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):

        print('Handling request')
          
        # self.request is the TCP socket connected to the client
        # self.data = self.request.recv(1024).strip()
        
        # self.data = self.rfile.readline.strip()
        # print("{} wrote:".format(self.client_address[0]))
        # print(self.data)

        fg = FeedGenerator()
        # won't print out anything at all. kind of strange
        dir(fg)

        # ?
        fg.id('http://eftm.duckdns.org/rss/')
        fg.title('Test feed')
        fg.author({'name': '', 'email': 'yeemail@yup.hom'} )
        # not sure what 'alternate' does?
        fg.link(href='http://eftm.duckdns.org', rel='alternate')
        # ?
        fg.link( href='http://eftm.duckdns.org/rss', rel='self')
        fg.language('en')
        fg.description('Null')

        # get the rss feed as a string
        rssfeed = fg.rss_str(pretty=True)
        print(rssfeed)
        
        # Likewise, self.wfile is a file-like object used to write back
        # to the client
        print(dir(self))
        self.wfile.write(rssfeed)

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999

    server = socketserver.TCPServer((HOST, PORT), MyStreamHandler)
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C

    server.serve_forever()
