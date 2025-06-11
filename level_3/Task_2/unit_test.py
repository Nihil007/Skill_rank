# import unittest
import unittest

# import result from freq_element
from freq_elements import mostfrequent

# unittest to test 
class mostfrequentelements(unittest.TestCase):

    def testcase1(self):
        self.assertEqual(mostfrequent([1, 1, 1, 2, 2, 3], 1), [1])

    def testcase2(self):
        self.assertEqual(mostfrequent([5, 5, 5, 5], 1), [5])

    def testcase3(self):
        # used count equal to accept any order
        self.assertCountEqual(mostfrequent([1, 2, 3, 4, 5], 3), [1, 2, 3])
        
    def testcase4(self):
        self.assertEqual(mostfrequent([42], 1), [42])

    def testcase5(self):
        # used count equal to accept any order
        self.assertCountEqual(mostfrequent([1, 2, 3], 5), [1, 2, 3])

    def testcase6(self):
        self.assertEqual(mostfrequent([3, 0, 1, 0], 1), [0])

    def testcase7(self):
        self.assertEqual(mostfrequent([7, 10, 11, 5, 2, 5, 5, 7, 11, 8, 9], 1), [5])

if __name__ == '__main__':
    unittest.main()