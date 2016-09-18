#!/usr/bin/env python3

import re
import socketserver
from feedgen.feed import FeedGenerator

def init_feed():
    fg = FeedGenerator()

    fg.id('http://eftm.duckdns.org/rss/')
    fg.title('Test feed')
    fg.author({'name': '', 'email': 'yeemail@yup.hom'} )
    # not sure what 'alternate' does?
    fg.link(href='http://eftm.duckdns.org', rel='alternate')
    fg.link( href='http://eftm.duckdns.org/rss', rel='self')
    fg.language('en')
    fg.description('Null')

    return fg


class MyStreamHandler(socketserver.StreamRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        fg = init_feed()
        
        # get the rss feed as a string
        rssfeed = fg.rss_str(pretty=True)
        
        # self.wfile is a file-like object used to write back to the client
        self.wfile.write(rssfeed)

if __name__ == "__main__":
    host = True
    
    if host:
        HOST, PORT = "localhost", 9998
        
        # Create the server, binding to localhost on port 9999
        server = socketserver.TCPServer((HOST, PORT), MyStreamHandler)

        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
    else:
        # Otherwise output to a file, which can be uploaded to hosting separately
        output = './rss'
        
