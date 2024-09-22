
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

import os
from block import Block
import argparse


class Blockchain:
    def __init__(self):
        self.chain = []

        self.load_blockchain()

    # Import blockchain data
    # Nab from environ
    # Add checks for absence of, or lack thereof, blocks here
    def load_blockchain(self):
    # Add a part to load up a JSON or CSV file


class Block:
    def __init__(self) -> None:
        pass

    # Add an initial block if there is none
    def init_blockchain(self):
        pass


    # Append
    def add_block(self, block):
        pass

    # Verify the chain
    def verify(self):
        pass

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
    print("Initializing blockchain")


def verify(args):
    print("Verifying blockchain")


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


if __name__ == "__main__":
    MainBlockchain = Blockchain()
    main()
