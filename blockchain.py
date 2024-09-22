# TODO: Implement blockchain class here

# Required block struct below
#INITIAL BLOCK =
#Prev_hash = 0, # 32 bytes 
#Timestamp = 0, # 08 bytes
#Case_id = b"0"*32, # 32 bytes (32 zero's) 
#Evidence_id = b"0"*32, # 32 bytes (32 zero's) 
#State = b"INITIAL\0\0\0\0\0", # 12 bytes
#creator = b"\0"*12, # 12 bytes (12 null bytes) 
#owner = b"\0"*12, # 12 bytes (12 null bytes) 
#D_length = 14, # 04 bytes
#Data = b"Initial block\0"

import os
from block import Block

class Blockchain:
    def __init__(self):
        self.chain = []
        self.load_blockchain()

    # Import blockchain data
    # Nab from environ
    # Add checks for absence of, or lack thereof, blocks here
    def load_blockchain(self):
        pass

    # Add an initial block if there is none
    def init_blockchain(self):
        pass

    # Append
    def add_block(self, block):
        pass

    # Verify the chain
    def verify(self):
        pass