import struct
import uuid
from Crypto.Cipher import AES

AES_KEY = b"R0chLi4uLi4uLi4="

def encrypt_UUID(uuidString):
    """
    Encrypts a valid UUID (case ID)
    """
    try:
        uuidObj = uuid.UUID(uuidString)
    except ValueError as e:
        print(f"Error in UUID format: {uuidString}")
        raise e

    uuidBytes = uuidObj.bytes
    cipher = AES.new(AES_KEY, AES.MODE_ECB)
    encryptedUUID = cipher.encrypt(uuidBytes)
    return encryptedUUID.hex()

def decrypt_UUID(encryptedHex):
    """
    Decrypts a valid UUID (case ID)
    """
    encryptedUUIDBytes = bytes.fromhex(encryptedHex)
    cipher = AES.new(AES_KEY, AES.MODE_ECB)
    originalUUIDBytes = cipher.decrypt(encryptedUUIDBytes)
    originalUUID = uuid.UUID(bytes=originalUUIDBytes)
    return str(originalUUID)

def encrypt_evidence_ID(evidenceID):
    """
    Encrypts evidence ID
    """
    print(f"Passed in: {evidenceID}")
    originalEvidenceID = decrypt_evidence_ID(evidenceID)
    print(f"Original Evidence ID: {originalEvidenceID}")
    evidenceID = int(evidenceID)
    evidenceIDBytes = struct.pack('>I', evidenceID)
    paddedEvidenceID = evidenceIDBytes.ljust(16, b'\x00')
    cipher = AES.new(AES_KEY, AES.MODE_ECB)
    encryptedEvidenceID = cipher.encrypt(paddedEvidenceID)
    return encryptedEvidenceID.hex()

    
def decrypt_evidence_ID(encryptedHex):
    """
    Decrypts evidence ID
    """
    #encryptedEvidenceIDBytes = bytes.fromhex(encryptedHex)
    #cipher = AES.new(AES_KEY, AES.MODE_ECB)
    #decryptedEvidenceIDPadded = cipher.decrypt(encryptedEvidenceIDBytes)
    #decryptedEvidenceIDBytes = decryptedEvidenceIDPadded[:4]
    #evidenceID = struct.unpack('>I', decryptedEvidenceIDBytes)[0]
    #return evidenceID
    try:
        encryptedEvidenceIDBytes = bytes.fromhex(encryptedHex)
        cipher = AES.new(AES_KEY, AES.MODE_ECB)
        decryptedEvidenceIDPadded = cipher.decrypt(encryptedEvidenceIDBytes)
        decryptedEvidenceID = decryptedEvidenceIDPadded.rstrip(b'\0').decode('utf-8')
        return decryptedEvidenceID

    except Exception as e:
        print(f"Error during decryption of evidenceID. Exception: {e}")
        raise e