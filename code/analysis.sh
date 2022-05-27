#!/bin/bash

# exit on first error
set -e

# area, dry period length, percentile, min event length, 
# min number for fitting, number of durations

# Harz
python code/main.py HARZ 24 75 3 10 5 &
python code/main.py HARZ 30 75 3 10 5 &
python code/main.py HARZ 36 75 3 10 5 &
python code/main.py HARZ 24 50 3 10 5 &
python code/main.py HARZ 30 50 3 10 5 &
python code/main.py HARZ 36 50 3 10 5 &

# Erzgebirge
python code/main.py ERZGEBIRGE 24 75 3 10 5 &
python code/main.py ERZGEBIRGE 30 75 3 10 5 &
python code/main.py ERZGEBIRGE 36 75 3 10 5 &
python code/main.py ERZGEBIRGE 24 50 3 10 5 &
python code/main.py ERZGEBIRGE 30 50 3 10 5 &
python code/main.py ERZGEBIRGE 36 50 3 10 5 &

# Schwarzwald
python code/main.py SCHWARZWALD 24 75 3 10 5 &
python code/main.py SCHWARZWALD 30 75 3 10 5 &
python code/main.py SCHWARZWALD 36 75 3 10 5 &
python code/main.py SCHWARZWALD 24 50 3 10 5 &
python code/main.py SCHWARZWALD 30 50 3 10 5 &
python code/main.py SCHWARZWALD 36 50 3 10 5