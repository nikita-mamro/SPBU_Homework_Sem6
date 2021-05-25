import signal
import socket
import sys
import logging
import threading


class ProxyServer:
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
        method = line.split(' ')[0]
        # URL: 'http://address:port'
        if len(line.split(' ')) < 2:
            return
        url = line.split(' ')[1]

        for blocked_domain in self.config['DOMAIN_BLACKLIST']:
            if blocked_domain in url:
                client_socket.close()
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
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(self.config['TIMEOUT'])
            s.connect((server, port))
            s.sendall(request)

            while True:
                received_data = s.recv(self.config['MAX_REQUEST_SIZE'])

                if len(received_data) > 0:
                    client_socket.send(received_data)
                    logging.info(f'Served request {client_address[0]} -> {server}')
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


def main():
    logging.basicConfig(level=logging.INFO)
    try:
        port = int(input('Enter port for listening: '))
    except ValueError:
        logging.ERROR('Unable to process input')
        sys.exit(0)

    config = {
        'HOST_NAME': '',
        'PORT': port,
        'MAX_CONNECTIONS': 10,
        'MAX_REQUEST_SIZE': 4096,
        'TIMEOUT': 5,
        'DOMAIN_BLACKLIST': ['neverssl.com']
    }

    server = ProxyServer(config)
    server.start()


if __name__ == '__main__':
    main()
