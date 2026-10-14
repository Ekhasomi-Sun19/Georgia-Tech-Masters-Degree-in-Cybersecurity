import unittest

from project_cryptography import cbc_pkcs_padding

class TestCBCDecrypt(unittest.TestCase):
    def test_1(self):
        padding_expected = False

        padding = cbc_pkcs_padding(b'\xb6\x03\x03')

        self.assertEqual(padding, padding_expected)

    def test_2(self):
        padding_expected = True

        padding = cbc_pkcs_padding(b'\xb6\x02\x02')

        self.assertEqual(padding, padding_expected)

if __name__ == '__main__':
    unittest.main()
