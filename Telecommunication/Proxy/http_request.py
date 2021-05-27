class HttpRequest:
    """"Class representing http request"""

    def __init__(self, request):
        self.data = request
        line = str(request).split('\n')[0]
        self.method = line.split(' ')[0][2:]
        # URL: 'http://address:port'
        if len(line.split(' ')) < 2:
            return
        self.url = line.split(' ')[1]

        # Find '://'
        http_pos = self.url.find('://')

        # tmp: 'address:port'
        if http_pos == -1:
            tmp = self.url
        else:
            tmp = self.url[(http_pos + 3):]

        port_pos = tmp.find(':')
        server_pos = tmp.find('/')

        if server_pos == -1:
            server_pos = len(tmp)

        if port_pos == -1 or server_pos < port_pos:
            self.port = 80
            self.server = tmp[:server_pos]
        else:
            self.port = int((tmp[port_pos + 1:])[:server_pos - port_pos - 1])
            self.server = tmp[:port_pos]