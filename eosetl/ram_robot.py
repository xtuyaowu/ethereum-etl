# -*- coding: utf-8 -*-
__author__ = 'terryyao'
import traceback
from time import sleep
import requests
import json
from pymongo import MongoClient
import paramiko

transport = paramiko.Transport(('127.0.0.1', 333))
transport.connect(username='root', password='123456')
ssh = paramiko.SSHClient()
ssh._transport = transport

def BuyRam():
    while True:
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

        if real_time_price < 0.4:
            # excuteSSHCommand('/root/pyworkspace/eos.sh walletlock wallet_name')
            # excuteSSHCommand('/root/pyworkspace/eos.sh walletunlock wallet_name private_key')
            excuteSSHCommand('/root/pyworkspace/eos.sh buyram https://mainnet.eoscanada.com account_name account_name 30')

        elif real_time_price > 0.5:
            # excuteSSHCommand('/root/pyworkspace/eos.sh walletlock wallet_name')
            # excuteSSHCommand('/root/pyworkspace/eos.sh walletunlock wallet_name private_key')
            excuteSSHCommand('/root/pyworkspace/eos.sh sellram https://mainnet.eoscanada.com account_name 30720')

        sleep(10)

def excuteSSHCommand(command):
    stdin, stdout, stderr = ssh.exec_command(command)
    sshresp = stdout.read()
    print(sshresp)
    stderrresp = stderr.read()
    print(stderrresp)

if __name__ == '__main__':
    BuyRam()
