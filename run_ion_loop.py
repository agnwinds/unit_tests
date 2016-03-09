#!/usr/bin/env python 

'''
                    UNLV

Synopsis:  

This routine carries out a series of thin shell python simulations 
We currently write out H,He,C,N,O and Fe. We also output heating and cooling
mechanisms.


Command line usage (if any):

	usage: ion_loop.py param_filename

Description:  

Primary routines:

Notes:
									   
History:

081214 nsh Commented

'''


if __name__ == "__main__":		# allows one to run from command line without running automatically with write_docs.py

	import sys, subprocess
	import numpy as np
	from scipy.optimize import brentq
	import v_hydro_sub as vhs
	from astropy import units as u
	from astropy import constants as c 

	#Use an optional suffix so file will be py_hydrogen_*suffix*.dat, 
	#If nothing is supplied, default is PL.


	if sys.argv[1]=='h' or sys.argv[1]=='help' or sys.argv[1]=='-h' or len(sys.argv)<2:
		print "This is the all purpose python loop running program"
		print "It can be run from a parameter file or using command line options"
		print "usage:"
		print "		-f filename : get all commands from parameter file"
		quit()


	param_file=sys.argv[1]
	#version_string = sys.argv[2]
	
	python_ver='py'
	atomic_data='data/standard79'
	nmpi=1
	temp=10000.0
	emin=0.0001
	emax=10000.0
	t_brem=1.16e8
	alpha_brem=-0.2
	run_name=param_file
	n_ioniz=2
	mdot_wind=0.00472e-17  #This makes 1e7 hydrogen density for a normal abundance calculation
	python_args=" "
	
	input=open(param_file,'r')
	for line in input.readlines():
		data=line.split()
		if data[0]=='loop':
			ltype=data[1]
		if data[0]=='mdot_wind':
			mdot_wind=float(data[1])
		if data[0]=='atomic':
			atomic_data=data[1]
		if data[0]=='n_ioniz':
			n_ioniz=int(data[1])
		if data[0]=='brem_temp':
			t_brem=float(data[1])
		if data[0]=='brem_alpha':
			alpha_brem=float(data[1])
		if data[0]=='spec_type':
				spec_type=data[1]
		if data[0]=='loop_range':
			varmin=float(data[1])
			varmax=float(data[2])
		if data[0]=='energy_range':
			emin=float(data[1])
			emax=float(data[2])
		if data[0]=='npoints':
			npoints=int(data[1])
		if data[0]=='run_name':
			run_name=data[1]
		if data[0]=='python_ver':
			python_ver=data[1]
		if data[0]=='U':
			U=float(data[1])
		if data[0]=='lum_0':
			lum_0=float(data[1])
		if data[0]=='mpi':
			nmpi=int(data[1])
		if data[0]=='temperature' or data[0]=='temp':
			temp=data[1]
		if data[0]=='python_args':
			python_args=data[1]
		if data[0]=='agn_alpha':
			agn_alpha=data[1]
		if data[0]=='agn_table_lo':
			agn_table_lo=data[1]
		if data[0]=='agn_table_hi':
			agn_table_hi=data[1]
			
	T_x=((emax*u.eV).to(u.erg)/c.k_B.cgs).value
			
			
			
#	npoints=161 			#this is the parameter which says how many runs to perform - we do 10 per order of magnitude in lum
#	python_ver="py79d_dev"   	#This is where we define the version of python to use

	#Open empty files to contain data

#	IP=1. #Zeus definition




	Hout=open('py_hydrogen_'+run_name+'.dat','w')
	Hout.write("U xi T_e I1 I2\n")
	Heout=open('py_helium_'+run_name+'.dat','w')
	Heout.write("U xi T_e I1 I2 I3\n")
	Cout=open('py_carbon_'+run_name+'.dat','w')
	Cout.write("U xi T_e I1 I2 I3 I4 I5 I6 I7\n")
	Nout=open('py_nitrogen_'+run_name+'.dat','w')
	Nout.write("U xi T_e I1 I2 I3 I4 I5 I6 I7 I8\n")
	Oout=open('py_oxygen_'+run_name+'.dat','w')
	Oout.write("U xi T_e I1 I2 I3 I4 I5 I6 I7 I8 I9\n")
	Feout=open('py_iron_'+run_name+'.dat','w')
	Feout.write("U xi T_e I1 I2 I3 I4 I5 I6 I7 I8 I9 I10 I11 I12 I13 I14 I15 I16 I17 I18 I19 I20 I21 I22 I23 I24 I25 I26 I27\n")
	Tout=open('py_temperature_'+run_name+'.dat','w')
	Tout.write("U xi T_e Lum N_e convergence\n")
	Heat=open('py_heat_'+run_name+'.dat','w')
	Heat.write('U xi T_e total photo ff compton ind_comp lines auger\n')
	Cool=open('py_cool_'+run_name+'.dat','w')
	Cool.write('U xi T_e total recomb ff compton DR DI lines Adiabatic\n')

	
	



#	tmin=1e4			#the lower temperature
#	tmax=1e8
#	npoints=21			#Number of runs
	if ltype=='temperature':
		var=np.logspace(np.log10(varmin),np.log10(varmax),npoints)
	elif ltype=='IP':
		var=np.linspace(varmin,varmax,npoints)

#	lum=7.12e28*10**IP #this luminosity give a cloudy U of -2.73, so IP=1, U=-1.73, we multiply lum by 10, and so on

	
	for i in range(len(var)):
		print "Starting Cycle "+str(i+1)+' of '+str(len(var))
		if ltype=="IP":
			U=var[i]
		print "Target U="+str(U)
		inp =open('input.pf','w')
		inp.write("Wind_type() 9\n")
		inp.write("Atomic_data                       "+atomic_data+"\n")
		inp.write("photons_per_cycle                           1000000\n")
		inp.write("Ionization_cycles "+str(n_ioniz)+" \n")
		inp.write("spectrum_cycles                                   0\n")
		inp.write("Coord.system()                   0\n")
		inp.write("Wind.dim.in.x_or_r.direction                     4\n")
		inp.write("Wind_ionization()                   9\n")
		inp.write("Line_transfer()                    3\n")
		inp.write("Thermal_balance_options 		0\n")
		inp.write("System_type()                   2\n")
		inp.write("disk.type(0=no.disk,1=standard.flat.disk,2=vertically.extended.disk)    0\n")
		inp.write("Star_radiation(y=1)                              0\n")
		inp.write("Disk_radiation(y=1)                              0\n")
		inp.write("Wind_radiation(y=1)                              0\n")
		inp.write("QSO_BH_radiation(y=1)                            1\n")
		inp.write("Rad_type_for_star(0=bb,1=models)_to_make_wind                   0\n")
		if spec_type=='brem':
			inp.write("Rad_type_for_agn()_to_make_wind                   5\n")
		elif spec_type=='table':
			inp.write("Rad_type_for_agn()_to_make_wind                   4\n")			
		elif spec_type=='PL':
			inp.write("Rad_type_for_agn()_to_make_wind                   3\n")
		inp.write("mstar(msol)                                     0.8\n")
		inp.write("rstar(cm)                                     1e10\n")
		inp.write("tstar                                      1000000\n")
		inp.write("disk.type()                   0\n")
		inp.write("lum_agn(ergs/s) "+str(lum_0*10**U)+"\n")
		if spec_type=='brem':
			inp.write('agn_bremsstrahlung_temp(K) '+str(t_brem)+'\n')
			inp.write('agn_bremsstrahlung_alpha  '+str(alpha_brem)+'\n')
		elif spec_type=='table':
			inp.write("agn_power_law_index "+str(agn_alpha)+"\n")
			inp.write("low_energy_break(ev) "+str(agn_table_lo)+"\n")
			inp.write("high_energy_break(ev) "+str(agn_table_hi)+"\n")
		inp.write("Torus(0=no,1=yes) 				 0\n")
		inp.write("wind.radmax(cm)                   1.00000000001e11\n")
		if ltype=="temperature" or ltype=="temp":
			inp.write("wind.t.init         "+str(var[i])+"\n")
		elif ltype=="IP":
			if temp=='blondin':
				t_init=brentq(vhs.hc_rate1,1,1e9,args=(10**(U+2.8),t_brem))
				inp.write("wind.t.init         "+str(t_init)+"\n")
				print "Using Blondin calculation for temperature="+str(t_init)
			else:
				inp.write("wind.t.init         "+str(temp)+"\n")
		inp.write("shell_wind_mdot(msol/yr)                     "+str(mdot_wind)+"\n")
		inp.write("shell.wind.radmin(cm)                       1e11\n")
		inp.write("shell.wind_v_at_rmin(cm)                    1.00000\n")
		inp.write("shell.wind.v_at_rmax(cm)                    1.00010\n")
		inp.write("shell.wind.acceleration_exponent                   1\n")
		inp.write("wind.filling_factor(1=smooth,<1=clumped) (1)       1\n")
		inp.write("spec.type(flambda(1),fnu(2),basic(other)                    2\n")
		inp.write("reverb.type (0) 0\n")
		inp.write("Extra.diagnostics(0=no)                           0\n")
		inp.write("Use.standard.care.factors(1=yes)                    1\n")
		if spec_type=='table':
			inp.write("Photon.sampling.approach()                   5\n")
		else:
			inp.write("Photon.sampling.approach()                   8\n")
			inp.write("Num.of.frequency.bands                           10\n")
		inp.write("Lowest_energy_to_be_considered(eV) "+str(emin)+"\n")
		inp.write("Highest_energy_to_be_considered(eV) "+str(emax)+" \n")
		inp.close()
		cline="time mpirun -n "+str(nmpi)+" "+python_ver+" "+python_args+" input > output"
		print cline
		subprocess.check_call(cline,shell=True)	   #This is where we define the version of python to use
		subprocess.check_call("tail -n 70 output  | grep Summary > temp",shell=True)#Strip the last 60 lines from the output
		subprocess.check_call("tail -n 70 output  | grep OUTPUT >> temp",shell=True)#Strip the last 60 lines from the output
		inp=open('temp','r')
		for line in inp.readlines():
			data=line.split()
			if (data[0]=='Summary' and data[1]=='convergence'):
				if data[2]=='1':
					print "Simulation converged"
					conv='1'
				else:
					print "Simulation did not converge"
					conv='0'
			if (data[1]=='Lum_agn='):       #This marks the start of the data we want. Field 14 is the cloudy ionization parameter
				Hout.write(data[14]+' '+data[16]+' '+data[4])
				Heout.write(data[14]+' '+data[16]+' '+data[4])
				Cout.write(data[14]+' '+data[16]+' '+data[4])
				Nout.write(data[14]+' '+data[16]+' '+data[4])
				Oout.write(data[14]+' '+data[16]+' '+data[4])
				Feout.write(data[14]+' '+data[16]+' '+data[4])
				Heat.write(data[14]+' '+data[16]+' '+data[4])
				Cool.write(data[14]+' '+data[16]+' '+data[4])
				Tout.write(data[14]+' '+data[16]+' '+data[4]+' '+data[2]+' '+data[8]+' '+conv+'\n')
				print "Measured U="+str(np.log10(float(data[14])))+' Xi='+str(np.log10(float(data[16])))
				dU=U-np.log10(float(data[14]))
				if abs(dU)>0.01:
					print "Missed target U, change Lum0 to ",lum_0*10**dU
			if (data[1]=='Absorbed_flux(ergs-1cm-3)'):
				Heat.write(' '+data[2]+' '+data[4]+' '+data[6]+' '+data[8]+' '+data[10]+' '+data[12]+' '+data[14]+'\n')
			if (data[1]=='Wind_cooling(ergs-1cm-3)'):
				Cool.write(' '+data[2]+' '+data[4]+' '+data[6]+' '+data[8]+' '+data[10]+' '+data[12]+' '+data[16]+' '+data[14]+'\n')
			if (data[1]=='H'):
				for j in range(2):
					Hout.write(' '+data[j+2])
				Hout.write('\n')
			if (data[1]=='He'):
				for j in range(3):
					Heout.write(' '+data[j+2])
				Heout.write('\n')
			if (data[1]=='C'):
				for j in range(7):
					Cout.write(' '+data[j+2])
				Cout.write('\n')
			if (data[1]=='N'):
				for j in range(8):
					Nout.write(' '+data[j+2])
				Nout.write('\n')
			if (data[1]=='O'):
				for j in range(9):
					Oout.write(' '+data[j+2])
				Oout.write('\n')
			if (data[1]=='Fe'):
				for j in range(27):
					Feout.write(' '+data[j+2])
				Feout.write('\n')
	#Flush the output files so one can see progress and if the loop crashes all is not lost
		Hout.flush()
		Heout.flush()
		Cout.flush()
		Nout.flush()
		Oout.flush()
		Feout.flush()
		Tout.flush()
		Heat.flush()
		Cool.flush()	
		print 'Finished cycle '+str(i+1)+' of '+str(npoints)
		print '\n'
		print '\n'

	#Close the files.
	Hout.close()
	Heout.close()
	Cout.close()
	Nout.close()
	Oout.close()
	Feout.close()
	Tout.close()
	Heat.close()
	Cool.close()

