#!/usr/bin/env python3
import argparse
from time import sleep

from pymongo import MongoClient
from web3 import IPCProvider, Web3

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

con = MongoClient('127.0.0.1', 27017)
eth_config = con.eth.eth_config
geth_ipc = "~/Library/Ethereum/geth.ipc"
def extractEosBlockData():

    while True:
        blockConfig = eth_config.find_one({'config_id': 1})
        export_flag = blockConfig["export_flag"]
        if export_flag is False:
            blockid = blockConfig["blockid"]
            print(blockid)
            web3 = ThreadLocalProxy(lambda: Web3(IPCProvider(geth_ipc, timeout=300)))
            blockidNow = web3.eth.blockNumber()
            if blockidNow > blockid:
                blockConfig["export_flag"] = True
                eth_config.save(blockConfig)

                blockid += 1
                job = ExportErc20TransfersJob(
                    start_block=blockid,
                    end_block=blockidNow,
                    batch_size=100,
                    web3=ThreadLocalProxy(lambda: Web3(IPCProvider(geth_ipc, timeout=300))),
                    output="",
                    max_workers=5,
                    tokens=None)
                job.run()
        sleep(3)

if __name__ == '__main__':

    job = ExportErc20TransfersJob(
        start_block=1,
        end_block=1000000,
        batch_size=100,
        web3=ThreadLocalProxy(lambda: Web3(IPCProvider("~/Library/Ethereum/geth.ipc", timeout=300))),
        output="",
        max_workers=5,
        tokens=None)

    job.run()