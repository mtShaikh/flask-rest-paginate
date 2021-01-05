from importlib import util

from setuptools import setup, find_packages

from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

install_requires = ['flask-sqlalchemy', 'flask-restful']

setup(
    name='flask-rest-paginate',
    version='1.1.1',
    packages=find_packages(),
    url='https://github.com/mtShaikh/flask-rest-paginate',
    license='MIT',
    author='mtShaikh',
    author_email='shaikh.taha95@gmail.com',
    description='Pagination extension for flask-restful',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    keywords='rest flask-restful pagination flask',
    install_requires=install_requires,
)
