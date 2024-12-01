import os
import struct
from block import Block
import sys
class Blockchain:
    def __init__(self):
        """
        Initialize an instance (always concurrent never unique) of the blockchain
        """
        self.blockchainFilePath = os.getenv("BCHOC_FILE_PATH", "blockchain.dat")
        self.chain = []
        self.load_blockchain()

    def load_blockchain(self):
        """
        Loads the blockchain file
        Creates an initial block if needed
        """
        if not os.path.exists(self.blockchainFilePath):
            print("Blockchain file not found. Created INITIAL block.")
            self.create_initial_block()
        else:
            with open(self.blockchainFilePath, 'rb') as file:
                fileSize = os.path.getsize(self.blockchainFilePath)
                if fileSize == 0:
                    print("Blockchain file is empty. Creating INITIAL block.")
                    self.create_initial_block()
                else:
                    self.read_blocks(file)

    def read_blocks(self, file):
        """
        Read the blockchain file (from binary) and appends it to the list (does not write)
        """
        # Size of a block - without the data field
        try:
            blockHeaderSize = struct.calcsize("32s d 32s 32s 12s 12s 12s I")
            while True:
                blockHeader = file.read(blockHeaderSize) # Read by size

                if not blockHeader:
                    break

                _, _, _, _, _, _, _, D_length = struct.unpack(
                    "32s d 32s 32s 12s 12s 12s I", blockHeader
                )

                dataField = file.read(D_length)
                blockBinaryData = blockHeader + dataField
                block = Block.from_binary(blockBinaryData)
                self.chain.append(block)
        except Exception as e:
            sys.exit(1)

    def create_initial_block(self):
        """
        Defines the structure of an initial block and appends it to the chain
        """
        initialBlock = Block(
            prevHash = b"\0"*32, # We should store the previous as hashes (see block constructor comment)
            timestamp = 0,
            caseID = "00000000-0000-0000-0000-000000000000",
            evidenceID = "0"*32,
            state = "INITIAL",
            creator = "",
            owner = "",
            data = "Initial block"
        )
        self.append_chain(initialBlock)

    def append_chain(self, newBlock):
        """
        Appends the block to the chain AND writes it to the file
        """
        self.chain.append(newBlock)
        with open(self.blockchainFilePath, 'ab') as file:
            file.write(newBlock.to_binary())