import argparse


# bchoc add -c case_id -i item_id [-i item_id ...] -g creator -p password(creator’s)
# bchoc checkout -i item_id -p password
# bchoc checkin -i item_id -p password
# bchoc show cases 
# bchoc show items -c case_id
# bchoc show history [-c case_id] [-i item_id] [-n num_entries] [-r] -p password
# bchoc remove -i item_id -y reason -p password(creator’s)
# bchoc init
# bchoc verify

class Blockchain:
    def __init__(self):
        self.chain = []
    #add a part to load up a json or csv file

class Block:

    def __init__(self) -> None:
        pass


def main():
    
    #Setup parsers
    mainParser = argparse.ArgumentParser()
    secondParser = mainParser.add_subparsers(dest='choices')

    #Adding
    addBlock = secondParser.add_parser('add')
    addBlock.add_argument('-c', '--case_id', required=True)
    addBlock.add_argument('-i', '--item_ids', nargs='+', required=True)
    addBlock.add_argument('-g', '--creator', required=True)
    addBlock.add_argument('-p', '--password', required=True)
    #Checkout
    checkoutBlock = secondParser.add_parser('checkout')
    #Checkin
    checkinBlock = secondParser.add_parser('checkin')
    #Showing
    showCasesBlock = secondParser.add_parser('show cases')

    showItemsBlock = secondParser.add_parser('show items')

    showHistoryBlock = secondParser.add_parser('show history')

    #Remove
    removeBlock = secondParser.add_parser('remove')
    #Init
    initBlock = secondParser.add_parser('init')
    #Verify
    verifyBlock = secondParser.add_parser('verify')

    #Grab Commands
    args = mainParser.parse_args()

    #Call functions
    if args.choices == 'add':
        print('add')
    if args.choices == 'checkout':
        print('checkout')
    if args.choices == 'checkin':
        print('checkin')
    if args.choices == 'show cases':
        print('show cases')
    if args.choices == 'show items':
        print('show items')
    if args.choices == 'show history':
        print('show history')
    if args.choices == 'remove':
        print('remove')
    if args.choices == 'init':
        print('init')
    if args.choices == 'add':
        print('verify')

if __name__ == "__main__":
    MainBlockchain = Blockchain()
    main()