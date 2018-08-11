import sys
from flask import Flask
sys.path.insert(0,"/var/www/reviewer/src/node")
sys.path.append("/usr/local/lib/python3.7/site-packages")
sys.path.append("/var/www/reviewer/src")
from node import node_server
application = node_server.app
