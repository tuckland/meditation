# data mining according to contacts and generate radar map
# Version 0.1
# Author Song Ke
# Date 2017-05

############################HEAD#####################################

#This shot scripts combo have three subscripts working pipeline
#1. This script ***contact_map_radar_data_collection.py*** iterate all sims
#								|
#								v
#2. 			***Contact_map_data_mining_final.py*** 
#			This is the main script	to generate and filter data
#	Noted if you use MDtraj to generate contact info, the pdb and xtc file
#						should be not capped. 
#								|
#								v
#3.				***Contact_map_radar_final.py***
#			This is the script to plot radar (polar) chart 

# Each script has detailed description

from __future__ import print_function
import matplotlib.pyplot as plt
import mdtraj as md
import mdtraj.testing
import os, re, commands, sys, math,gc
import glob
from pylab import *
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import pylab as plot
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
from sys import getrefcount
from operator import itemgetter
import matplotlib.mlab as mlab
from scipy.stats import norm
from scipy.stats import gaussian_kde
import matplotlib.pyplot as plt
import mpl_toolkits.axisartist as axisartist
from matplotlib import rc,pyplot
from matplotlib import rcParams
from scipy.stats import kde
import itertools
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import numpy as np
from mdtraj import *
import matplotlib.gridspec as gridspec
import subprocess
import shlex

name_raw=raw_input('Please input different mutation or \
truncation simulations, use SPACE to separate each input, i.e full-length,noVSD:')
namelist=[str(x) for x in name_raw.split(' ')]

sim_type=raw_input("Please input simulation type nores-p20mv or nores-p200mv:")

res_input=raw_input("Please input a list of residues you want to analyze,\
only resid is ok, each resid please separate by a space,please input at \
lease two residues, otherwise error occurs:")

reslist=res_input.split(' ')
			
data_mine_script='contact_map_data_mining_final.py'
			
pdb = raw_input("Please input the pdb file here, i.e. \
md-nores-p20mv_prot_nocap.pdb:") 	#Here nocap of the topology and xtc is recommand, if in contact_map_data_mining_final.py, use Mdtraj compute_contacts function 
xtc = raw_input("please input the xtc file here, i.e. \
md-nores-p20mv_drop100ps_compact_fit_0-1us_prot_nocap.xtc:")

nframes=int(raw_input("Please input how many frames of the original trajectory:"))
nassem=int(raw_input("Please input how many monomers in the structural assembly:"))
fine_parameter=float(raw_input("Please input a fine parameter to rule out \
low-probability contacting residues:"))

pis=os.getcwd()
for j in namelist:
	dir_prefix='/home/song/ins/navs/pis/5hvx_assembly_loopmodel_best_aligned_4p9o_capped_%s/pi1/pi1_0M/nacl_0.5M/310K/nores/%s'%(j,sim_type) #different simulation type and different voltage
	os.popen('cp %s %s'%(data_mine_script,dir_prefix))
	os.chdir('%s'%(dir_prefix))
	for i in reslist:
		try: #This exception ensures some residues are not included in certain types of truncated or mutated simulations 
			p = subprocess.Popen(['python %s/contact_map_data_mining_final.py'%(dir_prefix)], 
								stdin=subprocess.PIPE, stdout=subprocess.PIPE,shell=True) #iterate different residues we want to analyze
			stdout, stderr = p.communicate(input='%s\n%s\n%s\n'%(pdb,xtc,i))
		except ValueError as e:
			print (e);pass
	os.chdir('%s'%(pis))

for i in reslist:
	try:
		p = subprocess.Popen(['python contact_map_radar_final.py'], 
								stdin=subprocess.PIPE, stdout=subprocess.PIPE,shell=True) #iterate different residues we want to analyze
		stdout, stderr = p.communicate(input='%s\n%s\n%s\n%s\n%s\n%s'%(nframes,nassem,fine_parameter,sim_type,name_raw,i))
	except ValueError as e:
		print (e);pass
