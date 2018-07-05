# -*- coding: utf-8 -*-
import traceback
from time import sleep

__author__ = 'terryyao'

import requests
import json
from pymongo import MongoClient
from eosapi import Client

con = MongoClient('127.0.0.1', 27017)
eos = con.eos.eos
eos_config = con.eos.eos_config
ram = con.eos.ram
url_get_block = 'http://127.0.0.1:8888/v1/chain/get_block'
url_get_info = 'http://127.0.0.1:8888/v1/chain/get_info'


def createAccount():
    c = Client(nodes=['http://localhost:8888'])
    info = c.get_info()
    info_dict = json.loads(info)

if __name__ == '__main__':
    createAccount()
