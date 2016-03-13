'''
Created on Dec 20, 2015

@author: richd
'''
import unittest

from juglechart.juglechart_api import Formatter, JoogleChartsException

class Test(unittest.TestCase):


    
    
    # test format type
    def test_format_type_001(self):
        
        f = Formatter("NumberFormat", options={'foo': 'bar'}, cols=[0, 1])
        expected = "NumberFormat"
        result = f.type
        self.assertEqual(expected, result)

    def test_format_type_002(self):
        
        f = Formatter("number", options={'foo': 'bar'}, cols=[0, 1])
        expected = "NumberFormat"
        result = f.type
        self.assertEqual(expected, result)

    def test_format_type_003(self):
        
        f = Formatter("DateFormat", options={'foo': 'bar'}, cols=[0, 1])
        expected = "DateFormat"
        result = f.type
        self.assertEqual(expected, result)

    def test_format_type_004(self):
        
        f = Formatter("date", options={'foo': 'bar'}, cols=[0, 1])
        expected = "DateFormat"
        result = f.type
        self.assertEqual(expected, result)

    def test_format_type_005(self):
        
        f = Formatter("BarFormat", options={'foo': 'bar'}, cols=[0, 1])
        expected = "BarFormat"
        result = f.type
        self.assertEqual(expected, result)

    def test_format_type_006(self):
        
        f = Formatter("bar", options={'foo': 'bar'}, cols=[0, 1])
        expected = "BarFormat"
        result = f.type
        self.assertEqual(expected, result)

    def test_format_type_007(self):
        
        f = Formatter("ArrowFormat", options={'foo': 'bar'}, cols=[0, 1])
        expected = "ArrowFormat"
        result = f.type
        self.assertEqual(expected, result)

    def test_format_type_008(self):
        
        f = Formatter("arrow", options={'foo': 'bar'}, cols=[0, 1])
        expected = "ArrowFormat"
        result = f.type
        self.assertEqual(expected, result)

    def test_format_type_009(self):
        
        f = Formatter("PatternFormat", pattern = "foo{0} {1}", source_cols=[0, 1])
        expected = "PatternFormat"
        result = f.type
        self.assertEqual(expected, result)

    def test_format_type_010(self):
        
        f = Formatter("pattern", pattern = "foo{0} {1}", source_cols=[0, 1])
        expected = "PatternFormat"
        result = f.type
        self.assertEqual(expected, result)

    def test_format_type_011(self):
        
        self.assertRaises(JoogleChartsException, Formatter, "ColorFormat", options={'foo': 'bar'}, cols=[0, 1])

    def test_format_type_012(self):
        
        self.assertRaises(JoogleChartsException, Formatter, "color", options={'foo': 'bar'}, cols=[0, 1])

    def test_format_type_013(self):
        
        # invalid format type
        self.assertRaises(JoogleChartsException, Formatter, "blah", options={'foo': 'bar'}, cols=[0, 1])

    
    def test_missing_kwargs_001(self):

        # missing options    
        self.assertRaises(JoogleChartsException, Formatter, "number", cols=[0, 1])
        
    def test_missing_kwargs_002(self):

        # missing cols        
        self.assertRaises(JoogleChartsException, Formatter, "number", options={'foo': 'bar'})

    def test_missing_kwargs_003(self):

        # missing source_cols
        self.assertRaises(JoogleChartsException, Formatter, "pattern")
        

    
    def test_pattern_format_001(self):
        
        f = Formatter("PatternFormat", pattern = "foo{0} {1}", source_cols=[1, 2])
        expected = 1
        result = f.dest_col
        self.assertEqual(expected, result)

    def test_pattern_format_002(self):
        
        f = Formatter("PatternFormat", pattern = "foo{0} {1}", source_cols=[1, 2], dest_col = 3)
        expected = 3
        result = f.dest_col
        self.assertEqual(expected, result)




if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()