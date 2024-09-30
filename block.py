import struct
from cryptography import encrypt, decrypt

class Block:
    def __init__(self, prevHash, timestamp, caseID, evidenceID, state, creator, owner, data):
        """
        Constructor for a block
        Encode the fields here
        Calc the derived data length (D_length) in the constructor itself (DO NOT PASS AS PARAM)
        TODO: Implement init check here
        :param self: The block in question
        :param prevHash: A block should include a hash value pointing the its previous block AKA parent block (SHA-256)
        :param timestamp: A regular Unix timestamp - must be printed in ISO8601 format when displayed
        :param caseID: UUID that is encrypted using AES ECB and stored as hex
        :param evidenceID: Evidence Item ID - encrypted using AES ECB and stored as hex
        :param state: Can be 'INITIAL', 'CHECKEDIN', 'CHECKEDOUT', 'DISPOSED', 'DESTROYED', or 'RELEASED'
        :param creator: Creator name - free form text with max 12 chars
        :param owner: Free form text with max 16 chars (Must be one of Police, Lawyer, Analyst, Executive)
        :param data: Free form text with byte length specified in data length
        """
        self.prevHash = prevHash.encode('utf-8')[:32].ljust(32, b'\0')
        self.timestamp = timestamp
        self.caseID = encrypt(caseID)
        self.evidenceID = encrypt(evidenceID)
        self.state = state.encode('utf-8')[:12].ljust(12, b'\0')
        self.creator = creator.encode('utf-8')[:12].ljust(12, b'\0')
        self.owner = owner.encode('utf-8')[:12].ljust(12, b'\0')
        self.data = data.encode('utf-8')
        self.D_length = len(self.data)

    
    def to_binary(self):
        """
        Converts to a block's data to binary
        """
        packedBin = struct.pack(
            "32s d 32s 32s 12s 12s 12s I",
            self.prevHash,
            self.timestamp,
            self.caseID,
            self.evidenceID,
            self.state,
            self.creator,
            self.owner,
            self.D_length
        )

        return packedBin + self.data
    
    def get_case_id(self):
        """
        Return decrypted case ID
        """
        return decrypt(self.caseID)

    def get_evidence_id(self):
        """
        Return decrypted evidence ID
        """
        return decrypt(self.evidenceID)

    @classmethod
    def from_binary(cls, binData):
        unpackedData = struct.unpack("32s d 32s 32s 12s 12s 12s I", binData[:144])
        dataField = binData[144:]

        block = cls.__new__(cls)
        block.prevHash = unpackedData[0]
        block.timestamp = unpackedData[1]
        block.caseID = unpackedData[2]
        block.evidenceID = unpackedData[3]
        block.state = unpackedData[4]
        block.creator = unpackedData[5]
        block.owner = unpackedData[6]
        block.D_length = unpackedData[7]
        block.data = dataField

        return block