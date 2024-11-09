import os
from block import Block
from blockchain import Blockchain
import maya
import sys
import hashlib

def handle_init():
    Blockchain()

def handle_add(args):
    """
    Handle the 'add' command to add a block to the blockchain.
    """
    if not verify_password(args.password)[1]:
        print('> Invalid password')
        sys.exit(1)

    blockchain = Blockchain()
    role = verify_password(args.password)[0]

    if len(blockchain.chain) == 0:
        print("Blockchain empty, please initialize first.")
        return

    timestampFloat = maya.now().epoch
    timestampDisplay = maya.MayaDT(timestampFloat).iso8601().replace('+00:00', 'Z')

    # Get the hash of the initial block
    prevBlockHash = blockchain.chain[-1].hash_block()

    # SETS AGAIN LFGGGGG
    existingEvidenceIDs = set(block.get_evidence_id() for block in blockchain.chain)

    # Loop thru and add block for each evidence id
    # Could probably add a new base case in this function to not even 
    # enter this loop if there is only 1 evidence id in the list
    for evidenceID in args.item_id:
        parsedEvidenceID = int(evidenceID)

        # If the evidence ID is not unique, skip adding
        if str(parsedEvidenceID) in existingEvidenceIDs:
            print(f"Evidence ID '{parsedEvidenceID}' was not added.")
            print('Evidence IDs must be unique')
            sys.exit(1)
        
        newBlock = Block(
            prevHash = prevBlockHash,
            timestamp = timestampFloat,
            caseID = args.case_id,
            evidenceID = parsedEvidenceID,
            state = "CHECKEDIN",
            creator = args.creator,
            owner = role,
            data = f"Added item {parsedEvidenceID}"
        )

        blockchain.append_chain(newBlock)
        
        print(f"> Added item: {newBlock.get_evidence_id()}")
        print(f"> Status: {newBlock.get_state()}")
        print(f"> Time of action: {timestampDisplay}")
        print()

        # Update prevBlockHash for the next block
        prevBlockHash = newBlock.hash_block()

def handle_checkout(args):
    """
    Checks out a checked in case
    """
    if not verify_password(args.password)[1]:
        print('Invalid password')
        sys.exit(1)

    role = verify_password(args.password)[0] # Role of the password
    blockchain = Blockchain()
    checkoutBlock = None
    timestampFloat = maya.now().epoch
    timestampDisplay = maya.MayaDT(timestampFloat).iso8601().replace('+00:00', 'Z')
    searchID = str(args.item_id)
    
    # loop to find matching blocks
    for block in blockchain.chain:
        if searchID == block.get_evidence_id():
            checkoutBlock = block
    
    # Return if the item id does not exist
    if checkoutBlock == None:
        print(f"Item ID {args.item_id} does not exist")
        sys.exit(1)

    # Evidence items that are either disposed, destroyed, or released cannot be checkedout
    reasons = ['DISPOSED', 'DESTROYED', 'RELEASED']
    if checkoutBlock.get_state() in reasons:
        print(f"The requested block is {checkoutBlock.get_state()}. Further action is forbidden")
        sys.exit(1)
    
    # Nab hash of the previous block
    prevBlockHash = blockchain.chain[-1].hash_block()

    newBlock = Block(
        prevHash = prevBlockHash,
        timestamp = timestampFloat,
        caseID = checkoutBlock.get_case_id(),
        evidenceID = checkoutBlock.get_evidence_id(),
        state = "CHECKEDOUT",
        creator = checkoutBlock.get_creator(),
        owner = role,
        data = f"Checked out item {checkoutBlock.get_evidence_id()}"
    )

    blockchain.append_chain(newBlock)

    print(f"> Case: {newBlock.get_case_id()}")
    print(f"> Checked out item: {newBlock.get_evidence_id()}")
    print(f"> Status: {newBlock.get_state()}")
    print(f"> Time of action: {timestampDisplay}")

def handle_checkin(args):
    """
    Checks in a checked out case
    """
    if not verify_password(args.password)[1]:
        print("Invalid password")
        return

    role = verify_password(args.password)[0] # Role of the password
    blockchain = Blockchain()
    checkinBlock = None
    timestampFloat = maya.now().epoch
    timestampDisplay = maya.MayaDT(timestampFloat).iso8601().replace('+00:00', 'Z')
    searchID = str(args.item_id)
    
    # loop to find matching blocks
    for block in blockchain.chain:
        if searchID == block.get_evidence_id():
            checkinBlock = block
    
    # Return if the item id does not exist
    if checkinBlock == None:
        print(f"Item ID {args.item_id} does not exist")
        sys.exit(1)
    
    if checkinBlock.get_state() == 'CHECKEDIN':
        print(f"Cannot checkin items that are already checkedin")
        sys.exit(1)
    
    # Evidence items that are either disposed, destroyed, or released cannot be checkedout
    reasons = ['DISPOSED', 'DESTROYED', 'RELEASED']
    if checkinBlock.get_state() in reasons:
        print(f"The requested block is {checkinBlock.get_state()}. Further action is forbidden")
        sys.exit(1)
    
    # Nab hash of the previous block
    prevBlockHash = blockchain.chain[-1].hash_block()

    newBlock = Block(
        prevHash = prevBlockHash,
        timestamp = timestampFloat,
        caseID = checkinBlock.get_case_id(),
        evidenceID = checkinBlock.get_evidence_id(),
        state = "CHECKEDIN",
        creator = checkinBlock.get_creator(),
        owner = role,
        data = f"Checked out item {checkinBlock.get_evidence_id()}"
    )

    blockchain.append_chain(newBlock)

    print(f"> Case: {newBlock.get_case_id()}")
    print(f"> Checked in item: {newBlock.get_evidence_id()}")
    print(f"> Status: {newBlock.get_state()}")
    print(f"> Time of action: {timestampDisplay}")

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
    """
    Show all item ids (unique) for a given case id
    """
    blockchain = Blockchain()

    if len(blockchain.chain) <= 1:
        print("No cases found in the blockchain.")
        return

    # Sets again baby
    itemIDSet = set()
    
    # Loop to add valid evidence ids to the set
    for block in blockchain.chain:
        if block.get_case_id() == args.case_id:
            itemIDSet.add(block.get_evidence_id())

    # None found, return
    if len(itemIDSet) == 0:
        print(f"Case number '{args.case_id}' does not exist")
        return

    print(f"Item IDs for Case '{args.case_id}':")
    itemIDList = list(itemIDSet) # Convert to list because I want the prints to be numbered LMAO
    for index, itemID in enumerate(itemIDList, start=1):
        print(f"Item ID {index}: {itemID}")

def handle_show_history(args):
    """
    Display the blockchain entries for the requested item giving the oldest first
    Optional arguments to filter: Case ID, Item ID, reverse flag
    Password is optional: Display as hex if password is invalid or there is none
    """
    blockchain = Blockchain()

    # Get all blocks excluding the initial block
    filteredBlocks = blockchain.chain[1:]
    
    # Filter by case id if provided
    if args.case_id:
        filteredBlocks = [
                block for block in filteredBlocks if block.get_case_id() == args.case_id
            ]
    
    # Filter by item id
    if args.item_id:
        filteredBlocks = [
                block for block in filteredBlocks if block.get_evidence_id() == args.item_id
            ]
    
    # Reverse the list if given a flag
    if args.reverse:
        filteredBlocks = filteredBlocks[::-1]

    # Cap by num entries
    if args.num_entries:
        filteredBlocks = filteredBlocks[:args.num_entries]

    # Display
    for block in filteredBlocks:
        # Display case id and item id as hex if no password is provided
        caseID = block.caseID
        evidenceID = block.evidenceID
        if args.password:
            if verify_password(args.password)[1]:
                caseID = block.get_case_id()
                evidenceID = block.get_evidence_id()

        print(f"Case: {caseID}")
        print(f"Item: {evidenceID}")
        print(f"Action: {block.get_state()}")
        print(f"Time: {maya.MayaDT(block.get_timestamp()).iso8601()}")
        print()

def handle_remove(args):
    """
    "Removes" an item from the chain (prevents further action to the block)
    Adds the removed block to the chain
    If the reason of removal is RELEASED, -o (lawful owner information) must be given
    """
    if not verify_password(args.password)[1]:
        print("> Invalid password")
        sys.exit(1)

    
    blockchain = Blockchain()
    blockToRemove = None

    # Must be one of DISPOSED, DESTROYED, or RELEASED
    reasons = ['DISPOSED', 'DESTROYED', 'RELEASED']
    if args.reason not in reasons:
        print(f"Invalid reason. Must be one of: {', '.join(reasons)}")
        sys.exit(1)
    
    # # Check if owner is given if the reason is RELEASED
    # if args.reason == 'RELEASED':
    #     if not args.owner:
    #         print("Information about the lawful owner must be given to release an evidence item")
    #         return

    # Find the first instance of a matching block, break
    for block in reversed(blockchain.chain):
        if block.get_evidence_id() == args.item_id:
            blockToRemove = block
            break

    # If a block with the desired item id does not exist
    if not blockToRemove:
        print(f"Item ID {args.item_id} does not exist")
        sys.exit(1)
    
    # If the block is not checked in, it cannot be removed
    if blockToRemove.get_state() != 'CHECKEDIN':
        print(f"Only checkedin items can be removed")
        sys.exit(1)
    
    timestampFloat = maya.now().epoch
    timestampDisplay = maya.MayaDT(timestampFloat).iso8601().replace('+00:00', 'Z')
    prevBlockHash = blockchain.chain[-1].hash_block()

    newBlock = Block(
        prevHash = prevBlockHash,
        timestamp = timestampFloat,
        caseID = blockToRemove.get_case_id(),
        evidenceID = args.item_id,
        state = args.reason,
        creator = blockToRemove.get_creator(),
        owner = args.owner if args.owner else "",
        data = f"Removed item {args.item_id}. Reason: {args.reason}"
    )

    blockchain.append_chain(newBlock)

    print(f"Case: {newBlock.get_case_id()}")
    print(f"Removed item: {newBlock.get_evidence_id()}")
    print(f"Status: {newBlock.get_state()}")
    print(f"Time of action: {maya.MayaDT(block.get_timestamp()).iso8601()}")

def handle_verify():
    blockchain = Blockchain()
    transactionCount = len(blockchain.chain)
    print(f">Transactions in blockchain: {transactionCount}")

    initialBlockPrevHash = "0" * 64 # Initial block will always have this previous hash
    prevHash = None # Declare prevHash to keep track of the previous hash
    seenHashes = set() # Use this to keep track of seen hash values (should be unique = set)
    removedItems = set() # Use this to keep track of items which were removed (no action can happen)
    itemStates = {} # Key value pairs of 'itemId: state'. Use this to keep track of state transitions
    validTransitions = {
        "INITIAL": ["CHECKEDIN"],
        "CHECKEDIN": ["CHECKEDOUT", "DISPOSED", "DESTROYED", "RELEASED"],
        "CHECKEDOUT": ["CHECKEDIN"]
    }

    for index, block in enumerate(blockchain.chain):
        currentHash = block.hash_block().hex() # Always print in hex for verification

        # We have to handle the case where the initial block is empty as well
        if index == 0:
            if block.get_state() != "INITIAL" or block.get_prev_hash() != initialBlockPrevHash:
                print("State of blockchain: ERROR")
                print(f"Bad block: {currentHash}")
                print("Invalid initial block")
                sys.exit(1)
        else:
            # Check the previous hash here
            # If is in seenHashes... then a parent has multiple children
            if block.get_prev_hash() != prevHash:
                print("State of blockchain: ERROR")
                print(f"Bad block: {currentHash}")
                if block.get_prev_hash() not in seenHashes:
                    print("Parent block: NOT FOUND")
                else:
                    print("Two blocks were found with the same parent")
                sys.exit(1)

            # Check block checksum
            if block.hash_block() != hashlib.sha256(block.to_binary()).digest():
                print("State of blockchain: ERROR")
                print(f"Bad block: {currentHash}")
                print("Block contents do not match block checksum")
                sys.exit(1)

            itemID = block.get_evidence_id()
            currentState = block.get_state()

            # Check in and check out post removal validations
            if itemID in removedItems:
                print("State of blockchain: ERROR")
                print(f"Bad block: {currentHash}")
                print("Item checked out or checked in after removal from chain")
                sys.exit(1)

            # Validate state transitions
            if itemID in itemStates:
                prevState = itemStates[itemID]
                if currentState not in validTransitions.get(prevState, []):
                    print("State of blockchain: ERROR")
                    print(f"Bad block: {currentHash}")
                    print(f"Invalid state transition: {prevState} to {currentState}")
                    sys.exit(1)

            # Update itemStates
            itemStates[itemID] = currentState

            # Update removedItems
            if currentState in ["DISPOSED", "DESTROYED", "RELEASED"]:
                removedItems.add(itemID)
        
        # Update prevHash and seenHashes with currenHash
        prevHash = currentHash
        seenHashes.add(currentHash)
    
    print("State of blockchain: CLEAN")

def verify_password(passwordArg):
    """
    Verify if a parsed password is valid or not
    Returns a tuple of [role, isValid]
    """
    # Grab the environmental variables
    roles = {
        'POLICE': os.environ.get('BCHOC_PASSWORD_POLICE'),
        'LAWYER': os.environ.get('BCHOC_PASSWORD_LAWYER'),
        'ANALYST': os.environ.get('BCHOC_PASSWORD_ANALYST'),
        'EXECUTIVE': os.environ.get('BCHOC_PASSWORD_EXECUTIVE'),
        'CREATOR': os.environ.get('BCHOC_PASSWORD_CREATOR')
    }

    # Return early if password is not valid
    if passwordArg not in roles.values():
        return None, False

    role = None
    isValid = False

    # Find the associated key
    for key, value in roles.items():
        if value == passwordArg:
            role = key
            isValid = True

    return role, isValid