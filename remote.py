#import config
import os
import paramiko
import re
import unittest
import pip
import logging
#import vagrant

#from util.parser import OutputStr
from requests.packages.urllib3.exceptions import InsecureRequestWarning

try:
    import requests
except ImportError:
    pip.main(['install', 'requests'])
    import requests

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('crosstest.log')
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

serverip="10.84.2.164"

class Server(object):
    addition_info = None

    def __init__(self):


        parameters = {"username": "administrator", "password": "password"}
        response = self.webapi("post", "login", parameters)
        response_obj = response["response"].json()
        self.addition_info = response_obj[0]

        # logger.debug("addition_info = %s" % self.addition_info)



    def webapi(self, method, service, parameters=None):
        url = "https://"+serverip+"/service/" + service
        header = dict()
        header["Content-Type"] = "application/json"
        header["additioninfo"] = self.addition_info
        returninfo=dict()
        requests_function = getattr(requests, method)

        response = requests_function(url, json=parameters, headers=header, verify=False)


        returninfo["request"] = response.request
        returninfo["headers"] = response.headers
        returninfo["url"] = response.url
        returninfo["text"] = response.text
        returninfo["parameters"] = parameters
        returninfo["response"] = response
        try:
            if response.text != "":
                setattr(response, "data", response.json())
        except:
            raise AssertionError(response.text)

        return returninfo

    def webapiurl(self, method, service, urlparameter):
        url = "https://" + serverip + "/service/" + service+urlparameter
        header = dict()
        header["Content-Type"] = "application/json"
        header["additioninfo"] = self.addition_info
        returninfo = dict()
        requests_function = getattr(requests, method)
        response = requests_function(url, headers=header, verify=False)


        returninfo["request"] = response.request
        returninfo["headers"] = response.headers
        returninfo["url"] = response.url
        returninfo["text"] = response.text
        returninfo["parameters"] = urlparameter
        returninfo["response"] = response
        try:
            if response.text != "":
                setattr(response, "data", response.json())
        except:
            raise AssertionError(response.text)

        return returninfo

#
server = Server()

