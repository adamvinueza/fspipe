from setuptools import setup

setup(
    name='fspipe',
    version='0.2.0',
    description='Library for transforming data via streaming files',
    url='http://github.com/adamvinueza/fspipe',
    author='Adam Vinueza',
    author_email='adamvinueza@pm.me',
    license='MIT',
    packages=['fspipe'],
    install_requires=[
        'fsspec==0.8.3',
        'mypy-extensions==0.4.3',
        's3fs==0.5.1',
        'paramiko==2.7.2'
    ],
    zip_safe=False,
)
