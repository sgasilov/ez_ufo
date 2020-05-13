#!/usr/bin/env python2
'''
Created on Apr 5, 2018

@author: gasilos
'''

import Tkinter as tk
import tkMessageBox
from tkFont import Font
from ez_ufo.main import main_tk, clean_tmp_proj_dirs
import tkFileDialog as filedialog
import numpy as np
import os
from shutil import rmtree
import getpass

E=tk.E; W=tk.W

class tk_args():
    def __init__(self, e_indir, e_tmpdir, e_outdir, e_bigtif, \
                e_ax, e_ax_range, e_ax_row,e_ax_p_size, e_ax_fix, e_dax, \
                e_inp, e_inp_thr, e_inp_sig, \
                e_RR, e_RR_par, \
                e_PR, e_energy, e_pixel, e_z, e_log10db,\
                e_vcrop, e_y, e_yheight, e_ystep,\
                e_gray256, e_bit, e_hmin, e_hmax, \
                e_pre, e_pre_cmd, \
                e_a0, \
                e_crop, e_x0, e_dx, e_y0, e_dy, \
                e_dryrun, e_parfile, e_keep_tmp):
        self.args={}
        # PATHS
        self.args['indir']=str(e_indir.get())
        setattr(self,'indir',self.args['indir'])
        # self.args['bigtif_inp']=bool(e_bigtifinput.get())
        # setattr(self,'bigtif_inp',self.args['bigtif_inp'])
        # self.args['nviews']=int(e_nviews.get())
        # setattr(self,'nviews',self.args['nviews'])
        # self.args['H']=int(e_H.get())
        # setattr(self,'H',self.args['H'])
        # self.args['W']=int(e_W.get())
        # setattr(self,'W',self.args['W'])
        self.args['outdir']=str(e_outdir.get())
        setattr(self,'outdir',self.args['outdir'])
        self.args['tmpdir']=str(e_tmpdir.get())
        setattr(self,'tmpdir',self.args['tmpdir'])
        self.args['bigtif_sli']=bool(e_bigtif.get())
        setattr(self,'bigtif_sli',self.args['bigtif_sli'])
        # center of rotation parameters
        self.args['ax']=int(e_ax.get())
        setattr(self,'ax',self.args['ax'])
        self.args['ax_range']=str(e_ax_range.get())
        setattr(self,'ax_range',self.args['ax_range'])
        self.args['ax_p_size']=int(e_ax_p_size.get())
        setattr(self,'ax_p_size',self.args['ax_p_size'])
        self.args['ax_row']=int(e_ax_row.get())
        setattr(self,'ax_row',self.args['ax_row'])
        self.args['ax_fix']=float(e_ax_fix.get())
        setattr(self,'ax_fix',self.args['ax_fix'])
        self.args['dax']=float(e_dax.get())
        setattr(self,'dax',self.args['dax'])
        #ring removal
        self.args['inp']=bool(e_inp.get())
        setattr(self,'inp',self.args['inp'])
        self.args['inp_thr']=int(e_inp_thr.get())
        setattr(self,'inp_thr',self.args['inp_thr'])
        self.args['inp_sig']=int(e_inp_sig.get())
        setattr(self,'inp_sig',self.args['inp_sig'])
        self.args['RR']=bool(e_RR.get())
        setattr(self,'RR',self.args['RR'])
        self.args['RR_par']=int(e_RR_par.get())
        setattr(self,'RR_par',self.args['RR_par'])
        # phase retrieval
        self.args['PR']=bool(e_PR.get())
        setattr(self,'PR',self.args['PR'])
        self.args['energy']=float(e_energy.get())
        setattr(self,'energy',self.args['energy'])
        self.args['pixel']=float(e_pixel.get())*1e-6
        setattr(self,'pixel',self.args['pixel'])
        self.args['z']=float(e_z.get())
        setattr(self,'z',self.args['z'])
        self.args['log10db']=np.log10(float(e_log10db.get()))
        setattr(self,'log10db',self.args['log10db'])
        # Crop vertically
        self.args['vcrop']=bool(int(e_vcrop.get()))
        setattr(self,'vcrop',self.args['vcrop'])
        self.args['y']=int(e_y.get())
        setattr(self,'y',self.args['y'])
        self.args['yheight']=int(e_yheight.get())
        setattr(self,'yheight',self.args['yheight'])
        self.args['ystep']=int(e_ystep.get())
        setattr(self,'ystep',self.args['ystep'])
        # conv to 8 bit
        self.args['gray256']=bool(int(e_gray256.get()))
        setattr(self,'gray256',self.args['gray256'])
        self.args['bit']=int(e_bit.get())
        setattr(self,'bit',self.args['bit'])
        self.args['hmin']=float(e_hmin.get())
        setattr(self,'hmin',self.args['hmin'])
        self.args['hmax']=float(e_hmax.get())
        setattr(self,'hmax',self.args['hmax'])
        # preprocessing attributes
        self.args['pre']=bool(int(e_pre.get()))
        setattr(self,'pre',self.args['pre'])
        self.args['pre_cmd']=e_pre_cmd.get()
        setattr(self,'pre_cmd',self.args['pre_cmd'])
        # ROI in slice
        self.args['crop']=bool(int(e_crop.get()))
        setattr(self,'crop',self.args['crop'])
        self.args['x0']=int(e_x0.get())
        setattr(self,'x0',self.args['x0'])
        self.args['dx']=int(e_dx.get())
        setattr(self,'dx',self.args['dx'])
        self.args['y0']=int(e_y0.get())
        setattr(self,'y0',self.args['y0'])
        self.args['dy']=int(e_dy.get())
        setattr(self,'dy',self.args['dy'])
        # Optional FBP params
        self.args['a0']= float(e_a0.get())
        setattr(self,'a0',self.args['a0'])
        # misc settings
        self.args['dryrun']=bool(e_dryrun.get())
        setattr(self,'dryrun',self.args['dryrun'])
        self.args['parfile']=bool(e_parfile.get())
        setattr(self,'parfile',self.args['parfile'])
        self.args['keep_tmp']=bool(e_keep_tmp.get())
        setattr(self,'keep_tmp',self.args['keep_tmp'])

class GUI:
    def __init__(self, A):
        self.A = A
        bold_font = Font(weight="bold")
        A.title("E&Z ufo-kit")
        r=0;

        ################### PATHS BLOCK ########################
        #Select input directory
        self.indir = os.getcwd()
        self.input_b = tk.Button(A,\
            text="Select input directory (or paste abs. path)", \
            font=bold_font, command=self.select_indir)
        self.input_b.grid(row=r, column=0, columnspan=2)
        r+=1

        v = tk.StringVar(A, value=self.indir)
        self.e_indir = tk.Entry(A,textvariable=v, width=70)
        self.e_indir.grid(row=r, column=0, columnspan=2, sticky=E)
        r+=1
        # #explicit parameters for multipage tiffs
        # f_mtif = tk.Frame(A)
        # f_mtif.grid(row=r, column=0, columnspan=2)
        # self.e_bigtifinput = tk.BooleanVar(A, value=False)
        # tmp="Frames stored in multipage tifs."
        # f_mtif_b0 = tk.Checkbutton(f_mtif, text=tmp, variable=self.e_bigtifinput)
        # f_mtif_b0.pack(side="left")
        # tmp="For input in multipage tifs define explicitly:"
        # f_mtif_l0 = tk.Label(f_mtif, text=tmp)
        # f_mtif_l0.pack(side="left")
        # r+=1
        # f_mtif_par = tk.Frame(A)
        # f_mtif_par.grid(row=r, column=0, columnspan=2)
        # f_mtif_l1 = tk.Label(f_mtif_par, text="Number of projections")
        # f_mtif_l1.pack(side="left")
        # v = tk.IntVar(A, value=0)
        # self.e_nviews = tk.Entry(f_mtif_par,textvariable=v,width=10);
        # self.e_nviews.pack(side="left")
        # f_mtif_l2 = tk.Label(f_mtif_par, text="  Frames height")
        # f_mtif_l2.pack(side="left")
        # v = tk.IntVar(A, value=0)
        # self.e_H = tk.Entry(f_mtif_par,textvariable=v,width=10);
        # self.e_H.pack(side="left")
        # f_mtif_l3 = tk.Label(f_mtif_par, text="  width")
        # f_mtif_l3.pack(side="left")
        # v = tk.IntVar(A, value=0)
        # self.e_W = tk.Entry(f_mtif_par,textvariable=v,width=10);
        # self.e_W.pack(side="left")
        # r+=1

        #Select output directory
        f0 = tk.Frame(A)
        self.outdir = os.path.abspath(os.getcwd() + '-rec')
        b0_1 = tk.Button(f0,\
            text="Select output directory (or paste abs. path)", \
            font=bold_font, command=self.select_outdir)
        #Save in separate files of in one huge tiff file
        self.e_bigtif = tk.BooleanVar(A, value=True)
        tmp="Save slices in multipage tifs"
        b0_2 = tk.Checkbutton(f0, text=tmp, variable=self.e_bigtif)
        f0.grid(row=r, column=0, columnspan=2)
        b0_1.pack(side="left")
        b0_2.pack(side="right")
        r+=1

        v = tk.StringVar(A, value=self.outdir)
        self.e_outdir = tk.Entry(A,textvariable=v, width=70)
        self.e_outdir.grid(row=r, column=0, columnspan=2, sticky=E)
        r+=1

        ################### AXIS OF ROTATION BLOCK ##############
        tk.Label(A, text="Center of rotation", \
                font=bold_font, fg="darkgreen").grid(row=r);
        r+=1
        self.e_ax = tk.IntVar(A, value=1)
        tmp="Auto: Correlate first/last projections"
        tk.Radiobutton(A, text=tmp, font=bold_font, fg="darkgreen",\
                    variable=self.e_ax, value=1).grid(row=r, column=0)
        r+=1

        tmp="Auto: Minimize STD of a slice"
        tk.Radiobutton(A, text=tmp, font=bold_font, fg="darkgreen",
                    variable=self.e_ax, value=2).grid(row=r, column=0)
        r+=1
        tk.Label(A, text="Search rotation axis in start,stop,step interval:"\
                ,fg="darkgreen").grid(row=r);
        v = tk.StringVar(A, value='1010,1030,0.5')
        self.e_ax_range = tk.Entry(A,textvariable=v);
        self.e_ax_range.grid(row=r, column=1, sticky=E)
        r+=1

        tk.Label(A, text="Search in slice from row number"\
                    ,fg="darkgreen").grid(row=r);
        v = tk.IntVar(A, value=100)
        self.e_ax_row = tk.Entry(A,textvariable=v);
        self.e_ax_row.grid(row=r, column=1, sticky=E);
        r+=1

        tk.Label(A, text="Side of reconstructed patch [pixel]"\
                    ,fg="darkgreen").grid(row=r);
        v = tk.IntVar(A, value=256)
        self.e_ax_p_size = tk.Entry(A,textvariable=v);
        self.e_ax_p_size.grid(row=r, column=1, sticky=E);
        r+=1

        tmp="Define rotation axis manually"
        tk.Radiobutton(A, text=tmp, font=bold_font, fg="darkgreen",
                    variable=self.e_ax, value=3).grid(row=r, column=0)
        r+=1

        tk.Label(A, text="Axis is in column No [pixel]"\
                    ,fg="darkgreen").grid(row=r);
        v = tk.DoubleVar(A)
        self.e_ax_fix = tk.Entry(A,textvariable=v);
        self.e_ax_fix.grid(row=r, column=1, sticky=E); r+=1

        tk.Label(A, text="Increment axis every reconstruction"\
                    ,fg="darkgreen").grid(row=r);
        self.e_dax = tk.Entry(A,textvariable=tk.DoubleVar(A));
        self.e_dax.grid(row=r, column=1, sticky=E); r+=1

        ################### RING REMOVAL BLOCK ##############
        self.e_inp = tk.BooleanVar(A, value=False)
        tmp="Remove large spots from projections"
        tk.Checkbutton(A, text=tmp, font=bold_font, fg="darkorange3", \
                        variable=self.e_inp).grid(row=r, column=0)
        r+=1

        tmp="Threshold (prominence of the spot) [counts]"
        tk.Label(A, text=tmp, fg="darkorange3").grid(row=r);
        v = tk.IntVar(A, value=1000)
        self.e_inp_thr = tk.Entry(A,textvariable=v);
        self.e_inp_thr.grid(row=r, column=1, sticky=E); r+=1

        tmp="Spot blur, sigma [pixels]"
        tk.Label(A, text=tmp, fg="darkorange3").grid(row=r);
        v = tk.IntVar(A, value=2)
        self.e_inp_sig = tk.Entry(A,textvariable=v);
        self.e_inp_sig.grid(row=r, column=1, sticky=E); r+=1

        self.e_RR = tk.BooleanVar(A, value=False)
        tmp="Enable ring removal"
        tk.Checkbutton(A, text=tmp, font=bold_font, fg="darkorange3", \
                        variable=self.e_RR).grid(row=r, column=0)
        r+=1

        #tmp="1,2,3 Low-pass Fourier filt; >5 window size for median filt"
        tmp="Set 1,2,3 to suppress thin rings or odd number >5 for wide"
        tk.Label(A, text=tmp, fg="darkorange3").grid(row=r);
        v = tk.IntVar(A, value=2)
        self.e_RR_par = tk.Entry(A,textvariable=v);
        self.e_RR_par.grid(row=r, column=1, sticky=E); r+=1

        ################### PHASE RETRIEVAL ##############
        self.e_PR = tk.BooleanVar(A, value=False)
        tmp="Enable Paganin/TIE phase retrieval"
        tk.Checkbutton(A, text=tmp, font=bold_font, fg="blue", \
                        variable=self.e_PR).grid(row=r, column=0)
        r+=1

        tk.Label(A, text="Photon energy [keV]"\
                        ,fg="blue").grid(row=r);
        v = tk.DoubleVar(A, value=20)
        self.e_energy = tk.Entry(A,textvariable=v);
        self.e_energy.grid(row=r, column=1, sticky=E); r+=1

        tk.Label(A, text="Pixel size [micron]",\
                            fg="blue").grid(row=r);
        v = tk.DoubleVar(A, value=3.6)
        self.e_pixel = tk.Entry(A,textvariable=v);
        self.e_pixel.grid(row=r, column=1, sticky=E); r+=1

        tk.Label(A, text="Sample-detector distance [m]"\
                    ,fg="blue").grid(row=r);
        v = tk.DoubleVar(A, value=0.1)
        self.e_z = tk.Entry(A, textvariable=v);
        self.e_z.grid(row=r, column=1, sticky=E); r+=1

        tk.Label(A, text="Delta/beta ratio; (try default if unsure)"\
                        ,fg="blue").grid(row=r);
        v = tk.DoubleVar(A, value=200)
        self.e_log10db = tk.Entry(A,textvariable=v);
        self.e_log10db.grid(row=r, column=1, sticky=E); r+=1

        ################### PRE/POST PROCESSING ##############
        ### Crop vertically
        self.e_vcrop = tk.BooleanVar(A, value=False)
        tmp="Select rows which will be reconstructed"
        tk.Checkbutton(A, text=tmp, font=bold_font, fg="firebrick2", \
                        variable=self.e_vcrop).grid(row=r, column=0)
        r+=1

        tk.Label(A, text="First row in projections"\
                ,fg="firebrick2").grid(row=r);
        v = tk.IntVar(A, value=100)
        self.e_y = tk.Entry(A,textvariable=v);
        self.e_y.grid(row=r, column=1, sticky=E); r+=1

        tk.Label(A, text="Number of rows (ROI height)"\
                ,fg="firebrick2").grid(row=r);
        v = tk.IntVar(A, value=200)
        self.e_yheight = tk.Entry(A,textvariable=v);
        self.e_yheight.grid(row=r, column=1, sticky=E); r+=1

        tk.Label(A, text="Reconstruct every Nth row"\
                ,fg="firebrick2").grid(row=r);
        v = tk.IntVar(A, value=20)
        self.e_ystep = tk.Entry(A,textvariable=v);
        self.e_ystep.grid(row=r, column=1, sticky=E); r+=1

        ### Convert to 8 bit
        self.e_gray256 = tk.BooleanVar(A, value=False)
        tmp="Clip histogram and save slices in"
        tk.Checkbutton(A, text=tmp, font=bold_font, fg="magenta4", \
                        variable=self.e_gray256).grid(row=r, column=0)

        f_bits = tk.Frame(A)
        self.e_bit = tk.IntVar(A, value=8)
        tk.Radiobutton(f_bits, text='8 bit', fg="magenta4",\
                    variable=self.e_bit, value=8).pack(side="left")
        tk.Radiobutton(f_bits, text='16 bit', fg="magenta4",\
                    variable=self.e_bit, value=16).pack(side="left")
        f_bits.grid(row=r, column=1)

        r+=1

        tk.Label(A, text="Min value in 32-bit histogram"\
                ,fg="magenta4").grid(row=r);
        self.e_hmin = tk.Entry(A,textvariable=tk.DoubleVar());
        self.e_hmin.grid(row=r, column=1, sticky=E); r+=1

        tk.Label(A, text="Max value in 32-bit histogram"\
                ,fg="magenta4").grid(row=r);
        self.e_hmax = tk.Entry(A,textvariable=tk.DoubleVar());
        self.e_hmax.grid(row=r, column=1, sticky=E); r+=1

        ### Generic ufo pipeline
        self.e_pre = tk.BooleanVar(A, value=False)
        tmp="Preprocess with a generic ufo-launch pipeline, f.i."
        tk.Checkbutton(A, text=tmp, font=bold_font, fg="sienna4", \
                        variable=self.e_pre).grid(row=r, column=0)
        r+=1
        #tmp='crop x=500 y=10args0 width=1000 height=50 ! bin size=2'
        tmp = 'remove_outliers size=3 threshold=500 sign=1'
        v = tk.StringVar(A, value=tmp)
        self.e_pre_cmd = tk.Entry(A,textvariable=v, width=70)
        self.e_pre_cmd.grid(row=r, column=0, columnspan=2, sticky=E)
        r+=1

        ##### Optional FBP parameters
        #tk.Label(A, text="Optional FBP parameters", \
        #        font=bold_font, fg="sienna4").grid(row=r);
        #r+=1

        #self.e_step.grid(row=r, column=1, sticky=E); r+=1

        ###### Crop in the reconstruction plane
        self.e_crop = tk.BooleanVar(A, value=False)
        tmp="Crop slices in the reconstruction plane"
        tk.Checkbutton(A, text=tmp, font=bold_font, fg="sienna4", \
                        variable=self.e_crop).grid(row=r, column=0)
        r+=1

        f2 = tk.Frame(A)
        f2.grid(row=r, column=0, columnspan=2)
        bx0 = tk.Label(f2, text="x",fg="sienna4")
        self.e_x0 = tk.Entry(f2,textvariable=tk.IntVar(A),width=10);
        bdx = tk.Label(f2, text="width",fg="sienna4")
        self.e_dx = tk.Entry(f2,textvariable=tk.IntVar(A),width=10);
        by0 = tk.Label(f2, text="y",fg="sienna4")
        self.e_y0 = tk.Entry(f2,textvariable=tk.IntVar(A),width=10);
        bdy = tk.Label(f2, text="height",fg="sienna4")
        self.e_dy = tk.Entry(f2,textvariable=tk.IntVar(A),width=10);

        bx0.pack(side="left")
        self.e_x0.pack(side="left")
        bdx.pack(side="left")
        self.e_dx.pack(side="left")
        by0.pack(side="left")
        self.e_y0.pack(side="left")
        bdy.pack(side="left")
        self.e_dy.pack(side="left")
        r+=1
        # optinal - rotate
        tk.Label(A, text="Optional: rotate volume clockwise by [deg]"\
                ,fg="sienna4").grid(row=r);
        v = tk.DoubleVar(A, value=0.0)
        self.e_a0 = tk.Entry(A,textvariable=v);
        self.e_a0.grid(row=r, column=1, sticky=E); r+=1

        ##### names of directories with flats/darks/projections frames
        tmp="Name of flats/darks/tomo subdirectories in each CT data set"
        tk.Label(A, text=tmp, fg="gray21").grid(row=r, column=0, columnspan=2);
        r+=1
        f3 = tk.Frame(A)
        f3.grid(row=r, column=0, columnspan=2)
        DIRTYP=['darks','flats', 'tomo', 'flats2']
        self.e_DIRTYP=[]
        for i,dtyp in enumerate(DIRTYP):
            v=tk.StringVar(A, value=dtyp)
            self.e_DIRTYP.append( tk.Entry(f3,textvariable=v,width=10) )
            self.e_DIRTYP[i].pack(side="left")
        r+=1

#        #Select temporary directory
#        self.tmpdir = os.getcwd()
#        self.tmpdir = os.path.join("/data", 'tmp-ezufo')
#        self.tmpdir_b = tk.Button(A,\
#            text="Directory for temporary data", \
#            command=self.select_tmpdir)
#        #self.tmpdir_b.configure(state=tk.DISABLED)
#        self.tmpdir_b.grid(row=r, column=0, columnspan=2)
#        r+=1

#        v = tk.StringVar(A, value=self.tmpdir)
#        self.e_tmpdir = tk.Entry(A,textvariable=v, width=70)
#        #self.e_tmpdir.configure(state=tk.DISABLED)
#        self.e_tmpdir.grid(row=r, column=0, columnspan=2, sticky=E)
#        r+=1

        #Select temporary directory
        f_tmpdata = tk.Frame(A)
        self.tmpdir = os.getcwd()
        self.tmpdir = os.path.join("/data", 'tmp-ezufo')
        b_tmpdata_0 = tk.Button(f_tmpdata,\
            text="Select temporary directory", \
            command=self.select_tmpdir)
        #Save in separate files of in one huge tiff file
        self.e_keep_tmp = tk.BooleanVar(A, value=False)
        tmp="Keep all tmp data till the end of reconstruction"
        b_tmpdata_1 = tk.Checkbutton(f_tmpdata, \
                        text=tmp, variable=self.e_keep_tmp)
        f_tmpdata.grid(row=r, column=0, columnspan=2)
        b_tmpdata_0.pack(side="left")
        b_tmpdata_1.pack(side="right")
        #b_tmpdata_0.configure(state=tk.DISABLED)
        #b_tmpdata_1.configure(state=tk.DISABLED)
        r+=1

        v = tk.StringVar(A, value=self.tmpdir)
        self.e_tmpdir = tk.Entry(A,textvariable=v, width=70)
        #self.e_tmpdir.configure(state=tk.DISABLED)
        self.e_tmpdir.grid(row=r, column=0, columnspan=2, sticky=E)
        r+=1

        ############### EXECUTION BUTTONS ###################
        f1 = tk.Frame(A)
        b1 = tk.Button(f1, text='Quit', font=bold_font, command=self.clean_and_quit)
        b2 = tk.Button(f1, text='Help', command=self.printhelp)
        b3 = tk.Button(f1, text='Delete reco dir', \
                    command=self.rm_rec_dir)
        self.e_dryrun = tk.BooleanVar(A, value=False)
        b4 = tk.Button(f1, text='Dry run', \
                    command=self.dry_run)
        self.e_parfile = tk.BooleanVar(A, value=True)
        tmp="Save args"
        b6 = tk.Checkbutton(f1, \
                        text=tmp, variable=self.e_parfile)
        f1.grid(row=r, column=0)
        b1.pack(side="left")
        b2.pack(side="left")
        b3.pack(side="left")
        #b3.configure(state=tk.DISABLED)
        b4.pack(side="left")
        b6.pack(side="left")
        b5 = tk.Button(A, text='Reconstruct', font=bold_font, fg="red3", \
                    command=self.reco)
        b5.grid(row=r,column=1)

    def clean_and_quit(self):
        clean_tmp_proj_dirs(self.e_tmpdir.get())
        self.A.quit()

    def select_indir(self):
        cwd = self.e_indir.get()
        if cwd=='':
            cwd = '/mnt/BMIT_data/BMIT-USERS-DATA'
        tmp = "Select input directory"
        self.indir = filedialog.askdirectory(\
                  initialdir = cwd, title = tmp)
        self.e_indir.delete(0, tk.END)
        self.e_indir.insert(0, self.indir)

    def select_outdir(self):
        tmp = "Select output directory"
        cwd = self.e_outdir.get()
        if cwd=='':
            cwd = '/mnt/BMIT_data/BMIT-USERS-DATA/rec'
        self.outdir = filedialog.askdirectory(\
                  initialdir = cwd, title = tmp)
        self.e_outdir.delete(0, tk.END)
        self.e_outdir.insert(0, self.outdir)

    def select_tmpdir(self):
        tmp = "Select temporary directory"
        self.tmpdir = filedialog.askdirectory(\
                  initialdir = os.getcwd(), title = tmp)
        self.e_tmpdir.delete(0, tk.END)
        self.e_tmpdir.insert(0, self.tmpdir)


    def dry_run(self):
        self.e_dryrun = tk.BooleanVar(self.A, value=True)
        self.reco()
        self.e_dryrun = tk.BooleanVar(self.A, value=False)

    def reco(self):
        args=tk_args(self.e_indir, self.e_tmpdir, self.e_outdir, self.e_bigtif,\
            self.e_ax, self.e_ax_range, self.e_ax_row, self.e_ax_p_size, self.e_ax_fix, self.e_dax, \
            self.e_inp, self.e_inp_thr, self.e_inp_sig, \
            self.e_RR, self.e_RR_par, \
            self.e_PR, self.e_energy, self.e_pixel, self.e_z, self.e_log10db,\
            self.e_vcrop,self.e_y, self.e_yheight, self.e_ystep,\
            self.e_gray256, self.e_bit, self.e_hmin, self.e_hmax, \
            self.e_pre, self.e_pre_cmd, \
            self.e_a0, \
            self.e_crop, self.e_x0, self.e_dx, self.e_y0, self.e_dy, \
            self.e_dryrun, self.e_parfile, self.e_keep_tmp)

        DIRTYP = []
        for i in self.e_DIRTYP:
            DIRTYP.append(i.get())

        main_tk(args, DIRTYP)

    def rm_rec_dir(self):
        titletext = "Warning: data can be lost"
        text1 = "Delete directory with reconstructed data?"
        text2 = "Cannot delete: output directory is the same as input"
        dd = tkMessageBox.askyesno(titletext,text1)
        if dd and os.path.exists(self.e_outdir.get()):
            if self.e_outdir.get() == self.e_indir.get():
                tkMessageBox.showinfo("Warning", text2)
            else:
                os.system( 'rm -rf {}'.format(self.e_outdir.get()) )
                print "Directory with reconstructed data was removed"

    def printhelp(self):
          h="This utility provides an interface to the ufo-kit software package.\n"
          h+="Use it for batch processing and optimization of reconstruction parameters.\n"
          h+="It creates a list of paths to all CT directories in the _input_ directory.\n"
          h+="A CT directory is defined as directory with at least \n"
          h+="_flats_, _darks_, _tomo_, and, optionally, _flats2_ subdirectories, \n"
          h+="which are not empty and contain only *.tif files. Names of CT\n"
          h+="directories are compared with the directory tree in the _output_ directory.\n"
          h+="(Note: relative directory tree in _input_ is preserved when writing results to the _output_.)\n"
          h+="Those CT sets will be reconstructed, whose names are not yet in the _output_ directory."
          h+="Program will create an array of ufo/tofu commands according to defined parameters \n"
          h+="and then execute them sequentially. These commands can be also printed on the screen.\n"
          h+="Note2: if you bin in preprocess the center of rotation will change a lot; \n"
          h+="Note4: set to \"flats\" if \"flats2\" exist but you need to ignore them; \n"
          h+="SerG, BMIT CLS, Dec. 2018."
          print h

if __name__=="__main__":
    A = tk.Tk()
    ez_ufo_gui = GUI(A)
    A.mainloop()























