import subprocess
from stem.control import Controller, EventType
from collections import defaultdict
import threading

circuit_info = {}
stream_to_circuit = defaultdict(lambda: None)

def print_circuit(circ_id):
    path = circuit_info.get(circ_id)
    if path:
        print(f"[+] Circuit {circ_id} relays:")
        for i, (fp, name) in enumerate(path):
            print(f"   [{i}] {name} ({fp})")
    else:
        print(f"[!] Circuit {circ_id} info not yet available.")


def stream_event_handler(event):
    circ_id = event.circ_id
    if circ_id:
        stream_to_circuit[event.id] = circ_id
        print(f"\n[+] Stream {event.id} is using circuit {circ_id}")
        print_circuit(circ_id)


def main():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate()
        print("[*] Listening for Tor stream events...\n")
        controller.add_event_listener(stream_event_handler, EventType.STREAM)
        threading.Event().wait()


if __name__ == "__main__":
    main()

