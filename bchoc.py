# Completed main script file
# Parses command line commands
# Calls the wrapper interface commandHandlers.py

import argparse
import os
import commandHandlers

def main():
    # Hardcoded environmental variables for local testing
    os.environ['AES_KEY'] = 'R0chLi4uLi4uLi4='
    os.environ['BCHOC_PASSWORD_POLICE'] = 'P80P'
    os.environ['BCHOC_PASSWORD_LAWYER'] = 'L76L'
    os.environ['BCHOC_PASSWORD_ANALYST'] = 'A65A'
    os.environ['BCHOC_PASSWORD_EXECUTIVE'] = 'E69E'
    os.environ['BCHOC_PASSWORD_CREATOR'] = 'C67C'
    
    #Setup parsers
    mainParser = argparse.ArgumentParser(description='CSE469 Chain of Custody')
    subParser = mainParser.add_subparsers(dest='choices', required=True)

    #Adding
    addParser = subParser.add_parser('add')
    addParser.add_argument('-c', '--case_id', required=True, help='Case ID (UUID)')
    addParser.add_argument('-i', '--item_id', action='append', required=True, help='Evidence item ID')
    addParser.add_argument('-g', '--creator', required=True, help='Creator')
    addParser.add_argument('-p', '--password', required=True, help='Password')

    #Checkout
    checkoutParser = subParser.add_parser('checkout')
    checkoutParser.add_argument('-i', '--item_id', required=True, help='Evidence item ID')
    checkoutParser.add_argument('-p', '--password', required=True, help='Password')

    #Checkin
    checkinParser = subParser.add_parser('checkin')
    checkinParser.add_argument('-i', '--item_id', required=True, help='Evidence item ID')
    checkinParser.add_argument('-p', '--password', required=True, help='Password')

    #Show parser
    showParser = subParser.add_parser('show')
    showSubparser = showParser.add_subparsers(dest='show_choice', required=True)
    
    # Show cases
    showSubparser.add_parser('cases', help='Show all cases')

    #Show items
    showItemsParser = showSubparser.add_parser('items', help='Show all items in a case')
    showItemsParser.add_argument('-c', '--case_id', required=True, help='Case ID (UUID)')

    #Show history
    showHistoryParser = showSubparser.add_parser('history', help='Show history of a case or item')
    showHistoryParser.add_argument('-c', '--case_id', help='Case ID')
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
    subParser.add_parser('init')
    #Verify
    subParser.add_parser('verify')
    #Grab Commands
    args = mainParser.parse_args()

    if args.choices == 'add':
        commandHandlers.handle_add(args)
    elif args.choices == 'checkout':
        commandHandlers.handle_checkout(args)
    elif args.choices == 'checkin':
        commandHandlers.handle_checkin(args)
    elif args.choices == 'show':
        if args.show_choice == 'cases':
            commandHandlers.handle_show_cases()
        elif args.show_choice == 'items':
            commandHandlers.handle_show_items(args)
        elif args.show_choice == 'history':
            commandHandlers.handle_show_history(args)
    elif args.choices == 'remove':
        commandHandlers.handle_remove(args)
    elif args.choices == 'init':
        commandHandlers.handle_init()
    elif args.choices == 'verify':
        commandHandlers.handle_verify(args)

if __name__ == "__main__":
    main()