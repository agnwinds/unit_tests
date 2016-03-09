#!/usr/bin/env python


'''
                    UNLV

Synopsis:  

This routine carries out a series of cloudy simulations for comparison with
thin shell python simulations made in python_pl_loop, the partner code.
We currently write out H,He,C,N,O and Fe. We also output heating and cooling
mechanisms.


Command line usage (if any):

	usage: cloudy_pl_loop *optional file suffix*

Description:  

Primary routines:

Notes:
									   
History:

081214 nsh Commented

'''


if __name__ == "__main__":		# allows one to run from command line without running automatically with write_docs.py

	import sys, subprocess
	import numpy as np


	#Use an optional suffix so file will be py_hydrogen_*suffix*.dat, 
	#If nothing is supplied, default is PL.


	if  len(sys.argv) > 1:
		run_name=sys.argv[1]
	else:
		run_name='cloudy_PL_no_ce'


	distance=inner=1e11       	#Inner shell radius
	outer=1.00000000001e11		#Shell thickness - same as standard python run
	brem_temp=116045193.02808939      #The temperature of the bremstrahlung radiation - equivalent to 10keV
	nh=1e7				#Hydrogen density
	tmin=1e4			#the lower temperature
	tmax=1e8
	npoints=151			#Number of runs
	alpha_agn=-0.9
	xi=3


	temp=np.logspace(np.log10(tmin),np.log10(tmax),npoints)



#	run_name=run_name+"_IP_"+str(xi)
	
	IP_array=np.linspace(-10,5,npoints) 




	Hout=open('cl_hydrogen_'+run_name+'.dat','w')
	Hout.write("U I1 I2\n")
	Heout=open('cl_helium_'+run_name+'.dat','w')
	Heout.write("U I1 I2 I3\n")
	Cout=open('cl_carbon_'+run_name+'.dat','w')
	Cout.write("U I1 I2 I3 I4 I5 I6 I7\n")
	Nout=open('cl_nitrogen_'+run_name+'.dat','w')
	Nout.write("U I1 I2 I3 I4 I5 I6 I7 I8\n")
	Oout=open('cl_oxygen_'+run_name+'.dat','w')
	Oout.write("U I1 I2 I3 I4 I5 I6 I7 I8 I9\n")
	Feout=open('cl_iron_'+run_name+'.dat','w')
	Feout.write("U I1 I2 I3 I4 I5 I6 I7 I8 I9 I10 I11 I12 I13 I14 I15 I16 I17 I18 I19 I20 I21 I22 I23 I24 I25 I26 I27\n")
	Tout=open('cl_temperature_'+run_name+'.dat','w')
	Heat=open('cl_heat_'+run_name+'.dat','w')
	Pcon=open('cl_pcon_'+run_name+'.dat','w')
	Cool=open('cl_cool_'+run_name+'.dat','w')





	log_inner=np.log10(inner)
	log_thickness=np.log10(outer-inner)
	log_hden=np.log10(nh)
	i=0
	for IP in IP_array:
		inp =open('input.in','w')
		print 'Starting cycle '+str(i+1)+' of '+str(len(IP_array))
		i=i+1
		print 'U= '+str(IP)
		inp.write('Table power law [spectral index '+str(alpha_agn)+' low=0.01, hi=1470 ]\n')
		inp.write('ionization parameter '+str((IP))+'\n')
		inp.write('Constant temperature, t=10000\n')
	#	inp.write('no auger\n')
	#	inp.write('no UTA ionization\n')
	#	inp.write('no three body recombination\n')
	#	inp.write('no charge exchange\n')
	#	inp.write('no secondary ionizations\n')
	#	inp.write('no induced processes\n')
		inp.write('radius '+str(log_inner)+' '+str(log_thickness)+'\n')
		inp.write('hden '+str(log_hden)+'\n')
	#Set the abundances to the same as those used in python
		inp.write('abundances he =-1.01 li =-29 be =-29 b =-29 c =-3.44 n =-3.95 o =-3.07 \n')
		inp.write('continue f  =-29 ne =-3.91 na =-5.69 mg =-4.42 \n')
		inp.write('continue al =-5.52 si =-4.45 p  =-29 s  =-4.73 cl =-29 ar =-5.44 k  =-29 \n')
		inp.write('continue ca =-5.66 sc =-29 ti =-29 v  =-29 cr =-29 mn =-29 fe =-4.49 \n')
		inp.write('continue co =-29 ni =-29 cu =-29 zn =-29\n')
	#Just have the elements we use in python
		inp.write('element lithium off\n')
		inp.write('element beryllium off \n')
		inp.write('element boron off \n')
		inp.write('element fluorine  off \n')
		inp.write('element phosphorus  off \n')
		inp.write('element chlorine off \n')
		inp.write('element potassium  off \n')
		inp.write('element calcium off \n')
		inp.write('element cobalt off \n')
		inp.write('element nickel off \n')
		inp.write('element copper off \n')
		inp.write('element zinc off\n')
		inp.write('sphere\n')
		inp.write('no charge exchange\n')
		inp.write('stop column density 22\n')
		inp.write('save heat "heat.dat"\n')
		inp.write('save cool "cool.dat"\n')	
		inp.write('set WeakHeatCool -5\n')
		inp.write('save physical conditions "pcon.dat"\n')
		inp.write('save element iron "iron.dat"\n')
		inp.write('save element oxygen "oxygen.dat"\n')
		inp.write('save element carbon "carbon.dat"\n')
		inp.write('save element nitrogen "nitrogen.dat"\n')
		inp.write('save element helium "helium.dat"\n')
		inp.write('save element hydrogen "hydrogen.dat"\n')
		inp.close()
		subprocess.check_call("time cl13 input",shell=True)
		inp=open('heat.dat','r')
		inp.readline()
		line=inp.readline()
		data=line.split()
		if (data[0]=='Negative'):
			line=inp.readline()
			data=line.split()
		inp.close()
		Tout.write(str(IP)+' '+data[1]+'\n')
		Heat.write(str(IP)+' '+line)
	 	inp=open('cool.dat','r')
		inp.readline()
		line=inp.readline()
		data=line.split()
		inp.close()
		Cool.write(str(IP)+' '+line)
	 	inp=open('pcon.dat','r')
		inp.readline()
		line=inp.readline()
		data=line.split()
		inp.close()
		Pcon.write(str(IP)+' '+line)
		inp=open('iron.dat','r')
		inp.readline()
		line=inp.readline()
		data=line.split()	
		inp.close()
		Feout.write(str(IP))
		for j in range(27):
			Feout.write(' '+str(data[j+1]))
		Feout.write('\n')
		inp=open('oxygen.dat','r')
		inp.readline()
		line=inp.readline()
		data=line.split()	
		inp.close()
		Oout.write(str(IP))
		for j in range(9):
			Oout.write(' '+str(data[j+1]))
		Oout.write('\n')
		inp=open('carbon.dat','r')
		inp.readline()
		line=inp.readline()
		data=line.split()	
		inp.close()
		Cout.write(str(IP))
		for j in range(7):
			Cout.write(' '+str(data[j+1]))
		Cout.write('\n')
		inp=open('nitrogen.dat','r')
		inp.readline()
		line=inp.readline()
		data=line.split()	
		inp.close()
		Nout.write(str(IP))
		for j in range(8):
			Nout.write(' '+str(data[j+1]))
		Nout.write('\n')
		inp=open('helium.dat','r')
		inp.readline()
		line=inp.readline()
		data=line.split()	
		inp.close()
		Heout.write(str(IP))
		for j in range(3):
			Heout.write(' '+str(data[j+1]))
		Heout.write('\n')
		inp=open('hydrogen.dat','r')
		inp.readline()
		line=inp.readline()
		data=line.split()	
		inp.close()
		Hout.write(str(IP))
		for j in range(2):
			Hout.write(' '+str(data[j+1]))
		Hout.write('\n')
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

