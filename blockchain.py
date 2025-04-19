import hashlib
import json
import time

class Blockchain:
    def __init__(self):  # ✅ Fixed constructor
        self.chain = []  # Initialize the chain
        self.create_genesis_block()  # Create the genesis block when initializing

    def create_genesis_block(self):
        # The first block in the chain, known as the Genesis block
        genesis_block = self.create_block(data="Genesis Block", previous_hash="0")
        self.chain.append(genesis_block)  # Append it to the chain

    def create_block(self, data, previous_hash):
        # Create a new block using the given data and the previous block's hash
        block = {
            "index": len(self.chain),
            "timestamp": time.time(),
            "data": data,
            "previous_hash": previous_hash,
        }
        block["hash"] = self.hash(block)
        return block

    def add_block(self, data):
        last_block = self.chain[-1]
        new_block = self.create_block(data, last_block["hash"])
        self.chain.append(new_block)

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            curr = self.chain[i]
            prev = self.chain[i - 1]
            if curr["previous_hash"] != prev["hash"]:
                return False
            if curr["hash"] != self.hash(curr):
                return False
        return True

    def save_chain(self, filename="search_blockchain.json"):
        with open(filename, "w") as f:
            json.dump(self.chain, f, indent=4)

    def load_chain(self, filename="search_blockchain.json"):
        try:
            with open(filename, "r") as f:
                self.chain = json.load(f)
        except FileNotFoundError:
            self.chain = []
