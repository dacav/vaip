#!/bin/sh
python3 -m unittest discover -t vaip/ -s vaip/tests -p '*.py' -v $@ 2>&1
