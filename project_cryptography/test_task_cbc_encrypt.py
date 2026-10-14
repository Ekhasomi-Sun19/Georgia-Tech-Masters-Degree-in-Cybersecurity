import unittest

from project_cryptography import cbc_encrypt_128

class TestCBCEncrypt(unittest.TestCase):
    def test_1(self):
        c_expected = 'hP8Bn8h54STM641Q2GMU/Q=='

        c = cbc_encrypt_128(b'this key is 16bs', b'1010101010101010','hello world')
        self.assertEqual(c, c_expected)

if __name__ == '__main__':
    unittest.main()
