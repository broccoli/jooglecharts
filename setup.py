'''
Created on Jan 10, 2016

@author: richd
'''

from setuptools import setup

setup(
    name='jooglechart',
    version='0.1.2',
    packages=['jooglechart',],
    package_data={'jooglechart': ['jinja_templates/*.html', '*.ipynb', 'jinja_templates/js/*.js', 'jinja_templates/css/*.css']},
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    description='Tool for creating Google Charts in Jupyter notebooks.',
    long_description=open('README.md').read(),
    author='Rich Doan',
    author_email='richd@indeed.com',
    install_requires=[
        'Jinja2==2.8',
#         'gviz_api==1.8.2',
        'IPython[notebook]>=4.0.0, <4.1.0',
        'pandas==0.15.2',
    ],
#     dependency_links = ['git+https://github.com/google/google-visualization-python.git#egg=gviz_api-1.8.2'],
    )