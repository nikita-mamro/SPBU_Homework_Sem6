import socket
import sys
import logging
import threading

from Proxy.http_request import HttpRequest


class ProxyServer:
    """Class implementing proxy server with HTTPS support"""
    def __init__(self, config):
        self.config = config
        # AF_INET address family, stream socket type
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.start()

    def start(self):
        # Bind socket to host and port
        self.socket.bind((self.config['HOST_NAME'], self.config['PORT']))
        self.socket.listen(self.config['MAX_CONNECTIONS'])
        while True:
            # Establish connection, address: (ip, port)
            client_socket, address = self.socket.accept()
            # Use separate thread to handle request
            d = threading.Thread(name=address, target=self.handle_request,
                                 args=(client_socket, address))
            d.setDaemon(True)
            d.start()

    def handle_request(self, client_socket, address):
        # Read request
        request = HttpRequest(client_socket.recv(self.config['MAX_REQUEST_SIZE']))

        if len(request.data) > 0:
            # If domain is in blacklist, close connection
            for blocked_domain in self.config['DOMAIN_BLACKLIST']:
                if blocked_domain in request.url:
                    client_socket.close()
                    logging.info(f'Blocked {blocked_domain}')
                    sys.exit(1)

            self.handle_http_request(request, client_socket, address)

    def handle_http_request(self, request, client_socket, address):
        try:
            # Setup connection to destination and send copy of request
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(self.config['TIMEOUT'])
            s.connect((request.server, request.port))
            s.sendall(request.data)
            # Redirect response back to client
            while True:
                received_data = s.recv(self.config['MAX_REQUEST_SIZE'])

                if len(received_data) > 0:
                    # Send data to client
                    client_socket.send(received_data)
                    logging.info(f'Served {request.method} request {address[0]} -> {request.server}')
                else:
                    break

            client_socket.close()
            s.close()
        except socket.error as error:
            logging.error(f'{address} - {error}')
            if client_socket:
                client_socket.close()
            if s:
                s.close()

    def handle_https_request(self, request, client_socket, address):
        return