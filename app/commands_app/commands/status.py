import requests
import os

from redis.exceptions import RedisError
from redis_util.redis_connection import ping_redis

def parse_args(sub_parser):
    subparser = sub_parser.add_parser("status", help="Report on the status of the application")
    # register the function to be executed when command "status" is called
    subparser.set_defaults(func=print_status)

def print_status(arg):
    """ Prints the status of the aladdin-demo pod and the redis pod """
    print_aladdin_demo_status()
    print_redis_status()

def print_aladdin_demo_status():
    print("pinging aladdin-demo ...")
    host = os.environ["ALADDIN_DEMO_SERVICE_HOST"]
    port = os.environ["ALADDIN_DEMO_SERVICE_PORT"]
    url = "http://{}:{}/ping".format(host, port)
    r = requests.get(url)
    if r.status_code == 200:
        print("aladdin demo endpoint ready")
    else:
        print("aladdin demo endpoint returned with status code {}".format(r.status_code))

def print_redis_status():
    # TODO have this ping external redis when that gets added
    print("pinging redis ...")
    if os.environ["REDIS_CREATE"] == "false":
        print("redis creation flag set to false, no other redis connection available at this time")
        return
    try: 
        status = ping_redis()
        print("redis connection ready {}".format(status))
    except RedisError as e:
        print("redis connection error: {}".format(e))
