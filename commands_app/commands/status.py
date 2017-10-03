import socket

def parse_args(sub_parser):
    subparser = sub_parser.add_parser("status", help="Report on the status of the application")
    subparser.set_defaults(func=print_status)

def print_status(arg):
    if socket.gethostbyname("aladdin-demo"):
        print("Aladdin demo app up and ready")
    else:
        print("Cannot find aladdin demo app, possible errors may have occurred")
    if socket.gethostbyname("aladdin-demo-redis"):
        print("Redis server up and ready")
    else: print("Cannot find redis server")
