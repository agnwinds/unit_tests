#!/usr/bin/env python
#import read_sub as sub
import py_read_output as rd 
import py_plot_util as util
import plot_sub as p
from pylab import * 
import numpy as np 
import sys
import os
from astropy.io import ascii
import time

'''
usage
 e.g. python plot_output.py 
'''
  
BENCH_FOLDER = "outputs_release/"

def run_py_wind (fname, FOLDER, vers="", cmds=None, ilv=None):
	'''
	run version vers of py_wind on file fname.wind_save, removes
	all traces and moves the .complete file to FOLDER/
	'''

	if cmds == None:
		cmds = np.array(["1","1","1","q"]) # cms to make the onefile summaries

	x = cmds
	np.savetxt("_tempcmd.txt", x, fmt = "%s")

	cmd = 'py_wind'+vers+" "+FOLDER+fname+' < _tempcmd.txt > tempfile'

	isys = os.system(cmd)

	time.sleep(3)

	#os.system("mv %s.complete %s" % (fname, FOLDER))

	# remove temporary file
	os.system("rm -f _tempcmd.txt py_wind.pf logfile tempfile tmp.rdpar")
	return isys



def make_plots(names, FOLDER): 

	try:
		VERSION=""
		f = open("%s%s.out" % (FOLDER,names[0]), "r")
		for line in f:
			data = line.split()
			if len(data) > 2:
				if data[0] == "!!Python" and data[1]=="Version":
					VERSION = data[2]

			#if data[0] == "!!Python" and data[1]=="Version":

	except IOError:
		print "Couldn't read version"
		VERSION=""
		


	print "VERSION %s" % VERSION

	for i in range(len(names)):

		# this is just the name of the parameter file
		shortname = names[i]

		# the file will be in subfolders for comparison
		name = FOLDER + shortname
		benchname = BENCH_FOLDER + shortname
		PLOT_FOLDER = "plot%s" % FOLDER[4:]

		os.system("mkdir %s" % PLOT_FOLDER)

		# read in the parameter file
		pf_dict = rd.read_pf(name)						


		# try and read the output. if you get an index error it may have failed
		try:
			convergence = rd.read_convergence (name + ".out")		# get convergence of model
			bench_convergence = rd.read_convergence (benchname + ".out")
		except IndexError:
			print "Couldn't read convergence info for root %s, possible failure" % name

		# print out the convergence compared to the benchmark model
		print "Model %s" % name
		print "%.2fpc Converged. Release: %.2f" % (100.0*convergence, 100.0*bench_convergence)

		# run py_wind- only need to run this to create the onefile summary
		run_py_wind(shortname, FOLDER, vers=VERSION)

		
		p.make_geometry_plot(shortname, FOLDER, PLOT_FOLDER)					# make plots of pywind quantities
		p.make_geometry_ratios(shortname, FOLDER, PLOT_FOLDER)


		# try and read in the spectrum
		make_plots=True
		try:
			s = rd.read_spectrum(name)
		except IOError:
			print "Couldn't read spectrum for root %s, possible failure" % name
			make_plots = False

		# make plots against the benchmark spectrum
		if make_plots:

			s_bench = rd.read_spectrum(benchname)

			#get_standard_dev(shortname, s, s_bench)


			p.make_residual_plot(s, s_bench, shortname, PLOT_FOLDER)		# make residual plots
			p.make_comp_plot(s, s_bench, shortname, PLOT_FOLDER)				# make comparison plots
			p.make_components_comp_plot(s, s_bench, shortname, PLOT_FOLDER)		# make components comparison plots



		# this is the test spectot file
		s = rd.read_spectrum (name+".log_spec_tot")

		# this is the benchmark spectot file to test against
		s_bench = rd.read_spectrum (benchname+".log_spec_tot")

		# make a comparison plot of the log_spec_tot file
		p.make_log_spec_tot_comp_plot(s, s_bench, shortname, PLOT_FOLDER)	

		#p.make_hc_plots_from_loop (shortname)
		#p.make_ion_plots_from_loop (shortname)




	# move all the wind data somewhere out the way
	#os.system("mkdir wind_data")
	#os.system("mv *.dat wind_data/")
	#os.system("open -a preview *.png")

	print "all done"

	return 0


if __name__ == "__main__":

	os.system("mkdir plots")

	mode = int(sys.argv[1])

	# this is where the outputs and plots are stored
	FOLDER = sys.argv[2] +"/"

	if mode == 1:
		names = ["1d_sn", "star", "cv_standard"]
	elif mode == 2:
		names = ["1d_sn", "star", "fiducial_agn", "cv_standard"]
	elif mode == 3:
		names = ["1d_sn", "star", "m16_agn", "cv_macro_benchmark", "fiducial_agn", "cv_standard"]

	make_plots(names, FOLDER)

	# import Nick's script to make the ion plots
	if mode > 1:
		from ion_plots import make_ion_plots
		make_ion_plots(FOLDER)


