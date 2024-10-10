import os

from block import Block
from blockchain import Blockchain
import maya
import sys
def handle_init():
    Blockchain()

def handle_add(args):
    """
    Handle the 'add' command to add a block to the blockchain.
    """
    if verify_password(args.password)[1]:
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
                continue
            
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
    else:
        print('Invalid password')
        return

def handle_checkout(args):
    """
    Checks out a checked in case
    """
    isValid = verify_password(args.password)[1] # Bool
    if isValid:
        role = verify_password(args.password)[0] # Role of the password
        blockchain = Blockchain()
        checkoutBlock = None
        timestampFloat = maya.now().epoch
        timestampDisplay = maya.MayaDT(timestampFloat).iso8601().replace('+00:00', 'Z')

        # loop to find matching blocks
        for block in blockchain.chain:
            if args.item_id == block.get_evidence_id():
                checkoutBlock = block
        
        # Return if the item id does not exist
        if checkoutBlock == None:
            print(f"Item ID {args.item_id} does not exist")
            return

        # Must be one of the owners
        # Need clarification on the requirements
        # May need to edit this to roles of all instances of the item id
        if checkoutBlock.get_owner() != str(role):
            print(f"Only valid owners of this case can checkout")
            return
        
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
    else:
        print('Invalid password')
        return

def handle_checkin(args):
    """
    Checks in a checked out case
    """
    isValid = verify_password(args.password)[1] # Bool
    if isValid:
        role = verify_password(args.password)[0] # Role of the password
        blockchain = Blockchain()
        checkinBlock = None
        timestampFloat = maya.now().epoch
        timestampDisplay = maya.MayaDT(timestampFloat).iso8601().replace('+00:00', 'Z')

        # loop to find matching blocks
        for block in blockchain.chain:
            if args.item_id == block.get_evidence_id():
                checkinBlock = block
        
        # Return if the item id does not exist
        if checkinBlock == None:
            print(f"Item ID {args.item_id} does not exist")
            return

        # Must be one of the owners
        # Need clarification on the requirements
        # May need to edit this to roles of all instances of the item id
        if checkinBlock.get_owner() != str(role):
            print(f"Only valid owners of this case can checkout")
            return
        
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
    else:
        print('Invalid password')
        return

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
    print()
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
    pass

def handle_verify(args):
    blockchain = Blockchain()
    transactionCount = len(blockchain.chain)
    print(f">Transactions in blockchain: {transactionCount}")


    # IMPORTANT: For testing purposes, you can assume that a blockchain will only have one error in it.
    # If this weren’t the case, it would matter which direction you traverse the chain while validating,
    # and I don’t want you to have to worry about that.
    # In cases of errors (invalid operations), exit with error code 1.

    #Verify Error Cases
    #Im not sure what we should be returning as the "bad block"
    #For now, im just gonna use the case id

    hashHistory = {}
    for index,block in enumerate(blockchain.chain):

        if block.prevHash not in hashHistory and index != 0:
            print(">State of blockchain: ERROR")
            print(f">Bad block:\n{block.caseID}\n>Parent block: NOT FOUND")
            sys.exit(1)
        elif block.prevHash in hashHistory:
            print(">State of blockchain: ERROR")
            print(f">Bad block:\n{block.caseID}\n>Parent block:\n{hashHistory[block.caseID]}\n>Two blocks were found with the same parent.")
            sys.exit(1)

        #Add another case for Block contents do not match block checksum.


        #Add another case for Item checked out or checked in after removal from chain.

    print(">State of blockchain: CLEAN")



    pass

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