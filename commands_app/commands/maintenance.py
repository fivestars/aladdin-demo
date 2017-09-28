
def parse_args(sub_parser):
    subparser = sub_parser.add_parser("maintenance", help="print 'Entering maintenance mode' ")
    subparser.set_defaults(func=start_maintenance)

def start_maintenance(arg):
    print("Entering maintenance mode")
    # do some other stuff???