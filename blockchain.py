import os
import struct
from block import Block

class Blockchain:
    def __init__(self):
        self.blockchainFilePath = os.getenv("BCHOC_FILE_PATH", "blockchain.dat")
        self.chain = []
        self.load_blockchain()

    def load_blockchain(self):
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
                    print("Loading blockchain data...")
                    self.read_blocks(file)

    def read_blocks(self, file):
        blockHeaderSize = struct.calcsize("32s d 32s 32s 12s 12s 12s I")

        while True:
            blockHeader = file.read(blockHeaderSize)

            if not blockHeader:
                print("Reading a file with NO BLOCK IDITO")
                break

            prev_hash, timestamp, case_id, evidence_id, state, creator, owner, D_length = struct.unpack(
                "32s d 32s 32s 12s 12s 12s I", blockHeader
            )

            dataField = file.read(D_length)
            blockBinaryData = blockHeader + dataField
            block = Block.from_binary(blockBinaryData)
            self.chain.append(block)

    def create_initial_block(self):
        initialBlock = Block(
            prevHash = "0",
            timestamp = 0,
            caseID = "00000000-0000-0000-0000-000000000000",
            evidenceID = 0,
            state = "INITIAL",
            creator = "",
            owner = "",
            data = "Initial block"
        )
        with open(self.blockchainFilePath, 'wb') as file:
            file.write(initialBlock.to_binary())
        self.chain.append(initialBlock)