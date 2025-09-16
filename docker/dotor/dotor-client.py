import socket, dns, re, hmac, subprocess, dns.resolver, copy
import dns.message as dnsmessage
#from hashlib import sha1
debug = False
hostname_pattern = re.compile(r'^.+(?= IN A)')

def extract_hostname(data):
    message = dnsmessage.from_wire(data)
    hostname= hostname_pattern.search(message.sections[0][0].to_text()).group()
    return hostname, message.id


def extract_hostname(data):
    message = dnsmessage.from_wire(data)
    hostname= hostname_pattern.search(message.sections[0][0].to_text()).group()
    return hostname, message.id

def tor_socks5_handler(hostname):
    response = b''
    #Required greeting packet for SOCKS5
    greeting_raw = (b'\x05' + b'\x01' + b'\x00')  # SOCKS5, Nr. of methods: 1, NO AUTHENTICATION
    #Tor extends the SOCKS5 protocol with a RESOLVE command (0xF0) that we use here by replacing the adress with our question (domain)
    custom_packet= (
        b'\x05' + # SOCKS5
        b'\xF0' + # CMD: RESOLVE
        b'\x00' + # RSV (reserved because it just is)
        b'\x03' + # ATYP: DOMAINNAME
        bytes([len(hostname)]) + # length of domain
        hostname.encode('utf-8') + # domain
        b'\x00\x00' # Padding (2 bytes required but not used)
        )
    #print(f'custom_packet for {hostname}: {" ".join(hex(n) for n in custom_packet)}')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_out:
        
        #Establish connection to Tor SOCKS5
        s_out.connect(('localhost', 9050))
        s_out.sendall(greeting_raw)
        greeting_response = s_out.recv(2)
        if greeting_response!=b'\x05\x00':
            raise Exception(f'Error in greeting response from Tor SOCKS5: {greeting_response}') #Might need to fix to fail silently later
        #Resolve the hostname
        s_out.send(custom_packet)
        response = s_out.recv(1024)
        s_out.close()
        
    return response

def response_unpacker(data):
    
    result = {'Valid_response': True, 'Protocol': b'\x05', 'VER': b'\x00', 'RSV': b'\x00', 'ATYP': b'\x00', 'ADDR': b'\x00', 'IPv': 'None', 'Error': 'None', 'DNS-error': False}
    if data is Exception or isinstance(data, str):
        result['Valid_response'] = False
        result['Error'] = data
        return result
    if len(data) < 7:
        result['Valid_response'] = False
        result['Error'] = f'Response too short: {data}'
        return result
    if data[0:1] != b'\x05':
        result['Valid_response'] = False
        result['Error'] = f'Not SOCKS5 response: {data}'
        return result
    print(f'Debug: data response code: {data[1:2].hex()}')
    if data[1:2] != b'\x00':
        result['Valid_response'] = False
        if data[1:2] == b'\x04':
            result['Error'] = f'Host unreachable' #Used when resolve fails due to non existant domain
            result['DNS-error'] = True
        elif data[1:2] == b'\x01':
            result['Error'] = f'General SOCKS server failure' #Used when it fails to handle the hostname e.g. invalid format.
            result['DNS-error'] = True
        else:
            result['Error'] = f'Error in response, VER not 0: {data}'
        return result
    if data[2:3] != b'\x00':
        result['Valid_response'] = False
        result['Error'] = f'Error in response, RSV not 0: {data}'
        return result
    

    result['Protocol'] = data[0:1]
    result['VER'] = data[1:2]
    result['RSV'] = data[2:3]
    result['ATYP'] = data[3:4]
    if result['ATYP'] == b'\x01':  # IPv4
        result['IPv'] = 'IPv4'
        result['ADDR'] = '.'.join(str(b) for b in data[4:8])
    elif result['ATYP'] == b'\x04': # IPv6
        result['IPv'] = 'IPv6'
        result['ADDR'] = ':'.join(f'{data[i]:02x}{data[i+1]:02x}' for i in range(4, 20, 2))
    else:
        print(f'Unknown ATYP: {result["ATYP"]}')
        result['Valid_response'] = False
        result['Error'] = f'Did not get address of type IPv4 or IPv6, got code: {result["ATYP"].hex()}'

    return result

#Produces a dig compliant response for the given hostname (some shortcuts are taken, but the address is correct))
def fake_resolver(hostname, id, sample_response):
    print('Starting...\n\n')
     
    
    query_response = copy.deepcopy(sample_response)
    query_response.id = id
    query_response.question[0].name = dns.name.from_text(hostname)
    
        
    #Send the query
    response_raw = tor_socks5_handler(hostname)
    
    response_full = response_unpacker(response_raw)
    print(f'Unpacked response: {response_full}')

    if response_full['Valid_response']:
        query_response.set_rcode(dns.rcode.NOERROR)
        query_response.answer[0] = dns.rrset.from_text(hostname, 3600, 'IN', 'A', response_full['ADDR'])
    elif response_full['DNS-error']:
        # Usually means nothing found
        query_response.set_rcode(dns.rcode.NXDOMAIN)
        # Ensure no stale records leak from the base response
        query_response.answer.clear()
        query_response.authority.clear()
        query_response.additional.clear()
    else:
        #Something went wrong so we respond with servfail
        query_response.set_rcode(dns.rcode.SERVFAIL)
        query_response.answer.clear()
        query_response.authority.clear()
        query_response.additional.clear()

    return bytes(bytearray(query_response.to_wire()))


def main():
    #if debug: print(f'client running...\n')
    r_sample = dns.resolver.resolve('netnod.se')
    q_r_base = dnsmessage.from_wire(r_sample.response.to_wire())
    q_r = dns.message.from_wire(q_r_base.to_wire())
    if len(q_r.answer) < 1 or len(q_r.question) < 1:
        raise Exception(f'Error in sample query response from normal DNS resolve of netnod.se during startup phase: {q_r_base}')

    #test_response = subprocess.check_output(['tor-resolve', "netnod.se"])
    #if debug: print(f'test_response: {test_response.decode("utf-8").strip()} for domain netnod.se vs normal resolve: {q_r_base.answer[0]}\n')

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s_in:
        s_in.bind(('', 53))
        print('Listening on port 1337/udp for DNS queries...')
        while True:
            data, a = s_in.recvfrom(1024)
            print(f'Got data from {a}: {data}')
            client_host, client_port = a
            hostname, id = extract_hostname(data)
            q=fake_resolver(hostname, id, q_r) 
            print(f'{hostname} got response with id {id} from {client_host} at port {client_port}\nSent (id:{q_r.id}):\n{q}')
            s_in.sendto(q, a)


if __name__ == '__main__':
    main()
