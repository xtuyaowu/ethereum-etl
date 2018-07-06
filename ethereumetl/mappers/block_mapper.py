from ethereumetl.domain.block import EthBlock
from ethereumetl.mappers.transaction_mapper import EthTransactionMapper
from ethereumetl.utils import hex_to_dec, to_normalized_address


class EthBlockMapper(object):
    def __init__(self, transaction_mapper=None):
        if transaction_mapper is None:
            self.transaction_mapper = EthTransactionMapper()
        else:
            self.transaction_mapper = transaction_mapper

    def json_dict_to_block(self, json_dict):
        block = EthBlock()
        block.number = hex_to_dec(json_dict.get('number', None))
        block.hash = json_dict.get('hash', None)
        block.parent_hash = json_dict.get('parentHash', None)
        block.nonce = json_dict.get('nonce', None)
        block.sha3_uncles = json_dict.get('sha3Uncles', None)
        block.logs_bloom = json_dict.get('logsBloom', None)
        block.transactions_root = json_dict.get('transactionsRoot', None)
        block.state_root = json_dict.get('stateRoot', None)
        block.miner = to_normalized_address(json_dict.get('miner', None))
        block.difficulty = hex_to_dec(json_dict.get('difficulty', None))
        block.total_difficulty = hex_to_dec(json_dict.get('totalDifficulty', None))
        block.size = hex_to_dec(json_dict.get('size', None))
        block.extra_data = json_dict.get('extraData', None)
        block.gas_limit = hex_to_dec(json_dict.get('gasLimit', None))
        block.gas_used = hex_to_dec(json_dict.get('gasUsed', None))
        block.timestamp = hex_to_dec(json_dict.get('timestamp', None))

        if 'transactions' in json_dict:
            block.transactions = [
                self.transaction_mapper.json_dict_to_transaction(tx) for tx in json_dict['transactions']
                if isinstance(tx, dict)
            ]

            block.transaction_count = len(json_dict['transactions'])

        return block

    def block_to_dict(self, block):
        return {
            'block_number': str(block.number),
            'block_hash': str(block.hash),
            'block_parent_hash': str(block.parent_hash),
            'block_nonce': str(block.nonce),
            'block_sha3_uncles': str(block.sha3_uncles),
            'block_logs_bloom': str(block.logs_bloom),
            'block_transactions_root': str(block.transactions_root),
            'block_state_root': str(block.state_root),
            'block_miner': str(block.miner),
            'block_difficulty': str(block.difficulty),
            'block_total_difficulty': str(block.total_difficulty),
            'block_size': str(block.size),
            'block_extra_data': str(block.extra_data),
            'block_gas_limit': str(block.gas_limit),
            'block_gas_used': str(block.gas_used),
            'block_timestamp': str(block.timestamp),
            'block_transaction_count': str(block.transaction_count),
        }
