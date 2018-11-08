#!user/bin/env python3

#def application(environ, start_response):
#    status = '200 OK'
#    output = b'Hello Udacity!'

#    response_headers = [('Content-type', 'text/plain'), ('Content-Length', str(len(output)))]
#    start_response(status, response_headers)

#    return [output]

import sys
sys.path.insert(0, "/var/www/html/server/itemCatalog")

from itemCatalog import app as application
