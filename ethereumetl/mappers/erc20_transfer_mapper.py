import traceback


class EthErc20TransferMapper(object):
    def erc20_transfer_to_dict(self, erc20_transfer):
        return {
            'erc20_token': erc20_transfer.erc20_token,
            'erc20_from': erc20_transfer.erc20_from,
            'erc20_to': erc20_transfer.erc20_to,
            'erc20_value': erc20_transfer.erc20_value,
            'erc20_tx_hash': erc20_transfer.erc20_tx_hash,
            'erc20_log_index': erc20_transfer.erc20_log_index,
            'erc20_block_number': erc20_transfer.erc20_block_number,
        }

    def erc20_receipt_transfer_to_dict(self, receipt):

        return {
            'blockHash': receipt.blockHash,
            'blockNumber': receipt.blockNumber,
            'contractAddress': receipt.contractAddress,
            'cumulativeGasUsed': receipt.cumulativeGasUsed,
            'gasUsed': receipt.gasUsed,
            'logs': receipt.logs,
            'logsBloom': receipt.logsBloom,
            'root': receipt.root if hasattr(receipt, 'root') else None,
            'to': receipt.to,
            'transactionHash': receipt.transactionHash,
            'transactionIndex': receipt.transactionIndex,
            'status':receipt.status if hasattr(receipt, 'status') else None,
        }

    def transaction_to_dict(self, transaction):
        return {
            'blockHash': transaction.blockHash,
            'blockNumber': transaction.blockNumber,
            'gas': transaction.gas,
            'gasPrice': transaction.gasPrice,
            'input': transaction.input,
            'nonce': transaction.nonce,
            'to': transaction.to,
            'transactionIndex': transaction.transactionIndex
        }