'''
Created on Dec 12, 2015

@author: richd
'''
import unittest

import pandas as pd

from juglechart.juglechart_api import JugleChart, PythonGoogleChartsException

class Test(unittest.TestCase):


    cities = ['Seattle', 'Chicago', 'Phoenix', 'Atlanta']
    nums = [45, 74, 33, 50]

    df1 = pd.DataFrame({'cities': cities, 'nums': nums}, columns=['cities', 'nums'])

    def test_flat_vals_001(self):
        
        gchart = JugleChart(self.df1)
        gchart.add_chart_options(a=1)
        
        expected = {'a': 1}
        actual = gchart.chart_options
        
        self.assertEqual(expected, actual)
        

    def test_flat_vals_002(self):
        
        gchart = JugleChart(self.df1)
        gchart.add_chart_options(a=1)
        gchart.add_chart_options(b=2)
        
        expected = {'a': 1, 'b': 2}
        actual = gchart.chart_options
        
        self.assertEqual(expected, actual)
        
        
    def test_flat_vals_003(self):
        
        gchart = JugleChart(self.df1)
        gchart.add_chart_options(a=1)
        gchart.add_chart_options(a=2)
        
        expected = {'a': 2}
        actual = gchart.chart_options
        
        self.assertEqual(expected, actual)
        
    def test_flat_vals_004(self):
        
        gchart = JugleChart(self.df1)
        gchart.add_chart_options({'a': 1})
        
        expected = {'a': 1}
        actual = gchart.chart_options
        
        self.assertEqual(expected, actual)
        

    def test_flat_vals_005(self):
        
        gchart = JugleChart(self.df1)
        gchart.add_chart_options(a=1, b=2)
        
        expected = {'a': 1, 'b': 2}
        actual = gchart.chart_options
        
        self.assertEqual(expected, actual)
        

    def test_flat_vals_006(self):
        
        gchart = JugleChart(self.df1)
        gchart.add_chart_options(options={'c': 3}, a=1, b=2)
        
        expected = {'a': 1, 'b': 2, 'c': 3}
        actual = gchart.chart_options
        
        self.assertEqual(expected, actual)


    def test_flat_vals_007(self):
        
        gchart = JugleChart(self.df1)
        gchart.add_chart_options(a=1)
        gchart.add_chart_options({'b': 2, 'c': 4})
        
        expected = {'a': 1, 'b': 2, 'c': 4}
        actual = gchart.chart_options
        
        self.assertEqual(expected, actual)

    
    
    def test_nested_vals_001(self):

        # Add a nested dictionary with underscore notation in kwarg
        gchart = JugleChart(self.df1)
        gchart.add_chart_options(a_b = 1)
        
        expected = {'a': {'b': 1}}
        actual = gchart.chart_options
        
        self.assertEqual(expected, actual)

    def test_nested_vals_002(self):

        # Add a nested dictionary with underscore notation in key
        gchart = JugleChart(self.df1)
        gchart.add_chart_options({'a_b':1})
        
        expected = {'a': {'b': 1}}
        actual = gchart.chart_options
        
        self.assertEqual(expected, actual)


    def test_nested_vals_003(self):
        
        # Add a nested dictionary with dot notation in key

        gchart = JugleChart(self.df1)
        gchart.add_chart_options({'a.b':1})
        
        expected = {'a': {'b': 1}}
        actual = gchart.chart_options
        
        self.assertEqual(expected, actual)

    def test_nested_vals_004(self):
        # Add a nested dictionary with three levels

        gchart = JugleChart(self.df1)
        gchart.add_chart_options(a_b_c = 1)
        
        expected = {'a': {'b': {'c': 1}}}
        actual = gchart.chart_options
        
        self.assertEqual(expected, actual)

    def test_nested_vals_005(self):
        # Combine two nested dictionaries

        gchart = JugleChart(self.df1)
        gchart.add_chart_options(a_b = 1)
        gchart.add_chart_options(a_c = 2)
        
        expected = {'a': {'b': 1, 'c': 2}}
        actual = gchart.chart_options
        
        self.assertEqual(expected, actual)


    def test_nested_vals_006(self):

        # Overwrite a nested scalar with a dictionary
        gchart = JugleChart(self.df1)
        gchart.add_chart_options(a_b = 1)
        gchart.add_chart_options(a_b_c = 2)
        
        expected = {'a': {'b': {'c': 2}}}
        actual = gchart.chart_options
        
        self.assertEqual(expected, actual)

    
    def test_nested_vals_007(self):

        # Overwrite a nested dictionary with a scalar
        gchart = JugleChart(self.df1)
        gchart.add_chart_options(a_b_c = 2)
        gchart.add_chart_options(a_b = 1)
        
        expected = {'a': {'b': 1}}
        actual = gchart.chart_options
        
        self.assertEqual(expected, actual)

    def test_nested_vals_008(self):

        # Overwrite one nested item scalar with another
        gchart = JugleChart(self.df1)
        gchart.add_chart_options(a_b = 2)
        gchart.add_chart_options(a_b = 1)
        
        expected = {'a': {'b': 1}}
        actual = gchart.chart_options
        
        self.assertEqual(expected, actual)

    def test_nested_vals_009(self):

        # Add dictionary that has multiple items at lower level
        gchart = JugleChart(self.df1)
        gchart.add_chart_options(a_b = 2)
        gchart.add_chart_options({'a': {'c': 3, 'd': 4}})
        
        expected = {'a': {'b': 2, 'c': 3, 'd': 4}}
        actual = gchart.chart_options
        
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
#     unittest.main()
    
    suite = unittest.TestSuite()
    suite.addTest(Test('test_flat_vals_005'))
    unittest.TextTestRunner().run(suite)
    
