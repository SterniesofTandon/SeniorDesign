import unittest


class TestOne(unittest.TestCase):

    def test_hello(self):
        print("\nHello World! Welcome to Sternies of Tandon\n")
        self.assertEqual(1, 1)


if __name__ == '__main__':
    unittest.main()
