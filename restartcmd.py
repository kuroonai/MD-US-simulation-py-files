#loc wmin wmax multi submit

import os, sys

for i in range(int(sys.argv[2]), int(sys.argv[3])+1):
    print(f'python restart.py {sys.argv[1]} {i} {sys.argv[4]} {sys.argv[5]};')

