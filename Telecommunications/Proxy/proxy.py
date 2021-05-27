import socket
import sys
import logging
import threading

from Proxy.http_request import HttpRequest


class ProxyServer:
    """Class implementing HTTP proxy server with HTTPS support"""

    def __init__(self, config):
        self.config = config
        # Set properties from received configuration
        self.host_name = config['HOST_NAME']
        self.port = config['PORT']
        self.max_connections = config['MAX_CONNECTIONS']
        self.buffer_size = config['BUFFER_SIZE']
        self.domain_blacklist = config['DOMAIN_BLACKLIST']
        self.timeout = config['TIMEOUT']
        # AF_INET address family, stream socket type
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.start()

    def start(self):
        # Bind socket to host and port
        self.socket.bind((self.host_name, self.port))
        self.socket.listen(self.max_connections)
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
        data = client_socket.recv(self.buffer_size)
        request = HttpRequest(data)

        if data:
            # If domain is in blacklist, close connection
            for blocked_domain in self.domain_blacklist:
                if blocked_domain in request.url:
                    client_socket.close()
                    logging.info(f'Blocked domain: {blocked_domain}')
                    sys.exit(1)

            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.settimeout(self.timeout)

            if request.method == 'CONNECT':
                self.handle_https_request(request, client_socket, server_socket)
            else:
                self.handle_http_request(request, client_socket, server_socket)

    def handle_http_request(self, request, client_socket, server_socket):
        try:
            # Setup connection to destination and send copy of request
            server_socket.connect((request.host, request.port))
            server_socket.sendall(request.data)
            # Redirect response back to client
            while True:
                received_data = server_socket.recv(self.buffer_size)

                if len(received_data) > 0:
                    # Send data to client
                    client_socket.send(received_data)
                    logging.info(f'Served {request.method} client -> {request.host}')
                else:
                    break

            client_socket.close()
            server_socket.close()
        except socket.error as error:
            logging.error(f'Error serving HTTP request: {error}')
            if client_socket:
                client_socket.close()
            if server_socket:
                server_socket.close()

    def handle_https_request(self, request, client_socket, server_socket):
        # See: https://datatracker.ietf.org/doc/html/draft-luotonen-web-proxy-tunneling-01
        try:
            # Make connection to destination server
            server_socket.connect((request.host, request.port))
            response = "HTTP/1.1 200 Connection established\nProxy-agent: VeryCoolProxy/1.1\n\n"
            # Send Connection established response to client
            client_socket.sendall(response.encode())
        except socket.error as error:
            logging.error(f'Error serving HTTPS request: {error}')

        # Set non-blocking mode before starting tunneling
        client_socket.setblocking(False)
        server_socket.setblocking(False)

        # Data tunneling to both directions begins
        # The proxy response does not necessarily have a Content-Type field
        while True:
            try:
                data = client_socket.recv(self.buffer_size)
                if not data:
                    client_socket.close()
                    break
                server_socket.sendall(data)
            except socket.error:
                pass

            try:
                reply = server_socket.recv(self.buffer_size)
                if not reply:
                    server_socket.close()
                    break
                client_socket.sendall(reply)
                logging.info(f'Served {request.method} client -> {request.host}')
            except socket.error:
                pass
