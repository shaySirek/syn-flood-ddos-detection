#! /bin/bash

echo simulating...
python3.10 src/simulate.py

echo estimating...
python3.10 src/main.py
