# -*- coding: utf-8 -*-
import traceback
from time import sleep

__author__ = 'terryyao'

import requests
import json
from pymongo import MongoClient

client = MongoClient(host='172.16.0.24', port=28018)
mongo_connect = client['blockchain']
mongo_connect.authenticate(name='hashpaydl', password='hsashpaydldr3')
eos_data = mongo_connect.eos_data
eos_config = mongo_connect.eos_config
ram = mongo_connect.eos_ram
eos_actions = mongo_connect.eos_actions

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
            eos_data.insert(x)

            for t in x.get('transactions'):
                try:
                    for a in t['trx']['transaction']['actions']:
                        a["block_id"] = x["id"]
                        a["timestamp"] = x["timestamp"]
                        a["trx_id"] = t['trx']["id"]
                        for key, value in a["data"].items():
                            a["data_" + key] = value
                        print(a)
                        eos_actions.save(a)
                except Exception as e:
                    pass

            try:
                for q in x.get('transactions'):
                    for a in q['trx']['transaction']['actions']:
                        if a['name'] == 'buyram':
                            ramDict = {}
                            ramDict["block_num"] = x['block_num']
                            ramDict["timestamp"] = x['timestamp']
                            ramDict["account"] = a['account']
                            ramDict["receiver"] = a['data']['receiver']
                            ramDict["payer"] = a['data']['payer']
                            quant = a['data']['quant']
                            if quant is not None and quant.isalnum():
                                ramDict["quant"] = quant.replace(" EOS","")
                            else:
                                ramDict["quant"] = quant
                            ramDict["ram_type"] = "buyram"
                            ram.save(ramDict)
                            print(ramDict)
            except Exception as e:
                exstr = traceback.format_exc()
                print(exstr)

            try:
                for q in x.get('transactions'):
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
                for q in x.get('transactions'):
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
    q = eos_data.find({"transactions.trx.transaction.actions.name": "buyram"})
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

    q = eos_data.find({"transactions.trx.transaction.actions.name": "buyrambytes"})
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

    q = eos_data.find({"transactions.trx.transaction.actions.name": "sellram"})
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

def dealEos():
    rams = ram.find({})
    for ram_object in rams:
        quant = ram_object["quant"]
        if quant is not None and quant.isalnum():
            ram_object["quant"] = quant.replace(" EOS", "")
        else:
            ram_object["quant"] = quant
        ram.save(ram_object)

def dealActions():
    eoss = eos_data.find({})
    for eos_object in eoss:
        for t in eos_object['transactions']:
            try:
                for a in t['trx']['transaction']['actions']:
                    a["block_id"] = eos_object["id"]
                    a["timestamp"] = eos_object["timestamp"]
                    for key, value in a["data"].items():
                        a["data_"+ key] = value
                    print(a)
                    eos_actions.save(a)
            except Exception as e:
                pass
if __name__ == '__main__':
    extractEosBlockData()
    # minerRam()
    # dealEos()
    # dealActions()