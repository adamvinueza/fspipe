from setuptools import setup

setup(
    name='fspipe',
    version='0.6.0',
    description='Library for transforming data via streaming files',
    url='http://github.com/adamvinueza/fspipe',
    author='Adam Vinueza',
    author_email='adamvinueza@pm.me',
    license='MIT',
    packages=['fspipe'],
    install_requires=[
        'fsspec==0.8.0',
        'mypy-extensions==0.4.3', 's3fs==0.5.1',
    ],
    zip_safe=False,
)
