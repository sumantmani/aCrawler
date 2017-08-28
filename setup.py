from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='uif-8') as f:
    long_description = f.read()

setup(
    name='aCrawler',
    version='0.0.1',
    url='https://github.com/sumantmani/aCrawler',
    author='Sumant Mani',
    author_email='sumant.mani@outlook.com',
    license='MIT',

    classifiers=[
        'Development Status :: 3 -Alpha',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='A simple web crawler',

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    install_requires=[],

    # $ pip install -e .[dev, test]
    extras_require={
        'dev': ['check-mainfest'],
        'test': ['coverage'],
    },
)
