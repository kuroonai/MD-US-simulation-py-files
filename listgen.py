# loc = /lustre07/scratch/vasudevn/project/6003277/vasudevn/model3/100de/colvar
# s = 100de
# odd = 0 or 1

import os, sys
import numpy as np

loc = sys.argv[1]
s = sys.argv[2]
odd = int(sys.argv[3])

ms = np.linspace(2,20,37)

with open(f'{loc}/list.txt','w') as outfile:
    for w,m in enumerate(ms):
        if odd:
            if (w%2!=0): continue
        outfile.write(f'{s}{w}.colvars.traj {m} 7.0 60\n')