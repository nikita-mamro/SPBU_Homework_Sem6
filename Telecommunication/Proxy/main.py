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

    config = {
        'HOST_NAME': '',
        'PORT': port,
        'MAX_CONNECTIONS': 10,
        'MAX_REQUEST_SIZE': 16384,
        'TIMEOUT': 5,
        'DOMAIN_BLACKLIST': ['neverssl.com']
    }

    server = ProxyServer(config)
    server.start()


if __name__ == '__main__':
    main()