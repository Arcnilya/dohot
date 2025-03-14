import stem
import random
from stem.control import Controller
import argparse
import time

roles = ["entry", "middle", "exit"]

def list_circuits():
    with Controller.from_port(port = 9051) as controller:
        controller.authenticate()
        cid = ""
        for circ in controller.get_circuits():
            if circ.status != stem.CircStatus.BUILT:
                continue  # Only show active circuits

            if cid != circ.id: # new circ
                counter = 0
                cid = circ.id

            for relay in circ.path:
                desc = controller.get_network_status(relay[0], None)
                if desc:
                    location = controller.get_info("ip-to-country/%s" % desc.address, 'unknown')
                    role = roles[counter] if counter < len(roles) else "rp?"
                    print(f"{circ.id:<4} {desc.fingerprint:<40} {desc.address:<16} {desc.nickname:<20} {location:<2} {role:<6}")
                    counter += 1


def fetch_relay(targets, role="entry"):
    with Controller.from_port(port = 9051) as controller:
        controller.authenticate()

        while True:
            try:
                relays = list(controller.get_network_statuses())
                break
            except Exception as e: 
                time.sleep(5)


        random.shuffle(relays)
        for desc in relays:
            location = controller.get_info("ip-to-country/%s" % desc.address, 'unknown')
            if targets == "any" or location in targets.split(','):
                if role == "entry" and "Guard" in desc.flags:  
                    return desc.fingerprint
                elif role == "exit" and "Exit" in desc.flags:  
                    return desc.fingerprint


parser = argparse.ArgumentParser()
parser.add_argument('--circ', action='store_true', help='list current circuits')
parser.add_argument('--cc', default="", help='get a random relay from cc(s)')
parser.add_argument('--role', default="entry", help='select relay role (default: entry)')

args = parser.parse_args()

if args.circ:
    list_circuits()
elif args.cc: 
    fingerprint = fetch_relay(args.cc, args.role)
    print(fingerprint)
