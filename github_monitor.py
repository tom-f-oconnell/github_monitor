#!/usr/bin/env python3

from feedgen.feed import FeedGenerator
import socketserver
import urllib.request
import hashlib
import json

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

def add_general_event(event, feed):
    """ Adds one GitHub event entry (dict read from JSON) to feed with generic information. """

    fe = feed.add_entry()
    fe.id(event['created_at'])
    fe.title(event['type'])
    desc = event['actor']['login'] + ' ' + event['created_at']
    fe.description(desc)
    #fe.enclosure('', 0, '')

def add_comment_event(event, feed):
    """ Adds richer information about the more interesting events (ones with comments). """
    
    fe = feed.add_entry()
    fe.id(event['created_at'])

    prefix = event['actor']['login'] + ' at ' + event['created_at']
    fe.title(prefix)
    desc = prefix + ': ' + event['payload']['comment']['body']

    fe.description(desc)
    #fe.enclosure('', 0, '')


def json2entries(data, feed):
    """ Takes a dict of urls -> JSON descriptions and adds the feed entries I want. """

    for url in data:
        for event in data[url]:
            if not event['type'] == 'IssueCommentEvent':
                add_general_event(event, feed)
            else:
                add_comment_event(event, feed)


class MyTCPServer(socketserver.TCPServer):
    """ To give some state that the stream handler can use. """

    def __init__(self, hostport_tuple, handler, data):

        super().__init__(hostport_tuple, handler)
        self.feed = init_feed()

        # populates the feed with the github events info
        json2entries(data, self.feed)

class MyStreamHandler(socketserver.StreamRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    # TODO can this class get info from its TCPServer?

    def handle(self):
        #fg = init_feed()
        fg = self.server.feed

        #json2entries(
        
        # get the rss feed as a string
        rssfeed = fg.rss_str(pretty=True)
        
        # self.wfile is a file-like object used to write back to the client
        self.wfile.write(rssfeed)

if __name__ == "__main__":
    
    with open('sites.txt', 'r') as f:
        urls = f.read().strip().split()

    url2hash = dict()
    hash2url = dict()
    
    for url in urls:
        url2hash[url] = hashlib.md5(url.encode('utf-8')).hexdigest()[:10]
        hash2url[url2hash[url]] = url
        urllib.request.urlretrieve(url, './data/' + url2hash[url])

    data = dict()

    for hsh in hash2url:
        with open('./data/' + hsh, 'r') as fp:
            data[hash2url[hsh]] = json.load(fp)
    
    host = True
    
    if host:
        HOST, PORT = "localhost", 9997
        
        # Create the server, binding to localhost on port 9999
        server = MyTCPServer((HOST, PORT), MyStreamHandler, data)

        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
    else:
        # Otherwise output to a file, which can be uploaded to hosting separately
        output = './rss'
        
