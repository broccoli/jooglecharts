'''
Created on Feb 2, 2017

@author: richd
'''
import unittest

from jooglechart.utils import break_string

class Test(unittest.TestCase):


    def test_break_string_1(self):
        
        # one word, less than limit
        s = 'xxx'
        limit = 5
        expected = ['xxx']
        
        self.assertEqual(break_string(s, limit), expected)


    def test_break_string_2(self):
        
        # one word, at limit
        s = 'xxxxx'
        limit = 5
        expected = ['xxxxx']
        
        self.assertEqual(break_string(s, limit), expected)


    def test_break_string_3(self):
        
        # one word, over limit
        s = 'xxxxxxx'
        limit = 5
        expected = ['xxxxxxx']
        
        self.assertEqual(break_string(s, limit), expected)


    def test_break_string_4(self):
        
        # two words, under limit
        s = 'xx x'
        limit = 5
        expected = ['xx x']
        
        self.assertEqual(break_string(s, limit), expected)


    def test_break_string_5(self):
        
        # one short word, one long word
        s = 'xx xxxxxxxxx'
        limit = 5
        expected = ['xx', 'xxxxxxxxx']
        
        self.assertEqual(break_string(s, limit), expected)


    def test_break_string_6(self):
        
        # one long word, one short word
        s = 'xxxxxx xx'
        limit = 5
        expected = ['xxxxxx', 'xx']
        
        self.assertEqual(break_string(s, limit), expected)

    def test_break_string_7(self):
        
        # multiple words of various length
        s = 'xx xxx xx xx xxxxxx x x x x'
        limit = 5
        expected = ['xx', 'xxx', 'xx xx', 'xxxxxx', 'x x x', 'x']
        
        self.assertEqual(break_string(s, limit), expected)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_break_string_1']
    unittest.main()