# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 15:52:50 2023

@author: Naveen
"""
# system = ['100man', '100mgc', '100mgn', '100mgf']

# for s in system:
#     print(f'cd /project/6003277/vasudevn/model3/{s}/min;\nsbatch min.sh;')

# for s in system:
#     print(f'cd /scratch/vasudevn/project/6003277/vasudevn/model3/{s}/npt;\nsbatch npt.sh;')

# for s in system:
#     print(f'cp /project/6003277/vasudevn/model3/{s}/npt/nptf.dump /project/6003277/vasudevn/model3/{s}/smd/;')

# for s in system:
#     print(f'mkdir /lustre07/scratch/vasudevn/project/6003277/vasudevn/model3/{s}/colvar;')
    
# for s in system:
#     print(f'cp /lustre07/scratch/vasudevn/project/6003277/vasudevn/model3/100man/colvar/listgen.py /lustre07/scratch/vasudevn/project/6003277/vasudevn/model3/{s}/colvar/listgen.py;')

# for s in system:
#     print(f'rm /lustre07/scratch/vasudevn/project/6003277/vasudevn/model3/{s}/colvar/cattraj.py;')
#     # print(f'rm /lustre07/scratch/vasudevn/project/6003277/vasudevn/model3/{s}/colvar/cattrajcmd.py;')
#     # print(f'cp /lustre07/scratch/vasudevn/project/6003277/vasudevn/model3/100mgc/colvar/cattrajcmd.py /lustre07/scratch/vasudevn/project/6003277/vasudevn/model3/{s}/colvar/cattrajcmd.py;')
#     print(f'cp /lustre07/scratch/vasudevn/project/6003277/vasudevn/model3/100gg/colvar/cattraj.py /lustre07/scratch/vasudevn/project/6003277/vasudevn/model3/{s}/colvar/cattraj.py;')

# # adjusting boundary
# addvalue = 0.5

# b = "-7.094 50.128 xlo xhi -39.125 39.385 ylo yhi -37.324 37.376 zlo zhi" #100man

# # -7.344 50.378 xlo xhi
# # -39.375 39.635 ylo yhi
# # -37.574 37.626 zlo zhi

# # 5.8005075     1.389356    1.2785136
# b = "-7.094 50.138 xlo xhi -39.126 39.395 ylo yhi -37.329 37.382 zlo zhi" #100mgf


# # -7.344 50.388 xlo xhi
# # -39.376 39.645 ylo yhi
# # -37.579 37.632 zlo zhi

# values = [float(b.split(' ')[i]) for i in [0,1,4,5,8,9]]

# print(f'\n\n{values[0] - addvalue} {values[1] + addvalue} xlo xhi\n{values[2] - addvalue} {values[3] + addvalue} ylo yhi\n{values[4] - addvalue} {values[5] + addvalue} zlo zhi')


# ######

# for st, sp in zip([883,2059,3235,4411,5587,6763,7939,9115,10291],[1176,2352,3528,4704,5880,7056,8232,9408,10584]):
#     print(f'set sel{st} [atomselect top "serial {st} to {sp}"];\nmeasure center $sel{st} weight mass;\n\n')

###### colvar ######################

import os
import numpy as np

fc =7

win = np.arange(0,37,1)
cen = np.arange(2.0,20.5,0.5)
system = ['100man', '100de', '100dem', '100lg','100gg','100mgf','100mgn','100mgc']

subloc = 'model3neo'
cc = 'graham'
home = False

if home: foldloc = 'D:\\Research_work\\models'
else : foldloc = 'C:\\Users\\vasudevn\\Desktop'

timestep = 2
targettime = 10 #ns
targetstep =  int(targettime*1000000/2)
targethours = int(np.ceil(2.5*targettime))



if cc == 'graham' : pref=''
else : pref = '/scratch/vasudevn'

# for w in win:
#     print(f'mkdir {w};')


for s in system:
    os.chdir(f'{foldloc}\\PMF\\{cc}\\{s}')
    for w,c in zip(win,cen):
        
        os.chdir(f'{foldloc}\\PMF\\{cc}\\{s}\\colvar\\{w}')
        with open(f'{w}.in','w') as out:
            out.write(f'# {s} - {w} \n\nshell mkdir dz\nshell cd dz\n\n')
            out.write('#variable assignment\n')
            out.write(f'variable\tinputname index {w}\n\n')
            out.write('#initial configuration\n\n')
            out.write('units\treal\nboundary\tp p p\nnewton\ton\npair_style\tlj/cut/coul/long 16\npair_modify\tmix geometric shift yes\n')
            out.write('kspace_style\tpppm 1e-6\n')
            out.write('neighbor\t2 bin\n')
            out.write('neigh_modify\tdelay 0 every 1 check yes page 1000000 one 50000\n')
            out.write('\n\n')
            out.write('atom_style\tfull\n')
            out.write('bond_style\tharmonic\n')
            out.write('angle_style\tharmonic\n')
            out.write('dihedral_style\tharmonic\n')
            out.write('special_bonds\tlj/coul 0 0 1 angle yes dihedral yes\n')
            out.write('\n\n')
            out.write(f'read_data\t../../datafiles/${{inputname}}.data\n')
            out.write('\n\n')
            # out.write('#variable\tlaststep file ../${inputname}.dump\n')
            # out.write('#next\tlaststep\n')
            # out.write('#read_dump\t../${inputname}.dump ${laststep}  x y z vx vy vz ix iy iz box yes replace yes format native\n')
            out.write('\n\n')
            out.write('#group section\n')
            out.write('group cel id 1:10584\n')
            if '100man' in s:
                out.write('group pol id 10585:10755\n')
            elif s in ['100lg','100dem','100de'] :
                out.write('group pol id 10585:10797\n')
            else:
                out.write('group pol id 10585:10839\n')
            out.write('group lay1 id 883:1176 2059:2352 3235:3528 4411:4704 5587:5880 6763:7056 7939:8232 9115:9408 10291:10584\n')
            # out.write('group lay1m4 id 883:1176\ngroup lay1m8 id 2059:2352\ngroup lay1m12 id 3235:3528\ngroup lay1m16 id 4411:4704\ngroup lay1m20 id 5587:5880\ngroup lay1m24 id 6763:7056\ngroup lay1m28 id 7939:8232\ngroup lay1m32 id 9115:9408\ngroup lay1m36 id 10291:10584\n')
            out.write('group2ndx ../group.ndx cel pol lay1\n\n')
            out.write('reset_timestep\t0\n')
            out.write('timestep\t2\n')
            out.write('\n\n')
            out.write('#NVT fix and shake\n')
            out.write('fix\t1 all shake 1e-6 500 5000 b 1  4 6 7 #a 12\n')
            out.write('fix\t2 all nvt temp 303.15 303.15 100\n')
            out.write(f'fix colvar1 all colvars ../ini{w}.inp tstat 2 output ini{w}\n')
            # out.write('fix rclay1m4 lay1m4 recenter 5.800 1.389 1.278 units box\nfix rclay1m8 lay1m8  ter 5.800 1.389 1.278 units box\nfix rclay1m12 lay1m12 recenter 5.800 1.389 1.278 units box\nfix rclay1m16 lay1m16 recenter 5.800 1.389 1.278 units box\nfix rclay1m20 lay1m20 recenter 5.800 1.389 1.278 units box\nfix rclay1m24 lay1m24 recenter 5.800 1.389 1.278 units box\nfix rclay1m28 lay1m28 recenter 5.800 1.389 1.278 units box\nfix rclay1m32 lay1m32 recenter 5.800 1.389 1.278 units box\nfix rclay1m36 lay1m36 recenter 5.800 1.389 1.278 units box\n')
            out.write('#fix recen	lay1 recenter 5.800 1.389 1.278  units box\n')
            out.write('run 500000\n')
            out.write('unfix 1\n')
            out.write('unfix 2\n')
            out.write('#unfix recen\n')
            # out.write('unfix rclay1m4\n')
            # out.write('unfix rclay1m8\n')
            # out.write('unfix rclay1m12\n')
            # out.write('unfix rclay1m16\n')
            # out.write('unfix rclay1m20\n')
            # out.write('unfix rclay1m24\n')
            # out.write('unfix rclay1m28\n')
            # out.write('unfix rclay1m32\n')
            # out.write('unfix rclay1m36\n')
            
            out.write('unfix colvar1\n\n')
            out.write('\nreset_timestep	0\n\n')
            out.write('#compute section\n')
            out.write('compute\tcom1 cel com\n')
            out.write('fix\tcom11 cel ave/time 500 1 500 c_com1[*] file celcom.txt\n')
            out.write('\n\n')
            out.write('compute\tcom3 pol com\n')
            out.write('fix\tcom13 pol ave/time 500 1 500 c_com3[*] file polcom.txt\n')
            out.write('\n')
            out.write('compute\tcom2 lay1 com\n')
            out.write('fix\tcom12 lay1 ave/time 500 1 500 c_com2[*] file lay1com.txt\n')
            out.write('\n')
            out.write('variable d equal c_com3[1]-c_com2[1]\n')
            out.write('\n')
            out.write('#NVT fix and shake\n')
            out.write('fix\t1 all shake 1e-6 500 5000 b 1  4 6 7 #a 12\n')
            out.write('fix\t2 all nvt temp 303.15 303.15 100\n')
            out.write(f'fix colvar1 all colvars ../{w}.inp tstat 2 output {s}{w}\n')
            out.write('\n\n')
            out.write('#colvar section\n')
            out.write('#fix recen lay1 recenter 5.800 1.389 1.278 units box\n')
            # out.write('fix rclay1m4 lay1m4 recenter 5.800 1.389 1.278 units box\nfix rclay1m8 lay1m8 recenter 5.800 1.389 1.278 units box\nfix rclay1m12 lay1m12 recenter 5.800 1.389 1.278 units box\nfix rclay1m16 lay1m16 recenter 5.800 1.389 1.278 units box\nfix rclay1m20 lay1m20 recenter 5.800 1.389 1.278 units box\nfix rclay1m24 lay1m24 recenter 5.800 1.389 1.278 units box\nfix rclay1m28 lay1m28 recenter 5.800 1.389 1.278 units box\nfix rclay1m32 lay1m32 recenter 5.800 1.389 1.278 units box\nfix rclay1m36 lay1m36 recenter 5.800 1.389 1.278 units box\n')
            out.write('\n\n')
            out.write('#output section\n')
            out.write('restart\t500000 ps.restart\n')
            out.write('restart\t1000  crystal.restart1 crystal.restart2\n')
            out.write('\n\n')
            out.write(f'dump\t1 all dcd 500 {w}.dcd\n')
            out.write('dump_modify\t1 unwrap yes\n')
            out.write(f'dump\t2 all custom 5000 {w}.lammpstrj id type x y z vx vy vz ix iy iz\n')
            out.write('\n\n')
            out.write('thermo\t5000\n')
            out.write('thermo_style\tcustom step press temp vol density  pe ke c_com3[1] c_com2[1] v_d \n')
            out.write('\n')
            out.write(f'run\t{targetstep} upto\n')
            out.write('\n')
            out.write(f'write_data\tpmf{w}.data\n')
            out.write(f'write_dump\tall custom pmf{w}.dump id type x y z vx vy vz ix iy iz\n')

        with open('restart.in','w') as out:
            out.write(f'# {s} - {w} \n\nshell mkdir dz\nshell cd dz\n\n')
            out.write('#variable assignment\n')
            out.write(f'variable\tinputname index {w}\n\n')
            out.write('#initial configuration\n\n')
            out.write('units\treal\nboundary\tp p p\nnewton\ton\npair_style\tlj/cut/coul/long 16\npair_modify\tmix geometric shift yes\n')
            out.write('kspace_style\tpppm 1e-6\n')
            out.write('neighbor\t2 bin\n')
            out.write('neigh_modify\tdelay 0 every 1 check yes page 1000000 one 50000\n')
            out.write('\n\n')
            out.write('atom_style\tfull\n')
            out.write('bond_style\tharmonic\n')
            out.write('angle_style\tharmonic\n')
            out.write('dihedral_style\tharmonic\n')
            out.write('special_bonds\tlj/coul 0 0 1 angle yes dihedral yes\n')
            out.write('\n\n')
            out.write('read_data\n')
            out.write('\n\n')
            # out.write('variable\tlaststep file ../${inputname}.dump\n')
            # out.write('next\tlaststep\n')
            # out.write('read_dump\t../${inputname}.dump ${laststep}  x y z vx vy vz ix iy iz box yes replace yes format native\n')
            out.write('\n\n')
            out.write('#group section\n')
            out.write('group cel id 1:10584\n')
            if '100man' in s:
                out.write('group pol id 10585:10755\n')
            elif s in ['100lg','100dem','100de'] :
                out.write('group pol id 10585:10797\n')
            else:
                out.write('group pol id 10585:10839\n')
            out.write('group lay1 id 883:1176 2059:2352 3235:3528 4411:4704 5587:5880 6763:7056 7939:8232 9115:9408 10291:10584\n')
            # out.write('group lay1m4 id 883:1176\ngroup lay1m8 id 2059:2352\ngroup lay1m12 id 3235:3528\ngroup lay1m16 id 4411:4704\ngroup lay1m20 id 5587:5880\ngroup lay1m24 id 6763:7056\ngroup lay1m28 id 7939:8232\ngroup lay1m32 id 9115:9408\ngroup lay1m36 id 10291:10584\n')
            out.write('group2ndx ../group.ndx cel pol lay1\n\n')
            out.write('reset_timestep\n')
            out.write('timestep\t2\n')
            # out.write('\n\n')
            # out.write('#NVT fix and shake\n')
            # out.write('fix\t1 all shake 1e-6 500 5000 b 1  4 6 7 #a 12\n')
            # out.write('fix\t2 all nvt temp 303.15 303.15 100\n')
            # out.write(f'fix colvar1 all colvars ../ini{w}.inp tstat 2 output ini{w}\n')
            # out.write('fix recen1	lay1 recenter 5.800 1.389 1.278  units box\n')
            # out.write('run 500000\n')
            # out.write('unfix 1\n')
            # out.write('unfix 2\n')
            # out.write('unfix recen1\n')
            # out.write('unfix colvar1\n\n')
            # out.write('\nreset_timestep	0\n\n')
            out.write('#compute section\n')
            out.write('compute\tcom1 cel com\n')
            out.write('fix\tcom11 cel ave/time 500 1 500 c_com1[*] file celcom.txt\n')
            out.write('\n\n')
            out.write('compute\tcom3 pol com\n')
            out.write('fix\tcom13 pol ave/time 500 1 500 c_com3[*] file polcom.txt\n')
            out.write('\n')
            out.write('compute\tcom2 lay1 com\n')
            out.write('fix\tcom12 lay1 ave/time 500 1 500 c_com2[*] file lay1com.txt\n')
            out.write('\n')
            out.write('variable d equal c_com3[1]-c_com2[1]\n')
            out.write('\n')
            out.write('#NVT fix and shake\n')
            out.write('fix\t1 all shake 1e-6 500 5000 b 1  4 6 7 #a 12\n')
            out.write('fix\t2 all nvt temp 303.15 303.15 100\n')
            out.write(f'fix colvar1 all colvars ../{w}.inp tstat 2 output {s}{w}\n')
            out.write('\n\n')
            out.write('#colvar section\n')
            out.write('#fix recen lay1 recenter 5.800 1.389 1.278 units box\n')
            # out.write('fix rclay1m4 lay1m4 recenter 5.800 1.389 1.278 units box\nfix rclay1m8 lay1m8 recenter 5.800 1.389 1.278 units box\nfix rclay1m12 lay1m12 recenter 5.800 1.389 1.278 units box\nfix rclay1m16 lay1m16 recenter 5.800 1.389 1.278 units box\nfix rclay1m20 lay1m20 recenter 5.800 1.389 1.278 units box\nfix rclay1m24 lay1m24 recenter 5.800 1.389 1.278 units box\nfix rclay1m28 lay1m28 recenter 5.800 1.389 1.278 units box\nfix rclay1m32 lay1m32 recenter 5.800 1.389 1.278 units box\nfix rclay1m36 lay1m36 recenter 5.800 1.389 1.278 units box\n')
            out.write('\n\n')
            out.write('#output section\n')
            out.write('restart\t500000 ps.restart\n')
            out.write('restart\t1000  crystal.restart1 crystal.restart2\n')
            out.write('\n\n')
            out.write(f'dump\t1 all dcd 500 {w}.dcd\n')
            out.write('dump_modify\t1 unwrap yes\n')
            out.write(f'dump\t2 all custom 5000 {w}.lammpstrj id type x y z vx vy vz ix iy iz\n')
            out.write('\n\n')
            out.write('thermo\t5000\n')
            out.write('thermo_style\tcustom step press temp vol density  pe ke c_com3[1] c_com2[1] v_d \n')
            out.write('\n')
            out.write('run\n')
            out.write('\n')
            out.write(f'write_data\tpmf{w}.data\n')
            out.write(f'write_dump\tall custom pmf{w}.dump id type x y z vx vy vz ix iy iz\n')


        with open(f'ini{w}.inp','w') as out:
            out.write('indexFile ../group.ndx\ncolvarsTrajAppend no\ncolvarsTrajFrequency 500\ncolvarsRestartFrequency 500\n')
            out.write('colvar {\n')
            out.write('name dist\n')
            out.write('distanceZ {  \n')  
            out.write('main { indexGroup pol } \n')   
            out.write('ref { indexGroup lay1 }\n')
            out.write('axis (1,0,0)  \n')
            out.write('}\n')
            out.write('}\n')
            out.write('\n')
            out.write('harmonic {  \n')
            out.write('colvars dist  \n')
            out.write('outputCenters on \n')
            out.write(f'forceConstant {fc} \n')
            out.write(f'centers {c}         # initial distance \n') 
            out.write(f'targetCenters {c}  	# final distance  \n')
            out.write('targetNumSteps 500000  \n')
            out.write('targetNumstages 0\n')
            out.write('outputAccumulatedWork on\n')
            out.write('}\n')

        with open(f'{w}.inp','w') as out:
            out.write('indexFile ../group.ndx\ncolvarsTrajAppend no\ncolvarsTrajFrequency 500\ncolvarsRestartFrequency 500\n')
            out.write('colvar {\n')
            out.write('name dist\n')
            out.write('distanceZ {  \n')  
            out.write('main { indexGroup pol } \n')   
            out.write('ref { indexGroup lay1 }\n')
            out.write('axis (1,0,0)  \n')
            out.write('}\n')
            out.write('}\n')
            out.write('\n')
            out.write('harmonic {  \n')
            out.write('colvars dist  \n')
            out.write('outputCenters on \n')
            out.write(f'forceConstant {fc} \n')
            out.write(f'centers {c}         # initial distance \n') 
            out.write(f'targetCenters {c}  	# final distance  \n')
            out.write(f'targetNumSteps {targetstep}  \n')
            out.write('targetNumstages 0\n')
            out.write('outputAccumulatedWork on\n')
            out.write('}\n')
        if cc in ['graham','cedar']:
            Node = 5
            cpus = 32
        elif cc in ['beluga','niagara']:
            Node = 4
            cpus = 40

        with open(f'{w}.sh','w') as out:
            out.write('#!/bin/bash -l\n')
            if cc == 'graham':
                out.write('#SBATCH --account=rrg-xili\n')
            else : out.write('#SBATCH --account=def-xili\n')
            
            if cc in ['graham','cedar','beluga','niagara']:
                out.write(f'#SBATCH -N {Node}\n')
                out.write(f'#SBATCH -n {int(Node*cpus)}\n')
                nnn = int(Node*cpus)
            else : 
                out.write('#SBATCH -n 192\n')
                nnn = 192
                
            out.write('#SBATCH --mem-per-cpu=1G\n')
            out.write('#SBATCH --mail-type=ALL\n')
            out.write('#SBATCH --mail-user=vasudevnhpcjobs@gmail.com\n')
            
            if cc == 'graham':
                out.write(f'#SBATCH --time={targethours}:00:00\n')
            else : out.write(f'#SBATCH --time={targethours}:00:00\n')
            out.write(f'#SBATCH -J {s}-{w}\n')
            out.write('\n')
            out.write('module load StdEnv/2020  intel/2020.1.217  openmpi/4.0.3\n')
            out.write('module load lammps-omp/20210929\n')
            out.write('\n')
            out.write(f'cd {pref}/project/6003277/vasudevn/{subloc}/{s}/colvar/{w}\n')
            out.write(f'srun -n {nnn} lmp -i {w}.in;\n')
        
        with open('restart.sh','w') as out:
            out.write('#!/bin/bash -l\n')
            if cc == 'graham':
                out.write('#SBATCH --account=rrg-xili\n')
            else : out.write('#SBATCH --account=def-xili\n')

            if cc in ['graham','cedar','beluga','niagara']:
                out.write(f'#SBATCH -N {Node}\n')
                out.write(f'#SBATCH -n {int(Node*cpus)}\n')
                nnn = int(Node*cpus)
            else : 
                out.write('#SBATCH -n 160\n')
                nnn = 160
            out.write('#SBATCH --mem-per-cpu=1G\n')
            out.write('#SBATCH --mail-type=ALL\n')
            out.write('#SBATCH --mail-user=vasudevnhpcjobs@gmail.com\n')
            if cc == 'graham':
                out.write(f'#SBATCH --time={targethours}:00:00\n')
            else : out.write(f'#SBATCH --time={targethours}:00:00\n')
            out.write(f'#SBATCH -J {s}-{w}r\n')
            out.write('\n')
            out.write('module load StdEnv/2020  intel/2020.1.217  openmpi/4.0.3\n')
            out.write('module load lammps-omp/20210929\n')
            out.write('\n')
            out.write(f'cd {pref}/project/6003277/vasudevn/{subloc}/{s}/colvar/{w}\n')
            out.write(f'srun -n {nnn} lmp -i {w}restart.in;\n')

os.chdir(f'{foldloc}\\PMF')

## group sub.sh file ##

for s in system:
    with open(f'./{cc}/{s}_sub.sh','w') as out:
        for i in range(0,37,1):
            out.write(f'cd {pref}/project/6003277/vasudevn/{subloc}/{s}/colvar/{i};\n') 
            out.write(f'dos2unix {i}.sh;\n')
            out.write(f'sbatch {i}.sh;\n')

for s in system:
    print(f'dos2unix {s}_sub.sh')
    print(f'chmod +x {s}_sub.sh')
for s in system:
    print(f'./{s}_sub.sh')
    
############## plot distribution

# import os
# import glob
# import seaborn as sns
# import numpy as np
# import pandas as pd
# from matplotlib import pyplot as plt

# def displot(s):
    
#     os.chdir(f'{foldloc}\\PMF\\dist\\{s}')
    
#     distfilesunsort = glob.glob('*.traj')
#     length = len(distfilesunsort)
#     distfiles = [f'{s}{i}.colvars.traj' for i in range(length)]
    
#     df = pd.DataFrame(columns=range(length))
#     cen = np.arange(2.0,20.5,0.5)
    
#     for i in range(length):
#         df[i] = np.loadtxt(distfiles[i])[:,1]
    
#     fig, ax = plt.subplots()
#     fig.set_figwidth(15)
#     for i in range(length):
#         # sns.distplot(df[i], hist = False, kde = True, kde_kws = {'linewidth': 2})
#         sns.kdeplot(df[i])
#         ax.axvline(cen[i],c='k',ls='--')
#     plt.xticks(cen[::2])
#     plt.title(f'{s}')
#     plt.show()
    
#     return None


# displot('100de')
# displot('100lg')
# displot('100gg')
# displot('100man')
# displot('100mgc')
# displot('100mgf')
# displot('100mgn')




# ########### COWBOE #########
# #Simplex - I
# import matplotlib.pyplot as plt
# import numpy as np
# import os
# from cowboe import pmfcompare, pmftopoints, cowboe_settings, cowboe, cowboeRNM, cowboe_wham, cowboefit

# A = [1.75, 2.60, 3.25]
# Al = [np.log(i) for i in A]
# U = [0.7, 0.9, 0.6]
# K = [ 8*i for i in U]


# plt.plot([Al[0],Al[1],Al[2],Al[0]], [U[0],U[1],U[2],U[0]])
# plt.show()

# os.chdir('D:\\Research_work\\afinalpaperrun\\analysis\\OPT\\test\\algorithm\\pmf-equal-cut\\Analysis-p3\\100gg-40ns\\cowboe\\trajfiles')

# # pmfcompare(pmfs=['b100gg.txt','t39100gg.txt'],name='test-39',splices=[0,0])
# # pmfcompare(pmfs=['b100gg.txt','t10100gg.txt'],name='test-10',splices=[0,0])
# # pmfcompare(pmfs=['b100gg.txt','t20100gg.txt'],name='test-20',splices=[0,0])
# pmfcompare(pmfs=['bench.txt','raw.txt'],name='test-01',splices=[0,0])
# cowboe_settings.update({'mark every' : 10})


# loc = 'D:\\Research_work\\afinalpaperrun\\analysis\\OPT\\test\\algorithm\\pmf-equal-cut\\Analysis-p3\\100gg-40ns\\cowboe\\trajfiles'
# pmftopoints(location=loc,testpmf='raw.txt',order=16)

# cowboe_settings.update({'conv. min of 1st window' : 2.0})
# cowboe_settings.update({'conv. min of last window' : 20.0})
# cowboe_settings.update({'conventional no of windows' : 37})

# #1
# cowboe(A=1.75, V=0.7, sc=8, name='1', location=loc)
# os.chdir(loc)
# #2
# cowboe(A=2.60, V=0.9, sc=8, name='2', location=loc)
# os.chdir(loc)
# #3
# cowboe(A=3.25, V=0.6, sc=8, name='3', location=loc)
# os.chdir(loc)


# ########## cowboe - p2

# OA = 1.6571
# OB = 0.82

# A = [[2.0,2.9,3.5],[1.8,2.3,2.7]] #[1.8,2.3,2.9]
# U = [[0.75,.87,.8],[1.05,0.95,1.03]] #[1.0,0.95,1.05]

# def simplex(Als, Us):
#     # K = [ 8*i for i in U]
    
#     fig, ax = plt.subplots()
#     cs = ['k','b']
#     for A,U,c in zip(Als,Us,cs):
#         Al = [np.log(i) for i in A]
#         ax.plot([Al[0],Al[1],Al[2],Al[0]], [U[0],U[1],U[2],U[0]], f'{c}-' )
#     ax.plot([np.log(OA)],[OB],'g^',markersize=15)
#     plt.xlim(0.3,1.3)
#     plt.ylim(0.6,1.1)
#     plt.show()

# simplex(A,U)

# cowboeRNM(A=[1.8,2.3,2.7], V=[1.05,0.95,1.03], fit=[2,3,5])



#
























