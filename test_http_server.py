import unittest
from http_server import Error404, map_uri
from os import listdir


class TestMapUri(unittest.TestCase):
    """Test the uri mapping function. It should obtain a listing of the
    server's filesystem, check whether the file specified exists, and
    return the byte-representation of that file along with its mimetype
    code. These tests assume the use of the webroot directory provided
    in the assignment spec.
    """
    def setUp(self):
        self.directory_requested = '/images'
        self.image_requested = '/images/sample_1.png'
        self.text_requested = '/sample.txt'
        self.nonexistant_requested = '/iamnothere'

    def test_directory_requested(self):
        """Map a URI containing a request for a directory."""
        message, mimetype = map_uri(self.directory_requested)
        contents = listdir('webroot' + self.directory_requested)
        content_string = '\n'.join(contents)
        self.assertEqual(message, content_string)
        self.assertEqual(mimetype, 'text/plain')

    def test_image_file_requested(self):
        """Map a URI containing a request for an image file."""
        message, mimetype = map_uri(self.image_requested)

        with open('webroot' + self.image_requested, 'rb') as infile:
            expected = infile.read()

        self.assertEqual(message, expected)
        self.assertEqual(mimetype, 'image/png')

    def test_text_file_requested(self):
        """Map a URI containing a request for a text file."""
        message, mimetype = map_uri(self.text_requested)

        with open('webroot' + self.text_requested, 'rb') as infile:
            expected = infile.read()

        self.assertEqual(message, expected)
        self.assertEqual(mimetype, 'text/plain')

    def test_nonexistent_resource_requested(self):
        """Map a URI containing a request for a resource that doesn't
        exist.
        """
        self.assertRaises(Error404, map_uri, self.nonexistant_requested)


if __name__ == '__main__':
    unittest.main()
