'''
Created on Jan 10, 2016

@author: richd
'''

from setuptools import setup

setup(
    name='jooglechart',
    version='0.1',
    packages=['jooglechart',],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    description='Module for formatting dataframes and other common ishbook notebook outputs, in particular for styling and adding javascript to tables.',
    long_description=open('README.md').read(),
    author='Rich Doan',
    author_email='richd@indeed.com',
    install_requires=[
        'Jinja2==2.8',
        'gviz_api',
        'IPython[notebook]==4.0.0',
        'pandas',
    ],)