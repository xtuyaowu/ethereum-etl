import json
import traceback

from pymongo import MongoClient

from ethereumetl.exporters import CsvItemExporter
from ethereumetl.file_utils import get_file_handle, close_silently
from ethereumetl.jobs.batch_export_job import BatchExportJob
from ethereumetl.json_rpc_requests import generate_get_block_by_number_json_rpc
from ethereumetl.mappers.block_mapper import EthBlockMapper
from ethereumetl.mappers.transaction_mapper import EthTransactionMapper

BLOCK_FIELDS_TO_EXPORT = [
    'block_number',
    'block_hash',
    'block_parent_hash',
    'block_nonce',
    'block_sha3_uncles',
    'block_logs_bloom',
    'block_transactions_root',
    'block_state_root',
    'block_miner',
    'block_difficulty',
    'block_total_difficulty',
    'block_size',
    'block_extra_data',
    'block_gas_limit',
    'block_gas_used',
    'block_timestamp',
    'block_transaction_count'
]

TRANSACTION_FIELDS_TO_EXPORT = [
    'tx_hash',
    'tx_nonce',
    'tx_block_hash',
    'tx_block_number',
    'tx_index',
    'tx_from',
    'tx_to',
    'tx_value',
    'tx_gas',
    'tx_gas_price',
    'tx_input'
]

client = MongoClient(host='172.16.0.24', port=28018)
mongo_connect = client['blockchain']
mongo_connect.authenticate(name='hashpaydl', password='hsashpaydldr3')
blocks_exporter = mongo_connect.blocks_exporter
transactions_exporter = mongo_connect.transactions_exporter
eth_config = mongo_connect.eth_blockConfig

# Exports blocks and transactions
class ExportBlocksJob(BatchExportJob):
    def __init__(
            self,
            start_block,
            end_block,
            batch_size,
            ipc_wrapper,
            web3,
            max_workers=5,
            blocks_output=None,
            transactions_output=None,
            block_fields_to_export=BLOCK_FIELDS_TO_EXPORT,
            transaction_fields_to_export=TRANSACTION_FIELDS_TO_EXPORT):
        super().__init__(start_block, end_block, batch_size, max_workers)
        self.web3 = web3
        self.ipc_wrapper = ipc_wrapper
        self.blocks_output = blocks_output
        self.transactions_output = transactions_output
        self.block_fields_to_export = block_fields_to_export
        self.transaction_fields_to_export = transaction_fields_to_export

        self.export_blocks = blocks_output is not None
        self.export_transactions = transactions_output is not None
        # if not self.export_blocks and not self.export_transactions:
        #     raise ValueError('Either blocks_output or transactions_output must be provided')

        self.block_mapper = EthBlockMapper()
        self.transaction_mapper = EthTransactionMapper()

        self.blocks_output_file = None
        self.transactions_output_file = None

        self.blocks_exporter = None
        self.transactions_exporter = None

        self.start_block = start_block

    def _start(self):
        super()._start()

        # self.blocks_output_file = get_file_handle(self.blocks_output, binary=True, create_parent_dirs=True)
        # self.blocks_exporter = CsvItemExporter(
        #     self.blocks_output_file, fields_to_export=self.block_fields_to_export)
        #
        # self.transactions_output_file = get_file_handle(self.transactions_output, binary=True, create_parent_dirs=True)
        # self.transactions_exporter = CsvItemExporter(
        #     self.transactions_output_file, fields_to_export=self.transaction_fields_to_export)

    def _export_batch(self, batch_start, batch_end):
        blocks_rpc = list(generate_get_block_by_number_json_rpc(batch_start, batch_end, self.export_transactions))
        response = self.ipc_wrapper.make_request(json.dumps(blocks_rpc))
        for response_item in response:
            result = response_item['result']
            block = self.block_mapper.json_dict_to_block(result)
            self._export_block(block)

    def _export_block(self, block):
        # if self.export_blocks:
        #     self.blocks_exporter.export_item(self.block_mapper.block_to_dict(block))
        block_dict = self.block_mapper.block_to_dict(block)
        if blocks_exporter.find_one({"block_hash": block_dict['block_hash']}) is None:
            block_timestamp = block_dict["block_timestamp"]
            blocks_exporter.insert(block_dict)


            # if self.export_transactions:
            #     for tx in block.transactions:
            #         self.transactions_exporter.export_item(self.transaction_mapper.transaction_to_dict(tx))
            for tx in block.transactions:
                tx = self.transaction_mapper.transaction_to_dict(tx)
                if transactions_exporter.find_one({"tx_block_hash": tx['tx_block_hash']}) is None:
                    tx["timestamp"] = block_timestamp
                    receipt = self.web3.eth.getTransactionReceipt(tx.get("tx_hash"))
                    gasUsed = receipt.gasUsed
                    tx["status"] = 0
                    if int(gasUsed) <= int(tx.get("tx_gas")):
                        tx["status"] = 1  # 1 success
                    print(tx)
                    transactions_exporter.insert(tx)


    def _end(self):
        super()._end()
        # close_silently(self.blocks_output_file)
        # close_silently(self.transactions_output_file)
        blockConfig = eth_config.find_one({'config_id': 1})
        blockConfig["export_flag"] = False
        blockConfig["blockid"] = self.start_block
        eth_config.save(blockConfig)
