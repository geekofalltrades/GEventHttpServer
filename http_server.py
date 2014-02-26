from email.utils import formatdate
from mimetypes import guess_type
import socket
from os.path import isfile, isdir
from os import listdir, getcwd
from gevent.server import StreamServer
from gevent.monkey import patch_all


def http_server(sock, addr):
    """Handler for http server requests."""
    while True:
        try:
            msg = receive_message(sock)
            uri = parse_request(msg)
            resource, mimetype = map_uri(uri)

        except (Error404, Error405) as e:
            response = build_response(e.message, 'text/plain', e.code)

        except:
            response = build_response("500 Internal Server Error",
                'text/plain', '500')

        else:
            response = build_response(resource, mimetype)

        finally:
            sock.sendall(response)
           # conn.shutdown(socket.SHUT_WR)
           # sock.close()


def receive_message(conn, buffsize=4096):
    """When a connection is received by the http_server, this function
    pieces together the message received and returns it.
    """

    msg = ''
    while True:
        msg_part = conn.recv(buffsize)
        msg += msg_part
        if len(msg_part) < buffsize:
            break

    conn.shutdown(socket.SHUT_RD)

    return msg


def parse_request(request):
    first_rn = request.find('\r\n')
    first_line = request[:first_rn]
    if first_line.split()[0] == 'GET':
        uri = first_line.split()[1]
        return uri
    else:
        raise Error405("405: Method not allowed. Only GET is allowed.")


def map_uri(uri):
    """Given a uri, looks up the corresponding file in the file system.
    Returns a tuple containing the byte-string represenation of its
    contents and its mimetype code.
    """
    #URIs come in based in root. Make root the 'webroot' directory.
    filepath = 'webroot' + uri

    if isfile(filepath):
        with open(filepath, 'rb') as infile:
            message = infile.read()

        return (message, guess_type(filepath)[0])

    if isdir(filepath):
        contents = listdir(filepath)
        for i in range(len(contents)):
            if isdir('%s/webroot/%s' % (getcwd(), contents[i])):
                contents[i] += '/'
        return ('\n'.join(contents), 'text/plain')

    #If what we received was not a file or a directory, raise an Error404.
    raise Error404("404: File not found.")


def build_response(message, mimetype, code="200 OK"):
    """Build a response with the specified code and content."""

    # Headers should all be ascii
    if not isinstance(message, bytes):
        message = message.encode('utf-8')
    bytelen = len(message)
    resp_list = []
    resp_list.append('HTTP/1.1 %s' % code)
    resp_list.append('Date: %s' % formatdate(usegmt=True))
    resp_list.append('Server: Team Python')
    resp_list.append('Content-Type: %s; char=UTF-8' % mimetype)
    resp_list.append('Content-Length: %s' % str(bytelen))
    resp_list.append('\r\n%s' % message)
    resp = '\r\n'.join(resp_list)
    return resp


class Error404(BaseException):
    """Exception raised when a file specified by a URI does not exist."""
    code = '404'


class Error405(BaseException):
    """Exception raised when a request is made with a method other than GET."""
    code = '405'


if __name__ == '__main__':
    patch_all()
    server = StreamServer(('127.0.0.1', 50000), http_server)
    print('Starting server on port 50000')
    server.serve_forever()
