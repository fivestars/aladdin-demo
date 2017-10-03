import socket

def parse_args(sub_parser):
    subparser = sub_parser.add_parser("status", help="Report on the status of the application")
    # register the function to be executed when command "status" is called
    subparser.set_defaults(func=print_status)

def print_status(arg):
    """ Prints the status of the aladdin-demo pod and the redis pod """
    if socket.gethostbyname("aladdin-demo"):
        print("Aladdin demo app up and ready")
    else:
        print("Cannot find aladdin demo app, possible errors may have occurred")
    if socket.gethostbyname("aladdin-demo-redis"):
        print("Redis server up and ready")
    else: print("Cannot find redis server")
