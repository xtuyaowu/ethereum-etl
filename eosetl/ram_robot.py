# -*- coding: utf-8 -*-
__author__ = 'terryyao'
import traceback
from time import sleep
import requests
import json
from pymongo import MongoClient
import paramiko

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

def BuyRam():

	# 查询最新价格
	req = requests.get("https://tbeospre.mytokenpocket.vip/v1/ram_price")
	ram_price_dict = json.loads(req.text)
	real_time_price = 1*1024 / ram_price_dict["data"]

	# maxRam = br[0].rows[0].max_ram_size;
	# var ramBaseBalance = ar[0].rows[0].base.balance; // Amount of RAM bytes in use
	# var ramUsed = 1 - (ramBaseBalance - maxRam);
	# target = document.getElementById("maxRam");
	# target.innerHTML = (maxRam / 1024 / 1024 / 1024).toFixed(2) + " GB";
	# var ramUtilization = (ramUsed / maxRam) * 100;

	data_a = '{"json":"true","code":"eosio","scope":"eosio","table":"rammarket","limit":"10"}'
	body_a = requests.post("https://api.eosnewyork.io/v1/chain/get_table_rows", data=data_a)
	ar = json.loads(body_a.text)
	ramBaseBalance = int(ar["rows"][0]["base"]["balance"].replace(" RAM","")) # Amount of RAM bytes in use

	data_b = '{"json":"true","code":"eosio","scope":"eosio","table":"global"}'
	body_b = requests.post("https://api.eosnewyork.io/v1/chain/get_table_rows", data=data_b)
	br = json.loads(body_b.text)
	maxRam = int(br["rows"][0]["max_ram_size"]) # total Amount of RAM bytes
	maxRamGB = (maxRam / 1024 / 1024 / 1024)

	ramUsed = 1 - (ramBaseBalance - maxRam)
	ramUtilization = (ramUsed / maxRam) * 100

	if real_time_price>0.8:
		# wallet := "wallet name"
		# err := WalletLock(wallet)
		# fmt.Println("err: ", err)
		#
		# err_WalletOpen := WalletOpen(wallet)
		# fmt.Println("err: ", err_WalletOpen)
		#
		# err_WalletUnlock := WalletUnlock(wallet, "")
		# fmt.Println("err: ", err_WalletUnlock)

        # run remote shell
		transport = paramiko.Transport(('127.0.0.1', 22))
		transport.connect(username='root', password='pKx123456')
		ssh = paramiko.SSHClient()
		ssh._transport = transport
		stdin, stdout, stderr = ssh.exec_command('python /data/generate_password_hash.py SSHA512 ' + _passwd)
		sshresp = stdout.read()
		print(sshresp)

if __name__ == '__main__':
	BuyRam()