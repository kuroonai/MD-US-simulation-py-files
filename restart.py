# /project/6003277/vasudevn/model3/100lg/colvar # location
# 1 # window
# 1.0 # new time multiple of 5mil

import os
import sys
import glob
import numpy as np
import math

loc = sys.argv[1]
win = sys.argv[2]
multi = float(sys.argv[3])
subm = sys.argv[4]

os.chdir(loc+f'/{win}')

dzs = glob.glob('dz*')
reruns = sorted(list(filter(None, [i.split('dz')[1] for i in dzs])))

if os.path.isdir('dz') and reruns == [] :  
    os.rename('dz','dz1')
    newrun = 1
    laststep = int(np.loadtxt(f'dz1/polcom.txt')[-1][0])
    os.system(f'lmp -r2data ./dz1/crystal.restart2 {laststep}.data')

elif not os.path.isdir('dz') and reruns != [] :  
    newrun = int(reruns[-1])+1
    #os.rename('dz',f'dz{newrun}')
    laststep = int(np.loadtxt(f'dz{newrun-1}/polcom.txt')[-1][0])
    os.system(f'lmp -r2data ./dz{newrun-1}/crystal.restart2 {laststep}.data')

elif os.path.isdir('dz') and reruns != [] :
    newrun = int(reruns[-1])+1
    os.rename('dz',f'dz{newrun}')
    laststep = int(np.loadtxt(f'dz{newrun}/polcom.txt')[-1][0])
    os.system(f'lmp -r2data ./dz{newrun}/crystal.restart2 {laststep}.data')

# else: 
    # newrun = int(reruns[-1])+1
    # os.system(f'lmp -r2data ./dz{newrun-1}/crystal.restart2 {laststep}.data')

# try:laststep = int(np.loadtxt('dz/polcom.txt')[-1][0])
#laststep = int(np.loadtxt(f'dz{newrun-1}/polcom.txt')[-1][0])

# os.system('module load StdEnv/2020  intel/2020.1.217  openmpi/4.0.3')
# os.system('module load lammps-omp/20210929')
# os.system(f'lmp -r2data ./dz/crystal.restart2 {laststep}.data')
# os.system(f'lmp -r2data ./dz{newrun-1}/crystal.restart2 {laststep}.data')


# 

with open('restart.in','r') as inp :
    lines = inp.readlines()
    
    with open(f'{win}restart.in','w') as out:
        for line in lines:
            if line == 'shell mkdir dz\n' and reruns==[]: line='shell mkdir dz2\n'
            if line == 'shell mkdir dz\n' and reruns!=[]: line=f'shell mkdir dz{int(reruns[-1])+1}\n'
            if line == 'shell cd dz\n' and reruns==[]: line='shell cd dz2\n'
            if line == 'shell cd dz\n' and reruns!=[]: line=f'shell cd dz{int(reruns[-1])+1}\n'
            if line == 'read_data\n': line = f'read_data ../{laststep}.data\n'
            elif line == 'reset_timestep\n': line =f'reset_timestep {int(laststep)}\n'
            elif line == 'run\n' : line =f'run {int(multi*5000000)} upto\n'
            out.write(line)

print(f'\nLast step = {laststep}')
print(f'\nsteps remaining = {int(multi*5000000) - laststep}')
print(f'\nrate = {(40/5000000)*60*60} seconds/step')

hrs = (40/5000000)*(multi*5000000 - laststep)
if laststep == int(multi*5000000) : hrs = 0
elif 0 < hrs < 1: hrs = 1
elif hrs > 1 : hrs = math.ceil(hrs)

print(f'\nhours needed = {hrs}\n')



with open('restart.sh','r') as inp :
    lines = inp.readlines()
    
    with open(f'{win}restart.sh','w') as out:
        for line in lines:
            if '#SBATCH --time=' in line: line = f'#SBATCH --time={hrs}:00:00\n'
            out.write(line)

os.system(f'dos2unix {win}restart.sh')
if hrs >= 1: 
    if subm == 'yes' :
        os.system(f'sbatch {win}restart.sh')
        print('\n'+f'{hrs} hrs needed! so submitting job'+'\n')
else : print('\n'+f'{hrs} hrs needed! so NOT submitting job'+'\n')