import socket, dns, re, hmac, subprocess, dns.resolver
import dns.message as dnsmessage
#from hashlib import sha1
debug = True
hostname_pattern = re.compile(r'^.+(?= IN A)')

def extract_hostname(data):
    message = dnsmessage.from_wire(data)
    hostname= hostname_pattern.search(message.sections[0][0].to_text()).group()
    return hostname, message.id


def main():
    if debug: print(f'client running...\n')
    r_sample = dns.resolver.resolve('netnod.se')
    q_r_base = dnsmessage.from_wire(r_sample.response.to_wire())
    test_response = subprocess.check_output(['tor-resolve', "netnod.se"])
    if debug: print(f'test_response: {test_response.decode("utf-8").strip()} for domain netnod.se vs normal resolve: {q_r_base.answer[0]}\n')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s_in:
        s_in.bind(('', 1337))
        #s_in.listen()
        while True:
            data, a = s_in.recvfrom(1024)
            client_host, client_port = a
            hostname, id = extract_hostname(data)
            q_r = q_r_base.copy()
            if debug: print(f'DEBUG before: {q_r}\n--------\nID: {id}\n--------\n')
            q_r.id = id
            q_r.question[0].name = dns.name.from_text(hostname)
            if debug: print(f'DEBUG after: {q_r}\n--------\nqr.id: {q_r.id}\n--------\n')
            response = subprocess.check_output(['tor-resolve', hostname])
            q_r.answer[0] = (dns.rrset.from_text( hostname, 3600, 'IN', 'A', response.decode('utf-8').strip()))
            q = q_r.to_wire() 
            b_tmp = bytearray(q)
            
            q = bytes(b_tmp)
            print(f'{hostname} got response [{response}] with id {id} from {client_host} at port {client_port}\nSent (id:{q_r.id}):\n{q}\n{q_r}')
            s_in.sendto(q, a)


if __name__ == '__main__':
    main()
