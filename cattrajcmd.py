#loc wmin wmax s start stop
#/lustre07/scratch/vasudevn/project/6003277/vasudevn/model3/100de/colvar 0 36 100de 0 20

import os, sys

for i in range(int(sys.argv[2]), int(sys.argv[3])+1):
    print(f'python cattraj.py {sys.argv[1]} {sys.argv[4]} {i} {sys.argv[5]} {sys.argv[6]};')

