# -*- coding: utf-8 -*-
import traceback
from time import sleep

__author__ = 'terryyao'

import requests
import json
from pymongo import MongoClient

con = MongoClient('127.0.0.1', 27017)
eos = con.eos.eos
eos_config = con.eos.eos_config
ram = con.eos.ram
url_get_block = 'http://127.0.0.1:8888/v1/chain/get_block'
url_get_info = 'http://127.0.0.1:8888/v1/chain/get_info'

def extractEosBlockData():

    while True:
        blockConfig = eos_config.find_one({'config_id':1})
        blockid = blockConfig["blockid"]
        print(blockid)
        r = requests.post(url_get_info, timeout=20)
        j = json.loads(r.text)
        blockidNow = j["head_block_num"]

        while blockidNow > blockid:
            blockid += 1
            payload = {'block_num_or_id': blockid, }
            r = requests.post(url_get_block, data=json.dumps(payload), timeout=20)
            x = json.loads(r.text)
            eos.insert(x)
            try:
                for q in x['transactions']:
                    for a in q['trx']['transaction']['actions']:
                        if a['name'] == 'buyram':
                            ramDict = {}
                            ramDict["block_num"] = x['block_num']
                            ramDict["timestamp"] = x['timestamp']
                            ramDict["account"] = a['account']
                            ramDict["receiver"] = a['data']['receiver']
                            ramDict["payer"] = a['data']['payer']
                            ramDict["quant"] = a['data']['quant']
                            ramDict["ram_type"] = "buyram"
                            ram.save(ramDict)
                            print(ramDict)
            except Exception as e:
                exstr = traceback.format_exc()
                print(exstr)

            try:
                for q in x['transactions']:
                    for a in q['trx']['transaction']['actions']:
                        if a['name'] == 'buyrambytes':
                            ramDict = {}
                            ramDict["block_num"] = x['block_num']
                            ramDict["timestamp"] = x['timestamp']
                            ramDict["account"] = a['account']
                            ramDict["receiver"] = a['data']['receiver']
                            ramDict["payer"] = a['data']['payer']
                            ramDict["quant"] = a['data']['bytes']
                            ramDict["ram_type"] = "buyrambytes"
                            ram.save(ramDict)
                            print(ramDict)
            except Exception as e:
                exstr = traceback.format_exc()
                print(exstr)

            try:
                for q in x['transactions']:
                    for a in q['trx']['transaction']['actions']:
                        if a['name'] == 'sellram':
                            ramDict = {}
                            ramDict["block_num"] = x['block_num']
                            ramDict["timestamp"] = x['timestamp']
                            ramDict["account"] = a['account']
                            ramDict["receiver"] = a['data']['account']
                            ramDict["quant"] = a['data']['bytes']
                            ramDict["payer"] = a['authorization'][0]['actor']
                            ramDict["ram_type"] = "sellram"
                            ram.save(ramDict)
                            print(ramDict)
            except Exception as e:
                exstr = traceback.format_exc()
                print(exstr)

        blockConfig["blockid"] = blockid
        eos_config.save(blockConfig)
        sleep(3)

def minerRam():
    q = eos.find({"transactions.trx.transaction.actions.name": "buyram"})
    cnt = 0
    for x in q:
        for t in x['transactions']:
            try:
                for a in t['trx']['transaction']['actions']:
                    if a['name'] == 'buyram':
                        ramDict = {}
                        ramDict["block_num"] = x['block_num']
                        ramDict["timestamp"] = x['timestamp']
                        ramDict["account"] = a['account']
                        ramDict["receiver"] = a['data']['receiver']
                        ramDict["payer"] = a['data']['payer']
                        ramDict["quant"] =a['data']['quant']
                        ramDict["ram_type"] = "buyram"
                        ram.save(ramDict)
                        print(ramDict)
                        cnt += 1
            except Exception as e:
                exstr = traceback.format_exc()
                print(exstr)
                pass

    q = eos.find({"transactions.trx.transaction.actions.name": "buyrambytes"})
    cnt = 0
    for x in q:
        for t in x['transactions']:
            try:
                for a in t['trx']['transaction']['actions']:
                    if a['name'] == 'buyrambytes':
                        ramDict = {}
                        ramDict["block_num"] = x['block_num']
                        ramDict["timestamp"] = x['timestamp']
                        ramDict["account"] = a['account']
                        ramDict["receiver"] = a['data']['receiver']
                        ramDict["payer"] = a['data']['payer']
                        ramDict["quant"] = a['data']['bytes']
                        ramDict["ram_type"] = "buyrambytes"
                        ram.save(ramDict)
                        print(ramDict)
                        cnt += 1
            except Exception as e:
                exstr = traceback.format_exc()
                print(exstr)
                pass

    q = eos.find({"transactions.trx.transaction.actions.name": "sellram"})
    cnt = 0
    for x in q:
        for t in x['transactions']:
            try:
                for a in t['trx']['transaction']['actions']:
                    if a['name'] == 'sellram':
                        ramDict = {}
                        ramDict["block_num"] = x['block_num']
                        ramDict["timestamp"] = x['timestamp']
                        ramDict["account"] = a['account']
                        ramDict["receiver"] = a['data']['account']
                        ramDict["quant"] = a['data']['bytes']
                        ramDict["payer"] = a['authorization'][0]['actor']
                        ramDict["ram_type"] = "sellram"
                        ram.save(ramDict)
                        print(ramDict)
                        cnt += 1
            except Exception as e:
                exstr = traceback.format_exc()
                print(exstr)
                pass

if __name__ == '__main__':
    extractEosBlockData()
    # minerRam()