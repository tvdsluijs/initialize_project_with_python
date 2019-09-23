
from setuptools import setup, find_packages

setup(
    name='create_project',
    version='0.1',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='A simple project creator',
    long_description=open('README.md').read(),
    install_requires=[],
    url='https://github.com/tvdsluijs/initialize_project_with_python',
    author='Theo van der Sluijs',
    author_email='theo@vandersluijs.nl'
)