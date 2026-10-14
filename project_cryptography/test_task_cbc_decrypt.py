import unittest

from project_cryptography import cbc_decrypt_128

class TestCBCDecrypt(unittest.TestCase):
    def test_1(self):
        c_expected = 'hello world'

        c = cbc_decrypt_128(b'this key is 16bs', b'1010101010101010', b'\x84\xff\x01\x9f\xc8y\xe1$\xcc\xeb\x8dP\xd8c\x14\xfd')

        self.assertEqual(c, c_expected)

if __name__ == '__main__':
    unittest.main()
