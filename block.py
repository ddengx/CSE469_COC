# (TODO) Block class for the blockchain

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

# Block data MUST be in binary

import struct

class Block:
    # Block size constant (cannot exceed)
    BLOCK_SIZE = 144

    # Block data attributes
    def __init__(self, prevHash, timestamp, caseID, evidenceID, state, creator, owner, D_length, data):
        self.prevHash = prevHash
        self.timestamp = timestamp
        self.caseID = caseID
        self.evidenceID = evidenceID
        self.state = state
        self.creator = creator
        self.owner = owner
        self.data = data
        self.D_length = len(data)

    # (TODO) Possible implementation is to pack data into a struct to convert to binary
    # From the document - "I recommend you use the struct format string:
    # "32s d 32s 32s 12s 12s 12s I" 
    # to pack and unpack the first 6 fields of the block, which will handle the byte alignment issue for you"
    def to_binary(self):
        pass

    # (TODO) Convert back FROM binary
    def from_binary(self):
        pass

    # Add getters and setters