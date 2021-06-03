import logging
import argparse

from proxy import ProxyServer


def main():
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', dest='port', required=True, type=int)
    args = parser.parse_args()

    with open('domain_blacklist.txt', 'r') as f:
        domain_blacklist = f.read().split('\n')

    config = {
        'HOST_NAME': '',
        'PORT': args.port,
        'MAX_CONNECTIONS': 10,
        'BUFFER_SIZE': 16384,
        'TIMEOUT': 50,
        'DOMAIN_BLACKLIST': domain_blacklist
    }

    server = ProxyServer(config)
    server.start()


if __name__ == '__main__':
    main()
