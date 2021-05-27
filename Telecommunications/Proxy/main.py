import logging
import sys

from Proxy.proxy import ProxyServer


def main():
    logging.basicConfig(level=logging.INFO)
    try:
        port = int(input('Enter port for listening: '))
    except ValueError:
        logging.ERROR('Unable to process input')
        sys.exit(0)

    with open('domain_blacklist.txt', 'r') as f:
        domain_blacklist = f.read().split('\n')

    config = {
        'HOST_NAME': '',
        'PORT': port,
        'MAX_CONNECTIONS': 10,
        'BUFFER_SIZE': 16384,
        'TIMEOUT': 50,
        'DOMAIN_BLACKLIST': domain_blacklist
    }

    server = ProxyServer(config)
    server.start()


if __name__ == '__main__':
    main()
