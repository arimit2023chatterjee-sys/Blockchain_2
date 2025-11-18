# blockchain.py
import hashlib
import json
import time

class Transaction:
    def __init__(self, from_address, to_address, amount):
        self.from_address = from_address
        self.to_address = to_address
        self.amount = float(amount)

class Block:
    def __init__(self, index, transactions, previous_hash):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": [vars(tx) for tx in self.transactions],
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def mine(self, difficulty=4):
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.compute_hash()

class SimpleBlockchain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.create_genesis()

    def create_genesis(self):
        genesis_tx = Transaction("system", "alice", 1000)
        genesis = Block(0, [genesis_tx], "0")
        genesis.mine()
        self.chain.append(genesis)

    def add_transaction(self, tx):
        self.pending_transactions.append(tx)

    def mine_pending(self):
        if not self.pending_transactions:
            return None
        block = Block(
            len(self.chain),
            self.pending_transactions.copy(),
            self.chain[-1].hash
        )
        block.mine()
        self.chain.append(block)
        self.pending_transactions = []
        return block

    def get_chain_data(self):
        return [{
            "index": b.index,
            "hash": b.hash,
            "previous_hash": b.previous_hash,
            "timestamp": b.timestamp,
            "nonce": b.nonce,
            "transactions": [vars(tx) for tx in b.transactions]
        } for b in self.chain]

# Global instance
blockchain = SimpleBlockchain()
