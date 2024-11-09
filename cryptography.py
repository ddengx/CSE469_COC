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
    if len(encryptedUUID) != 16:
        encryptedUUID = encryptedUUID[:16].ljust(16, b'\0')
    return encryptedUUID.hex()


def decrypt_UUID(encryptedHex):
    """
    Decrypts a valid UUID (case ID)
    """
    encryptedUUIDBytes = bytes.fromhex(encryptedHex)
    cipher = AES.new(AES_KEY, AES.MODE_ECB)
    originalUUIDBytes = cipher.decrypt(encryptedUUIDBytes)
    formattedUUIDBytes = originalUUIDBytes.ljust(16, b'\0')[:16]
    originalUUID = uuid.UUID(bytes=formattedUUIDBytes)
    return str(originalUUID)


def encrypt_evidence_ID(evidenceID):
    """
    Encrypts evidence ID
    """
    # Fixed logic in this function (we were padding BEFORE we encrypted causing issues)
    # 
    evidenceID = str(int(evidenceID))
    evidenceIDBytes = struct.pack('>Q', int(evidenceID))  # Pack the raw number
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
    # Mismatch between encrypt evidence id - changed to >Q and to 8 bytes as in encrypt
    evidenceID = struct.unpack('>Q', decryptedEvidenceIDPadded[:8])[0]
    return str(evidenceID)