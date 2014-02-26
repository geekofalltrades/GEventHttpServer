#! /usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import http_server
from email.utils import formatdate


class testHTTPserver(unittest.TestCase):

    def test_build_response_txt(self):
        """Tests whether the response for a directory request is correct"""
        self.assertEqual('HTTP/1.1 200 OK\r\n\
Date: %s\r\n\
Server: Team Python\r\n\
Content-Type: text/plain; char=UTF-8\r\n\
Content-Length: 52\r\n\
\r\n\
JPEG_example.jpg\n\
sample_1.png\n\
Sample_Scene_Balls.jpg' % formatdate(usegmt=True),
http_server.build_response(
'JPEG_example.jpg\nsample_1.png\nSample_Scene_Balls.jpg',
'text/plain'))

    def test_build_response_unitxt(self):
        """Tests whether encoding is done properly and whether response is correct"""
        self.assertEqual('HTTP/1.1 200 OK\r\n\
Date: %s\r\n\
Server: Team Python\r\n\
Content-Type: text/plain; char=UTF-8\r\n\
Content-Length: 4\r\n\
\r\n\
ol\xc3\xa8' % formatdate(usegmt=True),
http_server.build_response(u'olè', 'text/plain'))

if __name__ == '__main__':
    unittest.main()
