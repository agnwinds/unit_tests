### Unit tests for Python

This repository contains unit tests for the Monte Carlo radiative transfer code PYTHON, hosted at 
https://github.com/agnwinds/python.

Fundamentally, this code allows one to run a series of models which should be well understood and fairly stable. Once they are run they can be compared to the latest release outputs which are stored in **outputs_release/**

The models run are generally the same models stored in $PYTHON/examples/core, and consist of:

* cv_standard.pf -- Standard CV model (Shlosman & Vitello 1993; Long & Knigge 2002).
* 1d_sn.pf -- simple Supernovae model as presented in Kerzendorf & Sim (2013).
* star.pf -- simple spherical stellar wind model
* fiducial_agn.pf -- QSO model from Higginbottom et al. (2013).
* cv_macro_benchmark.pf -- Macro-atom CV run from Matthews et al. (2015).
* m16_agn.pf -- Macro-atom AGN run from Matthews et al. (2016).

There is also an ion loop run using a governing python script which relies on the parameter file AGN_vIP.param.

these models have the following runtimes on endjinn

* 1d_sn: 272.6s in serial
* star: 895.6s in serial 
* cv_standard: 3066.8s in serial
* fiducial_agn: 5292.9s on 8 cores
* ion loop: 900s on 8 cores
* m16_agn: 58983.9s (14 hours+) on 8 cores
* cv_macro_benchmark: 47122.2s (13 hours) on 8 cores

### Usage

First, go to $PYTHON and check out the version of python you'd like to test. Compile it.

To run the test 

```
./run_test 80a 1
```

Args: 
* the first argument is the version of Python you have just compiled 
* The second argument set to 1 if you are doing a short run on e.g. a laptop, and runs serial
* If this is set to 2 then the program also runs the fiducial agn and ion loops on multi cores
* If this is set to 3 then the program runs the full test suite and needs a bunch of cores

This will run the test on version python 80a. Note that it copies the parameter files out of $PYTHON/examples to run, so that's why you have to have checked out a compatible version above.

Wait a while.

Once the test has run, you can plot the outputs and check some aspects of the run by typing

```
python plot_output.py
```

### Folders

If you run a test on version 80a on 2016-03-09 then your output files and plots will go into two separate folders entitled

```
test_80a_2016-03-09
plot_80a_2016-03-09
```

### Environment variables

* ```$PYTHON''' must be defined
* $PYTHON/py_progs/ must be in your ```$PYTHONPATH'''