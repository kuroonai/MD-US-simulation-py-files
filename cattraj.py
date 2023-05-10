# loc = '/project/6003277/vasudevn/model3/100gg/colvar/'
# s = '100gg'
# w = 0
# start = 0
# stop = 20

import os
import sys
import numpy as np
import glob
import pandas as pd

loc = sys.argv[1]
s = sys.argv[2]
w = sys.argv[3]
start = int(sys.argv[4])
stop = int(sys.argv[5])


os.chdir(loc+f'/{w}')

dzs = glob.glob('dz*')
reruns = sorted(list(filter(None, [i.split('dz')[1] for i in dzs])))
dzsort = [f'dz{i}' for i in reruns]

filenames = [f'{dz}/{s}{w}.colvars.traj' for dz in dzsort]
print(f'\n{filenames}')
with open(loc+f'{s}{w}.colvars.traj', 'w') as outfile:
    for fname in filenames:
        with open(fname) as infile:
            for line in infile:
                outfile.write(line)
    
data = np.loadtxt(loc+f'{s}{w}.colvars.traj')
a = pd.DataFrame(data)
#print(a)
a.columns = ['step','dist','0dist','work']
a = a.astype({'step':'float','dist':'float','0dist':'float','work':'float'})
a = a.drop_duplicates('step')

anew = a.iloc[start*1000:stop*1000]

print(f'\nsystem:{s} \nwindow:{w} \nlength_of_file:{len(anew)}\n')
np.savetxt(loc+f'/{s}{w}.colvars.traj', anew.values, fmt='%d %f %.2f %e')


