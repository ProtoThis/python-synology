# -*- coding:utf-8 -*-

import requests

    
# Define Static Variables


# Define Classes
class SynologyApi(object):
    def __init__(self, ip, port, username, password):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
