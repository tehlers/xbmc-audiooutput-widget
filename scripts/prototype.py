#! /usr/bin/env python

"""prototype.py: Toggle the audio output of a raspbmc between HDMI and analog output
 Options:
  -h, --host
  -p, --password
  -u, --username"""

import base64
import getopt
import json
import sys
import urllib
import urllib2

AUDIO_TOGGLE_DIGITAL = urllib.quote_plus( '{ "jsonrpc" : "2.0", "method" : "Input.ExecuteAction", "params" : { "action" : "audiotoggledigital" }, "id" : 1 }' )

def toggleAudioOutput( host, username, password ):
    json_command = AUDIO_TOGGLE_DIGITAL
    url = 'http://%s/jsonrpc?request=%s' % ( host, json_command )
    request = urllib2.Request( url )
    authorization = base64.encodestring( '%s:%s' % ( username, password ) ).replace( '\n', '' )
    request.add_header( 'Authorization', 'Basic %s' % authorization )   
    request.add_header( 'Content-Type', 'application/json' )   
    response = urllib2.urlopen( request )
    print response.read()

def usage():
    print __doc__

def main( argv ):
    host = None
    password = None
    username = None

    try:
        opts, args = getopt.getopt( argv, 'h:p:u:', [ 'host=', 'password=', 'username=' ] )
    except getopt.GetoptError:
        usage()
        sys.exit( 2 )

    for opt, arg in opts:
        if ( opt in ( '-h', '--host' ) ):
            host = arg
        elif ( opt in ( '-p', '--password' ) ):
            password = arg
        elif ( opt in ( '-u', '--username' ) ):
            username = arg

    if ( not all( ( host, password, username ) ) ):
        usage()
        sys.exit( 2 )

    toggleAudioOutput( host, username, password )

if __name__ == '__main__':
   main( sys.argv[1:] )
