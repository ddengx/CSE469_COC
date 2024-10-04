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
    evidenceID = str(evidenceID)
    #I added padding because it wasnt the right length - Ken
    evidenceID = evidenceID.ljust(16, '0') if len(evidenceID) < 16 else evidenceID[:16]
    #This line is because if you make it into int, sometimes the number get too big
    evidenceIDBytes = struct.pack('>I', int(evidenceID[:10]))
    paddedEvidenceID = evidenceIDBytes.ljust(16, b'\x00')
    cipher = AES.new(AES_KEY, AES.MODE_ECB)
    encryptedEvidenceID = cipher.encrypt(paddedEvidenceID)
    return encryptedEvidenceID.hex()


def decrypt_evidence_ID(encryptedHex):
    """
    Decrypts evidence ID
    """
    encryptedEvidenceIDBytes = bytes.fromhex(encryptedHex)
    cipher = AES.new(AES_KEY, AES.MODE_ECB)
    decryptedEvidenceIDPadded = cipher.decrypt(encryptedEvidenceIDBytes)
    evidenceID = struct.unpack('>I', decryptedEvidenceIDPadded[:4])[0]
    return str(evidenceID)