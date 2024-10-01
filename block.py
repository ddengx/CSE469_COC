import hashlib
import struct
from cryptography import encrypt_UUID, decrypt_UUID, encrypt_evidence_ID, decrypt_evidence_ID

class Block:
    def __init__(self, prevHash, timestamp, caseID, evidenceID, state, creator, owner, data):
        """
        Constructor for a block
        Encode the fields here
        Calc the derived data length (D_length) in the constructor itself (DO NOT PASS AS PARAM)
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
        self.caseID = encrypt_UUID(caseID) # 32 byte hex string
        self.evidenceID = encrypt_evidence_ID(evidenceID) # 32 byte hex string
        self.state = state.encode('utf-8')[:12].ljust(12, b'\0')
        self.creator = creator.encode('utf-8')[:12].ljust(12, b'\0')
        self.owner = owner.encode('utf-8')[:12].ljust(12, b'\0')
        self.data = data.encode('utf-8')
        self.D_length = len(self.data)

    
    def to_binary(self):
        """
        Converts to a block's data to binary
        """
        paddedCaseID = bytes.fromhex(self.caseID).ljust(32, b'\0')
        paddedEvidenceID = bytes.fromhex(self.evidenceID).ljust(32, b'\0')
        packedBin = struct.pack(
            "32s d 32s 32s 12s 12s 12s I",
            self.prevHash,
            self.timestamp,
            paddedCaseID,
            paddedEvidenceID,
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
        return decrypt_UUID(self.caseID)

    def get_evidence_id(self):
        """
        Return decrypted evidence ID
        """
        return decrypt_evidence_ID(self.evidenceID)

    @classmethod
    def from_binary(cls, binData):
        """
        Convert a binary representation of a block into a block
        """
        blockHeaderSize = struct.calcsize("32s d 32s 32s 12s 12s 12s I")
        blockHeader = binData[:blockHeaderSize]

        prevHash, timestamp, caseID, evidenceID, state, creator, owner, D_length = struct.unpack(
            "32s d 32s 32s 12s 12s 12s I", blockHeader
        )

        dataField = binData[blockHeaderSize:blockHeaderSize + D_length]
        caseID = caseID.rstrip(b'\0')
        caseIDHex = caseID.hex()
        evidenceID = evidenceID.rstrip(b'\0')
        evidenceIDHex = evidenceID.hex()

        return cls(
            prevHash = prevHash.decode('utf-8').rstrip('\0'),
            timestamp = timestamp,
            caseID = caseIDHex,
            evidenceID = evidenceIDHex,
            state = state.decode('utf-8').rstrip('\0'),
            creator = creator.decode('utf-8').rstrip('\0'),
            owner = owner.decode('utf-8').rstrip('\0'),
            data = dataField.decode('utf-8') 
        )
    
    def hash_block(self):
        """
        Create a SHA-256 hash of a block (its binary representation)
        """
        return hashlib.sha256(self.to_binary()).hexdigest()