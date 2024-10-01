from block import Block
from blockchain import Blockchain
import maya

def handle_init(args):
    Blockchain()

def handle_add(args):
    """
    Handle the 'add' command to add a block to the blockchain.
    """
    blockchain = Blockchain()
    parsedEvidenceID = int(args.item_id[0])
    timestampFloat = maya.now().epoch
    timestampDisplay = maya.MayaDT(timestampFloat).iso8601().replace('+00:00', 'Z')

    if len(blockchain.chain) > 0:
        prevBlock = blockchain.chain[-1]
        prevBlockHash = prevBlock.hash_block()
    else:
        print("Blockchain empty, please initialize first.")
        return
    
    newBlock = Block(
        prevHash = prevBlockHash,
        timestamp = timestampFloat,
        caseID = args.case_id,
        evidenceID = parsedEvidenceID,
        state = "CHECKEDIN",
        creator = args.creator,
        owner = args.creator,
        data="Added item"
    )

    blockchain.chain.append(newBlock)
    with open(blockchain.blockchainFilePath, 'ab') as file:
        file.write(newBlock.to_binary())
    print(f"> Added item: {args.item_id[0]}")
    print(f"> Status: CHECKEDIN")
    print(f"> Time of action: {timestampDisplay}")

def handle_checkout(args):
    # Add
    pass

def handle_checkin(args):
    # ADd
    pass

def handle_show_cases(args):
    # ADd
    pass

def handle_show_items(args):
    # ADd
    pass

def handle_show_history(args):
    # ADd
    pass

def handle_remove(args):
    # Add
    pass

def handle_verify(args):
    # ADd
    pass

def verify_password(args):
    # todo
    pass