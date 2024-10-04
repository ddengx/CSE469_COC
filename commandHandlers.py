from block import Block
from blockchain import Blockchain
import maya

def handle_init():
    Blockchain()

def handle_add(args):
    """
    Handle the 'add' command to add a block to the blockchain.
    """
    blockchain = Blockchain()

    if len(blockchain.chain) == 0:
        print("Blockchain empty, please initialize first.")
        return

    timestampFloat = maya.now().epoch
    timestampDisplay = maya.MayaDT(timestampFloat).iso8601().replace('+00:00', 'Z')

    # Get the hash of the initial block
    prevBlockHash = blockchain.chain[-1].hash_block()

    # Loop thru and add block for each evidence id
    # Could probably add a new base case in this function to not even 
    # enter this loop if there is only 1 evidence id in the list
    for evidence_id in args.item_id:
        parsedEvidenceID = int(evidence_id)
        
        newBlock = Block(
            prevHash = prevBlockHash,
            timestamp = timestampFloat,
            caseID = args.case_id,
            evidenceID = parsedEvidenceID,
            state = "CHECKEDIN",
            creator = args.creator,
            owner = args.creator,
            data = f"Added item {evidence_id}"
        )

        blockchain.chain.append(newBlock)
        with open(blockchain.blockchainFilePath, 'ab') as file:
            file.write(newBlock.to_binary())
        
        print(f"> Added item: {newBlock.get_evidence_id()}")
        print(f"> Status: {newBlock.get_state()}")
        print(f"> Time of action: {timestampDisplay}")
        print()

        # Update prevBlockHash for the next block
        prevBlockHash = newBlock.hash_block()

def handle_checkout(args):
    # Add
    pass

def handle_checkin(args):
    # ADd
    pass

# Not sure of the exact output Baek wants
# Showing only case IDs for now
def handle_show_cases():
    """
    Show all the added case IDs
    """
    blockchain = Blockchain()
    if len(blockchain.chain) <= 1:
        print("No cases found in the blockchain.")
        return

    cases = set() # set so we avoid duplicates (LEETCODE TOTD)
    for block in blockchain.chain[1:]:
        cases.add(block.caseID) # Since password is not an argument, show the encrypted hex value
    for case in cases:
        print(f"Case ID: {case}")

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