*** Introduction ***

Ezufo is a GUI to data reconstruction tools of 
ufo-kit software package (https://github.com/ufo-kit). 
It can be used to find the center of rotation and reconstruct 
X-ray uCT slices, to optimize reconstruction parameters, 
and to batch process multiple data sets after experiment.

Distributed without warranty of any kind.


*** Installation requirements ***

1. Working istallation of ufo-core, ufo-python-tools, ufo-filters, 
tofu, and concert is required. This version was tested with
ufo-core:  
https://github.com/ufo-kit/ufo-core/commit/ab39783930ccbe3fa06e0f50427e01376f431256
ufo-filters:
https://github.com/ufo-kit/ufo-filters/commit/2f2dbf96c3075de062e73c655708af516773110c
tofu:
https://github.com/ufo-kit/tofu/commit/6d7c27328bf9397d7f8c7e99ce7520ac90007afa
concert:
https://github.com/ufo-kit/concert/commit/6bb7b3436702adaa2e6df1e0c0e68de6837dd582
2. tkinter.


*** How it works ***

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


*** Tested combinations ***

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

** with RingRemoval
8. RR only                                 	<-- tested
8b. RR with bigtiff input			<-- tested
8c. RR with vert ROI                        	<-- tested
9. RR + PR                                 	<-- tested

** finally
10. Everything enabled                     	<-- tested
