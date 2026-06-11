from setuptools import setup

with open("README.md" , "r" , encoding="utf-8") as fh:
    long_description = fh.read()

AUTHOR_NAME = 'HARSH'
SRC_REPO = 'src'
LIST_OF_REQUIREMENTS = ['streamlit']

setup(
    name = SRC_REPO,
    version = '0.0.1',
    author = AUTHOR_NAME,
    author_email='pvtharshdeep@gmail.com',
    description='A simple python package to maek a simple web app for Movie Recommendation system',
    package = [SRC_REPO],
    python_requires = '>=3.7',
    install_requires= LIST_OF_REQUIREMENTS,

)