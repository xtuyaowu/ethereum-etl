#!/usr/bin/env python3
import argparse
import time
from pymongo import MongoClient
from web3 import IPCProvider, Web3, HTTPProvider

from ethereumetl.ipc import IPCWrapper
from ethereumetl.jobs.export_blocks_job import ExportBlocksJob
from ethereumetl.thread_local_proxy import ThreadLocalProxy

# parser = argparse.ArgumentParser(description='Export blocks and transactions.')
# parser.add_argument('-s', '--start-block', default=0, type=int, help='Start block')
# parser.add_argument('-e', '--end-block', required=True, type=int, help='End block')
# parser.add_argument('-b', '--batch-size', default=100, type=int, help='The number of blocks to export at a time.')
# parser.add_argument('--ipc-path', required=True, type=str, help='The full path to the ipc file.')
# parser.add_argument('--ipc-timeout', default=300, type=int, help='The timeout in seconds for ipc calls.')
# parser.add_argument('-w', '--max-workers', default=5, type=int, help='The maximum number of workers.')
# parser.add_argument('--blocks-output', default=None, type=str,
#                     help='The output file for blocks. If not provided blocks will not be exported. '
#                          'Use "-" for stdout')
# parser.add_argument('--transactions-output', default=None, type=str,
#                     help='The output file for transactions. If not provided transactions will not be exported. '
#                          'Use "-" for stdout')
#
# args = parser.parse_args()
#
# job = ExportBlocksJob(
#     start_block=args.start_block,
#     end_block=args.end_block,
#     batch_size=args.batch_size,
#     ipc_wrapper=ThreadLocalProxy(lambda: IPCWrapper(args.ipc_path, timeout=args.ipc_timeout)),
#     max_workers=args.max_workers,
#     blocks_output=args.blocks_output,
#     transactions_output=args.transactions_output)
#
# job.run()

client = MongoClient(host='172.16.0.24', port=28018)
mongo_connect = client['blockchain']
mongo_connect.authenticate(name='hashpaydl', password='hsashpaydldr3')
eth_config = mongo_connect.eth_blockConfig
geth_ipc = "/home/dl/geth-alltools-linux-amd64-1.8.2-b8b9f7f4/chain/localchain/geth.ipc"
http_address = "http://127.0.0.1:8545"


def extractBlockData():

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
                job = ExportBlocksJob(
                    start_block=blockid,
                    end_block=blockidNow,
                    batch_size=100,
                    ipc_wrapper=ThreadLocalProxy(lambda: IPCWrapper(geth_ipc, timeout=300)),
                    web3=ThreadLocalProxy(lambda: Web3(IPCProvider(geth_ipc, timeout=300))),
                    max_workers=5,
                    blocks_output="",
                    transactions_output="")

                job.run()
        time.sleep(3)

if __name__ == '__main__':
    extractBlockData()