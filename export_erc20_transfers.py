#!/usr/bin/env python3
import argparse
from time import sleep
import time
from pymongo import MongoClient
from web3 import IPCProvider, Web3, HTTPProvider

from ethereumetl.jobs.export_erc20_transfers_job import ExportErc20TransfersJob
from ethereumetl.thread_local_proxy import ThreadLocalProxy

# parser = argparse.ArgumentParser(
#     description='Exports ERC20 transfers using eth_newFilter and eth_getFilterLogs JSON RPC APIs.')
# parser.add_argument('-s', '--start-block', default=0, type=int, help='Start block')
# parser.add_argument('-e', '--end-block', required=True, type=int, help='End block')
# parser.add_argument('-b', '--batch-size', default=100, type=int, help='The number of blocks to filter at a time.')
# parser.add_argument('-o', '--output', default='-', type=str, help='The output file. If not specified stdout is used.')
# parser.add_argument('-w', '--max-workers', default=5, type=int, help='The maximum number of workers.')
# parser.add_argument('--ipc-path', required=True, type=str, help='The full path to the ipc socket file.')
# parser.add_argument('--ipc-timeout', default=300, type=int, help='The timeout in seconds for ipc calls.')
# parser.add_argument('-t', '--tokens', default=None, type=str, nargs='+',
#                     help='The list of token addresses to filter by.')

# args = parser.parse_args()

# job = ExportErc20TransfersJob(
#     start_block=args.start_block,
#     end_block=args.end_block,
#     batch_size=args.batch_size,
#     web3=ThreadLocalProxy(lambda: Web3(IPCProvider(args.ipc_path, timeout=args.ipc_timeout))),
#     output=args.output,
#     max_workers=args.max_workers,
#     tokens=args.tokens)
#
# job.run()

client = MongoClient(host='172.16.0.24', port=28018)
mongo_connect = client['blockchain']
mongo_connect.authenticate(name='hashpaydl', password='hsashpaydldr3')
eth_config = mongo_connect.eth_erc20_config
geth_ipc = "/home/dl/geth-alltools-linux-amd64-1.8.2-b8b9f7f4/chain/localchain/geth.ipc"
http_address = "http://127.0.0.1:8545"

def extractErc20BlockData():

    while True:
        blockConfig = eth_config.find_one({'config_id': 1})
        export_flag = blockConfig["export_flag"]
        if export_flag is False:
            blockid = blockConfig["blockid"]
            print(blockid)
            web3 = ThreadLocalProxy(lambda: Web3(IPCProvider(geth_ipc, timeout=300)))
            # web3 = ThreadLocalProxy(lambda: Web3(HTTPProvider(http_address)))
            blockidNow = web3.eth.blockNumber
            print(blockidNow)

            if blockidNow > blockid:
                blockConfig["export_flag"] = True
                blockid += 1
                blockConfig["blockid"] = blockid
                t = time.time()
                blockConfig['timestamp'] = int(round(t * 1000))
                eth_config.save(blockConfig)
                job = ExportErc20TransfersJob(
                    start_block=blockid,
                    end_block=blockidNow,
                    batch_size=100,
                    web3=ThreadLocalProxy(lambda: Web3(IPCProvider(geth_ipc, timeout=300))),
                    output="",
                    max_workers=1,
                    tokens=None)
                job.run()
        sleep(3)

if __name__ == '__main__':
    extractErc20BlockData()
