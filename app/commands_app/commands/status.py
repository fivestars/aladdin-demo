import requests
import os


def parse_args(sub_parser):
    subparser = sub_parser.add_parser("status", help="Report on the status of the application")
    # register the function to be executed when command "status" is called
    subparser.set_defaults(func=print_status)


def print_status(arg):
    """ Prints the status of the aladdin-demo pod and the redis pod """
    print_aladdin_demo_server_status()


def print_aladdin_demo_server_status():
    print("pinging aladdin-demo-server ...")
    host = os.environ["ALADDIN_DEMO_SERVER_SERVICE_HOST"]
    port = os.environ["ALADDIN_DEMO_SERVER_SERVICE_PORT"]
    url = "http://{}:{}/ping".format(host, port)
    try:
        r = requests.get(url)
        if r.status_code == 200:
            print("aladdin demo server endpoint ping successful")
        else:
            print("aladdin demo server endpoint ping returned with status code {}".format(r.status_code))
    except requests.exceptions.ConnectionError as e:
        print("aladdin demo endpoint connection error: {}".format(e))
