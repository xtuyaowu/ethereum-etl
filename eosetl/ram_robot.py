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

def BuyRam():
    # 查询最新价格
    req = requests.get("https://tbeospre.mytokenpocket.vip/v1/ram_price")
    ram_price_dict = json.loads(req.text)
    real_time_price = 1 * 1024 / ram_price_dict["data"]

    # maxRam = br[0].rows[0].max_ram_size;
    # var ramBaseBalance = ar[0].rows[0].base.balance; // Amount of RAM bytes in use
    # var ramUsed = 1 - (ramBaseBalance - maxRam);
    # target = document.getElementById("maxRam");
    # target.innerHTML = (maxRam / 1024 / 1024 / 1024).toFixed(2) + " GB";
    # var ramUtilization = (ramUsed / maxRam) * 100;

    data_a = '{"json":"true","code":"eosio","scope":"eosio","table":"rammarket","limit":"10"}'
    body_a = requests.post("https://api.eosnewyork.io/v1/chain/get_table_rows", data=data_a)
    ar = json.loads(body_a.text)
    ramBaseBalance = int(ar["rows"][0]["base"]["balance"].replace(" RAM", ""))  # Amount of RAM bytes in use

    data_b = '{"json":"true","code":"eosio","scope":"eosio","table":"global"}'
    body_b = requests.post("https://api.eosnewyork.io/v1/chain/get_table_rows", data=data_b)
    br = json.loads(body_b.text)
    maxRam = int(br["rows"][0]["max_ram_size"])  # total Amount of RAM bytes
    maxRamGB = (maxRam / 1024 / 1024 / 1024)
    print(maxRamGB)

    ramUsed = 1 - (ramBaseBalance - maxRam)
    ramUtilization = (ramUsed / maxRam) * 100

    if real_time_price < 0.8:

        transport = paramiko.Transport(('10.8.42.153', 22))
        transport.connect(username='yaowu', password='12345678')
        ssh = paramiko.SSHClient()
        ssh._transport = transport

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
        stdin, stdout, stderr = ssh.exec_command('sh /home/yaowu/eos.sh getinfo http://10.8.42.153:8888')
        sshresp = stdout.read()
        print(sshresp)

if __name__ == '__main__':
    BuyRam()