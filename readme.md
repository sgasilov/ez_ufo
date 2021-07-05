<h1> EZUFO </h1>

<h2> Introduction </h2>
  
Ezufo provides a graphical interface to the data reconstruction tools of 
the ufo-kit software package (https://github.com/ufo-kit). 
It can be used to find the center of rotation and reconstruct 
X-ray uCT slices, to optimize reconstruction parameters, 
and to batch process multiple data sets after experiment.

Distributed without warranty of any kind.
  
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
	- python setup.py install –record install_manifest.txt

6. Install EZ_UFO
	- cd ~my/venvs/bmit38/lib
	- git clone https://github.com/sgasilov/ez_ufo.git
	- cd ez_ufo
	- git checkout ez_ufo_qt
	- python setup.py install –record install_manifest.txt
