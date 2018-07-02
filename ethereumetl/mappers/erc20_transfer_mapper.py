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
            'root': receipt.root,
            'to': receipt.to,
            'transactionHash': receipt.transactionHash,
            'transactionIndex': receipt.transactionIndex
        }