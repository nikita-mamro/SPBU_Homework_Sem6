import logging
import argparse
import sys

from proxy import ProxyServer


def main():
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', required=True,
                        type=int, help='Port number for proxy')
    parser.add_argument('-mc', '--max_connections',
                        required=False, type=int, help='Max connections')
    parser.add_argument('-dbl', '--domain_blacklist', required=False, type=str, help='Path to file with domains to '
                                                                                     'be blocked written line by '
                                                                                     'line')
    args = parser.parse_args()

    try:
        with open(args.domain_blacklist if args.domain_blacklist else 'domain_blacklist.txt', 'r') as f:
            domain_blacklist = f.read().split('\n')
    except:
        logging.error(
            f'Could not load domain blacklist from {args.domain_blacklist}')
        sys.exit(1)

    config = {
        'HOST_NAME': '',
        'PORT': args.port,
        'MAX_CONNECTIONS': args.max_connections if args.max_connections else 10,
        'BUFFER_SIZE': 16384,
        'DOMAIN_BLACKLIST': domain_blacklist
    }

    server = ProxyServer(config)
    server.start()


if __name__ == '__main__':
    main()
