from setuptools import setup, find_packages

setup(
    name='flask-restful-paginate',
    version='0.1',
    packages=find_packages(),
    url='https://github.com/mtShaikh/flask-restful-paginate',
    license='MIT',
    author='mtShaikh',
    author_email='shaikh.taha95@gmail.com',
    description='Pagination extension for flask-restful',
    install_requires=[
        'flask-restful',
        'flask-sqlalchemy',
        'flask-restplus'
    ],
)
