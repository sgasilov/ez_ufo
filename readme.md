<h1> EZ-UFO </h1>

<h2> Introduction </h2>
  
EZ-UFO provides a graphical interface to the data reconstruction tools of 
the ufo-kit software package (https://github.com/ufo-kit). 
It can be used to find the center of rotation and reconstruct 
X-ray microCT slices, to optimize reconstruction parameters, 
and to batch process multiple data sets after an experiment.

Distributed without warranty of any kind.
Main Tab             |  Image Viewer
:-------------------------:|:-------------------------:
<img src="https://github.com/sgasilov/ez_ufo/blob/ez_ufo_qt/ezufo_interface1.png" alt="drawing" width="50%"/>  |  <img src="https://github.com/sgasilov/ez_ufo/blob/ez_ufo_qt/ezufo_interface2.png" alt="drawing" width="50%"/>


  
<h2> Installation Requirements </h2>
  
1. Working installation of ufo-core, ufo-python-tools, ufo-filters, 
tofu, and concert is required. This version was tested with
* ufo-core:  
https://github.com/ufo-kit/ufo-core/commit/ab39783930ccbe3fa06e0f50427e01376f431256
* ufo-filters:
https://github.com/ufo-kit/ufo-filters/commit/2f2dbf96c3075de062e73c655708af516773110c
* tofu:
https://github.com/ufo-kit/tofu/commit/6d7c27328bf9397d7f8c7e99ce7520ac90007afa
* concert:
https://github.com/ufo-kit/concert/commit/6bb7b3436702adaa2e6df1e0c0e68de6837dd582

<h2> Installation Instructions </h2>

1. Install Python 3.8
- https://www.python.org/downloads/release/python-384/
- https://www.liquidweb.com/kb/how-to-install-python-3-on-centos-7/
- Save python tarball to /opt or some other directory
	- wget https://www.python.org/ftp/python/3.8.4/Python-3.8.4.tgz
- Unzip tarball
	- tar -xzf Python-3.8.4.tgz
	- cd Python-3.8.4
- Compile and install Python
	- ./configure –enable-optimizations
	- <addr> make altinstall </addr>

2. Install virtualenv
	- python3.8 -m pip install virtualenv
	- virtualenv –python=$(which python3.8) ~/my_venvs/bmit38
	
3. Activate virtualenv
	- source ~/my_venvs/bmit38/bin/activate

4. Install python modules
	- pip install -r requirements.txt

5. Download and install Tofu
	- cd ~/my_venvs/bmit38/lib
	- git clone https://github.com/ufo-kit/tofu.git
	- cd tofu
	- git checkout flow	
	- python setup.py install –-record install_manifest.txt

6. Install EZ_UFO
	- cd ~my/venvs/bmit38/lib
	- git clone https://github.com/sgasilov/ez_ufo.git
	- cd ez_ufo
	- git checkout ez_ufo_qt
	- python setup.py install –-record install_manifest.txt

<h2> How it works </h2>

![Image of Block Scheme](https://github.com/sgasilov/ez_ufo/blob/ez_ufo_qt/ezufo_block-scheme.jpg)

It the beginning ezufo creates a list of paths to all CT directories 
in the input directory recursively. A CT directory is defined as any 
directory, which containing a set of flats, darks, tomo, and, optionally, 
flats2 subdirectories. These subdirectories must contain only *.tif files 
with CT data. Names of directories with CT data sets are compared with the 
directory tree in the output directory. Those CT sets will be reconstructed,
whose names are not yet in the output directory. Ezufo will create a 
list of formatted ufo-launch/tofu commands according to defined parameters. 
These commands can be executed or printed on the screen. 

Three or more pre-processing steps can be applied to data:
- An arbitrary pipeline of ufo-launch filters
- Removal of large spots (scintillator defects)
- Paganing/TIE phase retrieval.
Sinograms can be created and filtered in order to suppress ring artifacts.
Finally, CT reconstruction is performed with tofu reco algorithm. 
Region of interest and other miscellaneous parameters can be defined.

All temporary data is saved in multi-page tif files. It will be preserved
in the temporary directory until the next reconstruction or until the
Quit button is pressed. Note that the size of temporary data can easily
exceed 300 GB when multiple processing steps are applied to a large CT set.

<h2> Tested Combinations </h2>

** w/o RingRemoval
1. Straight CT with "corr" axis search	        <-- tested
1b. Straight CT with "min std" axis search      <-- tested
1c. CT search axis "corr" and bigtiff input	<-- tested
2. PR + CT                                 	<-- tested
2b. PR + CT + vertical ROI                 	<-- tested
2. Prepro                                  	<-- tested
3. Prepro and inp                          	<-- tested 
4. Prepro and inp and PR:                  	<-- tested
4b. Prepro and inp and PR + vert ROI      	<-- tested
5. Inp                                     	<-- tested
5b. Inp with multipage input		   	<-- tested
6. Inp and PR                              	<-- tested
7. RR only                                 	<-- tested
7b. RR with bigtiff input			<-- tested
7c. RR with vert ROI                        	<-- tested
8. RR + PR                                 	<-- tested
9. Everything enabled                     	<-- tested
