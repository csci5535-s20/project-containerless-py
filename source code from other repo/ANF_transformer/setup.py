from setuptools import setup, find_packages
import os


thelibFolder = os.path.dirname(os.path.realpath(__file__))
requirementPath = thelibFolder + '/requirements.txt'
if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = list(f.read().splitlines())

setup(name="ANF_transformer", install_requires=install_requires, packages=find_packages())
