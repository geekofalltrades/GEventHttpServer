import unittest
from http_server import *


# tests to see if non-get requests raise an exception
class ExceptionTest(unittest.TestCase):

    def testFailUnlessRaises(self):
        for s in ('POST /index.html HTTP/1.1 \r\n \
                        Host: www.example.com \r\n \
                        <CRLF>',
                    'PUT /index.html HTTP/1.1 \r\n \
                        Host: www.example.com \r\n \
                        <CRLF>',
                    'DELETE /index.html HTTP/1.1 \r\n \
                        Host: www.example.com \r\n \
                       <CRLF>'):
            self.failUnlessRaises(Error405, parse_request, s)


class EqualityTest(unittest.TestCase):
    def testEqual(self):
        tester = parse_request('GET /index.html HTTP/1.1 \r\n \
                        Host: www.example.com \r\n \
                        <CRLF>')
        self.assertEqual(tester, '/index.html')

if __name__ == '__main__':
    unittest.main()
