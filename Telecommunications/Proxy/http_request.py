class HttpRequest:
    """"Class representing http request"""

    def __init__(self, data):
        self.data = data
        line = str(self.data).split('\n')[0]
        if len(line.split(' ')) < 2:
            return

        # URL: 'http://address:port'
        self.method = line.split(' ')[0][2:]
        self.url = line.split(' ')[1]

        # Find '://'
        http_pos = self.url.find('://')

        # tmp: 'address:port'
        if http_pos == -1:
            tmp = self.url
        else:
            tmp = self.url[(http_pos + 3):]

        port_pos = tmp.find(':')
        host_pos = tmp.find('/')

        if host_pos == -1:
            host_pos = len(tmp)

        if port_pos == -1 or host_pos < port_pos:
            self.port = 80
            self.host = tmp[:host_pos]
        else:
            self.port = int((tmp[port_pos + 1:])[:host_pos - port_pos - 1])
            self.host = tmp[:port_pos]