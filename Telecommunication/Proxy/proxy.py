import socket
import sys
import logging
import threading


class ProxyServer:
    """Class implementing proxy server with HTTP support"""
    def __init__(self, config):
        self.config = config
        # AF_INET address family, stream socket type
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Bind socket to host and port
        self.socket.bind((config['HOST_NAME'], config['PORT']))
        self.socket.listen(config['MAX_CONNECTIONS'])
        self.start()

    def start(self):
        while True:
            # Establish connection, address: (ip, port)
            client_socket, client_address = self.socket.accept()
            # Use separate thread to handle request
            d = threading.Thread(name=client_address, target=self.proxy_thread,
                                 args=(client_socket, client_address))
            d.setDaemon(True)
            d.start()
        self.shutdown()

    def proxy_thread(self, client_socket, client_address):
        # Read request
        request = client_socket.recv(self.config['MAX_REQUEST_SIZE'])
        line = str(request).split('\n')[0]
        method = line.split(' ')[0][2:]
        # URL: 'http://address:port'
        if len(line.split(' ')) < 2:
            return
        url = line.split(' ')[1]
        # If domain is in blacklist, close connection
        for blocked_domain in self.config['DOMAIN_BLACKLIST']:
            if blocked_domain in url:
                client_socket.close()
                logging.info(f'Blocked {blocked_domain}')
                sys.exit(1)

        # Find '://'
        http_pos = url.find('://')

        # tmp: 'address:port'
        if http_pos == -1:
            tmp = url
        else:
            tmp = url[(http_pos + 3):]

        port_pos = tmp.find(':')
        server_pos = tmp.find('/')

        if server_pos == -1:
            server_pos = len(tmp)

        if port_pos == -1 or server_pos < port_pos:
            port = 80
            server = tmp[:server_pos]
        else:
            port = int((tmp[port_pos + 1:])[:server_pos - port_pos - 1])
            server = tmp[:port_pos]

        try:
            # Setup connection to destination and send copy of request
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(self.config['TIMEOUT'])
            s.connect((server, port))
            s.sendall(request)
            # Redirect response back to client
            while True:
                received_data = s.recv(self.config['MAX_REQUEST_SIZE'])

                if len(received_data) > 0:
                    # Send data to client
                    client_socket.send(received_data)
                    logging.info(f'Served {method} request {client_address[0]} -> {server}')
                else:
                    break

            client_socket.close()
            s.close()
        except socket.error as error:
            logging.error(f'{client_address} - {error}')
            if client_socket:
                client_socket.close()
            if s:
                s.close()

    def shutdown(self):
        self.socket.close()
        main_thread = threading.currentThread()
        for t in threading.enumerate():
            if t is main_thread:
                continue
            t.join()
            self.socket.close()
        sys.exit(0)
