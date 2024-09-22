import argparse
import sys
import blockchain
import commandHandlers

# bchoc add -c case_id -i item_id [-i item_id ...] -g creator -p password(creator’s)
# bchoc checkout -i item_id -p password
# bchoc checkin -i item_id -p password
# bchoc show cases 
# bchoc show items -c case_id
# bchoc show history [-c case_id] [-i item_id] [-n num_entries] [-r] -p password
# bchoc remove -i item_id -y reason -p password(creator’s)
# bchoc init
# bchoc verify

def main():
    
    #Setup parsers
    mainParser = argparse.ArgumentParser(description='CSE469 Chain of Custody')
    subParser = mainParser.add_subparsers(dest='choices', required=True)

    #Adding
    addParser = subParser.add_parser('add')
    addParser.add_argument('-c', '--case_id', required=True, help='Case ID (UUID)')
    addParser.add_argument('-i', '--item_id', nargs='+', required=True, help='Evidence item ID')
    addParser.add_argument('-g', '--creator', required=True, help='Creator')
    addParser.add_argument('-p', '--password', required=True, help='Password')

    #Checkout
    checkoutParser = subParser.add_parser('checkout')
    checkoutParser.add_argument('-i', '--item_id', nargs='+', required=True, help='Evidence item ID')
    checkoutParser.add_argument('-p', '--password', required=True, help='Password')

    #Checkin
    checkinParser = subParser.add_parser('checkin')
    checkinParser.add_argument('-i', '--item_id', nargs='+', required=True, help='Evidence item ID')
    checkinParser.add_argument('-p', '--password', required=True, help='Password')

    #Show cases
    subParser.add_parser('show').add_subparsers().add_parser('cases')

    #Show items
    showItemsParser = subParser.add_parser('show').add_subparsers().add_parser('items')
    showItemsParser.add_argument('-c', '--case_id', required=True, help='Case ID (UUID)')

    #Show history
    showHistoryParser = subParser.add_parser('show').add_subparsers().add_parser('history')
    showHistoryParser.add_argument('-c', '--case', help='Case ID')
    showHistoryParser.add_argument('-i', '--item_id', help='Evidence item ID')
    showHistoryParser.add_argument('-n', '--num_entries', type=int, help='Number of entries to show')
    showHistoryParser.add_argument('-r', '--reverse', action='store_true', help='Reverse block entries (Most Recent)')
    showHistoryParser.add_argument('-p', '--password', required=True, help='Password')

    #Remove
    removeParser = subParser.add_parser('remove')
    removeParser.add_argument('-i', '--item_id', required=True, help='Evidence item ID')
    removeParser.add_argument('-y', '--reason', required=True, help='Reason for removal')
    removeParser.add_argument('-p', '--password', required=True, help='Password')

    #Init
    initParser = subParser.add_parser('init')

    #Verify
    verifyParser = subParser.add_parser('verify')

    #Grab Commands
    args = mainParser.parse_args()

    #(TODO: Create a better implementation)
    #Tnit blockchain (temp: change in future)
    #Check absence of initial block or lack thereof
    #Maybe just check below in choices
    #blockchain = blockchain()

    #Call functions
    if args.choices == 'add':
        commandHandlers.handle_add(args)
    elif args.choices == 'checkout':
        commandHandlers.handle_checkout(args)
    elif args.choices == 'checkin':
        commandHandlers.handle_checkin(args)
    elif args.choices == 'show':
        if 'cases' in sys.argv:
            commandHandlers.handle_show_cases(args)
        elif 'items' in sys.argv:
            commandHandlers.handle_show_items(args)
        elif 'history' in sys.argv:
            commandHandlers.handle_show_history(args)
    elif args.choices == 'remove':
        commandHandlers.handle_remove(args)
    elif args.choices == 'init':
        commandHandlers.handle_init(args)
    elif args.choices == 'verify':
        commandHandlers.handle_verify(args)

if __name__ == "__main__":
    main()