
#EXAMPLE: https://www.youtube.com/watch?v=umLm_ES-fvk&ab_channel=CameronHartmann
#This is from the slides

# TODO: Implement blockchain class here

# Required block struct below
#INITIAL BLOCK =
#Prev_hash = 0, # 32 bytes 
#Timestamp = 0, # 08 bytes
#Case_id = b"0"*32, # 32 bytes (32 zero's) 
#Evidence_id = b"0"*32, # 32 bytes (32 zero's) 
#State = b"INITIAL\0\0\0\0\0", # 12 bytes
#creator = b"\0"*12, # 12 bytes (12 null bytes) 
#owner = b"\0"*12, # 12 bytes (12 null bytes) 
#D_length = 14, # 04 bytes
#Data = b"Initial block\0"

#REMEMBER:
#All block data must be stored in a binary format.

import os
import sys
from block import Block
import argparse
import struct


class Blockchain:
    def __init__(self):
        self.chain = []



def add(args):
    print(f"Adding item(s)")


def checkout_item(args):
    print(f"Checking out item")


def checkin_item(args):
    print(f"Checking in item")


def show_cases(args):
    print("Showing all cases")


def show_items(args):
    print(f"Showing items")


def show_history(args):
    print(f"Showing history")


def remove(args):
    print(f"Removing item")


def init(args):
    bhocFilePath = os.environ.get('BCHOC_FILE_PATH')
    givenFormat = "32s d 32s 32s 12s 12s 12s I"
    if bhocFilePath is None:
        print("Blockchain file not found. Created INITIAL block.")
        newBlock = Block(
                0,
                0,
                b"0"*32,
                b"0"*32,
                b"INITIAL\0\0\0\0\0",
                b"\0"*12, 
                b"\0"*12,
                14,
                b"Initial block\0"
            )
        MainBlockchain.chain.append(newBlock)
        packedData = struct.pack(givenFormat,newBlock.prevHash,newBlock.
                                 timestamp,newBlock.caseID,newBlock.evidenceID,
                                 newBlock.state,newBlock.creator,newBlock.owner,newBlock.data)
        #TODO: Most likely write this in a file and also declare file path for recognizing again.
    else:
        #TODO: Add logic to parse through BHOC file given
        #WTF DOES THE FILE LOOK LIKE?????
        # INITIAL BLOCK =  
        # Prev_hash = 0,  # 32 bytes
        # Timestamp = 0,  # 08 bytes
        # Case_id = b"0"*32,      # 32 bytes (32 zero's)
        # Evidence_id = b"0"*32,  # 32 bytes (32 zero's)
        # State = b"INITIAL\0\0\0\0\0",  # 12 bytes
        # creator = b"\0"*12,     # 12 bytes (12 null bytes)
        # owner = b"\0"*12,       # 12 bytes (12 null bytes)
        # D_length = 14,  # 04 bytes
        # Data = b"Initial block\0"
        with open(bhocFilePath, 'rb') as file:
            data = file.read(144)
            previousHash, timeStamp, caseId, evidenceId, state, creator, owner, dataLength = struct.unpack(givenFormat, data)
            


def verify(args):
    print("going through and verifying")




def main():
    try:
        #Parsing TIME
        mainParser = argparse.ArgumentParser()
        subparsers = mainParser.add_subparsers(dest='choices')

        #Adding Blocks
        addBlock = subparsers.add_parser('add')
        addBlock.add_argument('-c', '--case_id', required=True)
        addBlock.add_argument('-i', '--item_id', nargs='+', required=True)
        addBlock.add_argument('-g', '--creator', required=True)
        addBlock.add_argument('-p', '--password', required=True)
        addBlock.set_defaults(func=add)

        #Checkout blocks
        checkoutBlock = subparsers.add_parser('checkout')
        checkoutBlock.add_argument('-i', '--item_id', required=True)
        checkoutBlock.add_argument('-p', '--password', required=True)
        checkoutBlock.set_defaults(func=checkout_item)

        #Checkin Blocks
        checkinBlock = subparsers.add_parser('checkin')
        checkinBlock.add_argument('-i', '--item_id', required=True)
        checkinBlock.add_argument('-p', '--password', required=True)
        checkinBlock.set_defaults(func=checkin_item)

        #Showing subparser (because argparse doesnt do whitespace ugh)
        showBlock = subparsers.add_parser("show")
        showSubparser = showBlock.add_subparsers(dest='showing')
        #Showing Cases 
        showCasesBlock = showSubparser.add_parser('cases')
        showCasesBlock.set_defaults(func=show_cases)

        #Showing Items
        showItemsBlock = showSubparser.add_parser('items')
        showItemsBlock.add_argument('-c', '--case_id', required=True)
        showItemsBlock.set_defaults(func=show_items)

        #showting history
        showHistoryBlock = showSubparser.add_parser('history')
        showHistoryBlock.add_argument('-c', '--case_id')
        showHistoryBlock.add_argument('-i', '--item_id')
        showHistoryBlock.add_argument('-n', '--num_entries')
        showHistoryBlock.add_argument('-r', '--reverse')
        showHistoryBlock.add_argument('-p', '--password', required=True)
        showHistoryBlock.set_defaults(func=show_history)
        #show block end

        #Removing Blocks
        removeBlock = subparsers.add_parser('remove')
        removeBlock.add_argument('-i', '--item_id', required=True)
        removeBlock.add_argument('-y', '--reason', required=True)
        removeBlock.add_argument('-p', '--password', required=True)
        removeBlock.set_defaults(func=remove)

        #Init blocks
        initBlock = subparsers.add_parser('init')
        initBlock.set_defaults(func=init)

        #Verifying 
        verifyBlock = subparsers.add_parser('verify')
        verifyBlock.set_defaults(func=verify)

        # Parse arguments
        args = mainParser.parse_args()

        if hasattr(args, 'func'):
            args.func(args)
        else:
            print("function calls are wrong or something idk.")

    except Exception as error:
        print(f"An error occurred: {error}")
        sys.exit(1)


if __name__ == "__main__":
    MainBlockchain = Blockchain()
    main()
