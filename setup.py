from setuptools import setup, find_packages

setup(
    name='flask-rest-paginate',
    version='0.1',
    packages=find_packages(),
    url='https://github.com/mtShaikh/flask-rest-paginate',
    license='MIT',
    author='mtShaikh',
    author_email='shaikh.taha95@gmail.com',
    description='Pagination extension for flask-restful and flask-restplus',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    install_requires=[
        'flask-restful',
        'flask-sqlalchemy',
        'flask-restplus'
    ],
)
