'''
Created on Jan 10, 2016

@author: richd
'''

from setuptools import setup

setup(
    name='jooglechart',
    version='0.1',
    packages=['jooglechart',],
    package_data={'mypkg': ['jinja_templates/*.html', '*.ipynb']},
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    description='Module for formatting dataframes and other common ishbook notebook outputs, in particular for styling and adding javascript to tables.',
    long_description=open('README.md').read(),
    author='Rich Doan',
    author_email='richd@indeed.com',
    install_requires=[
        'Jinja2==2.8',
        'gviz_api.py==1.8.2',
        'IPython[notebook]==4.0.0',
        'pandas',
    ],
    dependency_links = ['git+https://github.com/google/google-visualization-python.git#egg=gviz_api-1.8.2'],
    )