# Runtime Instrumentation of Python for Serverless Acceleration
## csci5535-s20/project-containerless-py

Course Project for CSCI5535 Programming Languages, Spring 2020

Dylan Fox & Erika Hunhoff


## Overview

This library provides a python tracing library for Containerless, a serverless function accelerator developed by Arjun Guha and Emily Herbert. See: https://arxiv.org/abs/1911.02178. This python library currenlty supports and extremely limited set of python, including arithmatic and boolean expressions, functions and if/else statements.

## How to Run

Make sure you are using Python 3.7. This library is not compatable with pre-3.7 python. 

Pip install all three python modules:
```
$ cd ANF_transformer
$ pip install .
$ cd ../py_transform
$ pip install .
$ cd ../tracing
$ pip install .
```

ANF_transformer also has pytests: for instructions, see ANF_transform/README.md

Once that is installed, you can create traces from python functions using run.py. For example,
```
./run.py -v -t -o examples/python/ -f examples/python/arithmetic.py
```
The above assumes your python instalation lives at `/usr/bin/python3.7`. If it is elsewhere, the below should be run:
```
python3 run.py -v -t -o examples/python/ -f examples/python/arithmetic.py
```


