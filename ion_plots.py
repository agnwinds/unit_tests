#!/usr/bin/env python

def make_ion_plots(folder):
	import matplotlib.pyplot as plt
	import numpy as np
	from astropy.io import ascii
	from matplotlib import rc

	rc('font',**{'family':'serif','serif':['Times']})
	rc('font',size=18)
	rc('text', usetex=True)
	xlim=[-10,5]
	ylim=[0.0001,2.000]


	py='_PL_fixed_t'
	cl='_cloudy_pl_no_ce'
	release_folder = "outputs_release/"
	savefolder = folder

	py_h=ascii.read(folder+'py_hydrogen'+py+'.dat')
	py_he=ascii.read(folder+'py_helium'+py+'.dat')
	py_c=ascii.read(folder+'py_carbon'+py+'.dat')
	py_n=ascii.read(folder+'py_nitrogen'+py+'.dat')
	py_o=ascii.read(folder+'py_oxygen'+py+'.dat')
	py_fe=ascii.read(folder+'py_iron'+py+'.dat')

	py_h_rel=ascii.read(release_folder+'py_hydrogen'+py+'.dat')
	py_he_rel=ascii.read(release_folder+'py_helium'+py+'.dat')
	py_c_rel=ascii.read(release_folder+'py_carbon'+py+'.dat')
	py_n_rel=ascii.read(release_folder+'py_nitrogen'+py+'.dat')
	py_o_rel=ascii.read(release_folder+'py_oxygen'+py+'.dat')
	py_fe_rel=ascii.read(release_folder+'py_iron'+py+'.dat')

	cl_h=ascii.read('cloudy/cl_hydrogen'+cl+'.dat')
	cl_he=ascii.read('cloudy/cl_helium'+cl+'.dat')
	cl_c=ascii.read('cloudy/cl_carbon'+cl+'.dat')
	cl_n=ascii.read('cloudy/cl_nitrogen'+cl+'.dat')
	cl_o=ascii.read('cloudy/cl_oxygen'+cl+'.dat')
	cl_fe=ascii.read('cloudy/cl_iron'+cl+'.dat')



	xlabel="Ionization parameter (cloudy definition)"
	pdetails="1cm thick shell, 1e11cm radius, Nh=1e7"


	fig=plt.figure(figsize=(12,8),dpi=300)
	#fig.subplots_adjust(hspace=0.0,wspace=0.0)
	ax1=fig.add_subplot(111)
	ax1.set_color_cycle(['k','r'])
	ax1.set_title("Hydrogen ionization state")
	for i in range(2):
		ax1.semilogy(np.log10(py_h["U"]),py_h[py_h.keys()[i+3]],label='Python H'+str(i+1))
		ax1.semilogy(np.log10(py_h_rel["U"]),py_h[py_h_rel.keys()[i+3]],"o",label='Release H'+str(i+1))
	for i in range(2):
		ax1.semilogy(cl_h["U"],cl_h[cl_h.keys()[i+1]],'x')
	ax1.set_xlabel(xlabel)
	ax1.set_ylabel("Relative abundance")
	ax1.set_ylim(ylim)
	ax1.set_xlim(xlim)
	ax1.legend(loc='lower right',prop={'size':6})
	fig.savefig(savefolder+'hydrogen.png')
	plt.close(fig)



	fig=plt.figure(figsize=(12,8),dpi=300)
	#fig.subplots_adjust(hspace=0.0,wspace=0.0)
	ax1=fig.add_subplot(111)
	ax1.set_color_cycle(['k','r','b'])
	ax1.set_title("Helium ionization state")
	for i in range(3):
		ax1.semilogy(np.log10(py_he["U"]),py_he[py_he.keys()[i+3]],label='Python He'+str(i+1))
		ax1.semilogy(np.log10(py_he_rel["U"]),py_he_rel[py_he_rel.keys()[i+3]],"o",label='Release He'+str(i+1))
	for i in range(3):
		ax1.semilogy(cl_h["U"],cl_he[cl_he.keys()[i+1]],'x')
	ax1.set_xlabel(xlabel)
	ax1.set_ylabel("Relative abundance")
	ax1.set_ylim(ylim)
	ax1.set_xlim(xlim)
	ax1.legend(loc='lower right',prop={'size':6})
	fig.savefig(savefolder+'helium.png')
	plt.close(fig)

	fig=plt.figure(figsize=(12,8),dpi=300)
	#fig.subplots_adjust(hspace=0.0,wspace=0.0)
	ax1=fig.add_subplot(111)
	ax1.set_color_cycle(['k','r','g','b','c','y','m'])
	ax1.set_title("Carbon ionization state")
	for i in range(7):
		ax1.semilogy(np.log10(py_c["U"]),py_c[py_c.keys()[i+3]],label='Python C'+str(i+1))
		ax1.semilogy(np.log10(py_c_rel["U"]),py_c_rel[py_c_rel.keys()[i+3]],"o",label='Release C'+str(i+1))
	for i in range(7):
		ax1.semilogy(cl_h["U"],cl_c[cl_c.keys()[i+1]],'x')
	ax1.set_xlabel(xlabel)
	ax1.set_ylabel("Relative abundance")
	ax1.set_ylim(ylim)
	ax1.set_xlim(xlim)
	ax1.legend(loc='lower right',prop={'size':6})
	fig.savefig(savefolder+'carbon.png')
	plt.close(fig)


	fig=plt.figure(figsize=(12,8),dpi=300)
	#fig.subplots_adjust(hspace=0.0,wspace=0.0)
	ax1=fig.add_subplot(111)
	ax1.set_color_cycle(['k','r','g','b','c','y','m','k'])
	ax1.set_title("Nitrogen ionization state")
	for i in range(8):
		ax1.semilogy(np.log10(py_n["U"]),py_n[py_n.keys()[i+3]],label='Python N'+str(i+1))
		ax1.semilogy(np.log10(py_n_rel["U"]),py_n_rel[py_n_rel.keys()[i+3]],"o",label='Release N'+str(i+1))
	for i in range(8):
		ax1.semilogy(cl_n["U"],cl_n[cl_n.keys()[i+1]],'x')
	ax1.set_xlabel(xlabel)
	ax1.set_ylabel("Relative abundance")
	ax1.set_ylim(ylim)
	ax1.set_xlim(xlim)
	ax1.legend(loc='lower right',prop={'size':6})
	fig.savefig(savefolder+'nitrogen.png')
	plt.close(fig)



	fig=plt.figure(figsize=(12,8),dpi=300)
	#fig.subplots_adjust(hspace=0.0,wspace=0.0)
	ax1=fig.add_subplot(111)
	ax1.set_color_cycle(['k','r','g','b','c','y','m','k','r'])
	ax1.set_title("Oxygen ionization state")
	for i in range(9):
		ax1.semilogy(np.log10(py_o["U"]),py_o[py_o.keys()[i+3]],label='Python O'+str(i+1))
		ax1.semilogy(np.log10(py_o_rel["U"]),py_o_rel[py_o_rel.keys()[i+3]],"o",label='Release O'+str(i+1))
	for i in range(9):
		ax1.semilogy(cl_n["U"],cl_o[cl_o.keys()[i+1]],'x')
	ax1.set_xlabel(xlabel)
	ax1.set_ylabel("Relative abundance")
	ax1.set_ylim(ylim)
	ax1.set_xlim(xlim)
	ax1.legend(loc='lower right',prop={'size':6})
	fig.savefig(savefolder+'oxygen.png')
	plt.close(fig)



	xlim=[-7,3]

	fig=plt.figure(figsize=(12,8),dpi=300)
	#fig.subplots_adjust(hspace=0.0,wspace=0.0)
	ax1=fig.add_subplot(111)
	ax1.set_color_cycle(['k','r','g','b','c','y','m','k','r'])
	ax1.set_title("Iron ionization state PL modelled as PL in thin shell python")
	for i in range(9):
		ax1.semilogy(np.log10(py_fe["U"]),py_fe[py_fe.keys()[i+3]],label='Python Fe'+str(i+1))
		ax1.semilogy(np.log10(py_fe_rel["U"]),py_fe_rel[py_fe_rel.keys()[i+3]],"o",label='Release Fe'+str(i+1))
	for i in range(9):
		ax1.semilogy(cl_fe["U"],cl_fe[cl_fe.keys()[i+1]],'x')
	ax1.set_xlabel(xlabel)
	ax1.set_ylabel("Relative abundance")
	ax1.set_ylim(ylim)
	ax1.set_xlim(xlim)
	ax1.legend(loc='lower right',prop={'size':6})
	plt.savefig(savefolder+'iron_low_plot.png')
	plt.close(fig)

	xlim=[-1,3]

	fig=plt.figure(figsize=(12,8),dpi=300)
	#fig.subplots_adjust(hspace=0.0,wspace=0.0)
	ax1=fig.add_subplot(111)
	ax1.set_color_cycle(['k','r','g','b','c','y','m','k','r'])
	ax1.set_title("Iron ionization state PL modelled as PL in thin shell python")
	for i in range(9):
		ax1.semilogy(np.log10(py_fe["U"]),py_fe[py_fe.keys()[i+12]],label='Python Fe'+str(i+9))
		ax1.semilogy(np.log10(py_fe_rel["U"]),py_fe_rel[py_fe_rel.keys()[i+12]],"o",label='Release Fe'+str(i+9))
	for i in range(9):
		ax1.semilogy(cl_fe["U"],cl_fe[cl_fe.keys()[i+10]],'x')
	ax1.set_xlabel(xlabel)
	ax1.set_ylabel("Relative abundance")
	ax1.set_ylim(ylim)
	ax1.set_xlim(xlim)
	ax1.legend(loc='lower right',prop={'size':6})
	plt.savefig(savefolder+'iron_mid_plot.png')
	plt.close(fig)

	xlim=[0,7]

	fig=plt.figure(figsize=(12,8),dpi=300)
	#fig.subplots_adjust(hspace=0.0,wspace=0.0)
	ax1=fig.add_subplot(111)
	ax1.set_color_cycle(['k','r','g','b','c','y','m','k','r'])
	ax1.set_title("Iron ionization state PL modelled as PL in thin shell python")
	for i in range(9):
		ax1.semilogy(np.log10(py_fe["U"]),py_fe[py_fe.keys()[i+21]],label='Python Fe'+str(i+18))
		ax1.semilogy(np.log10(py_fe_rel["U"]),py_fe_rel[py_fe_rel.keys()[i+21]],"o",label='Release Fe'+str(i+18))

	for i in range(9):
		ax1.semilogy(cl_fe["U"],cl_fe[cl_fe.keys()[i+19]],'x')
	ax1.set_xlabel(xlabel)
	ax1.set_ylabel("Relative abundance")
	ax1.set_ylim(ylim)
	ax1.set_xlim(xlim)
	ax1.legend(loc='lower right',prop={'size':6})
	plt.savefig(savefolder+'iron_high_plot.png')
	plt.close(fig)


	print "end"

if __name__ == "__main__":

	make_ion_plots(sys.argv[1])
