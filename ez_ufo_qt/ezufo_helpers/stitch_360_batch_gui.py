#!/usr/bin/env python2
'''
Created on Apr 5, 2018

@author: gasilos, bondt
'''

import Tkinter as tk
import tkFileDialog as filedialog
import numpy as np
import os
from stitch_funcs import main_360_mp_depth2
import getpass

E=tk.E; W=tk.W

class tk_args():
    def __init__(self, e_input, e_output, e_tmpdir, e_ax1, e_ax2, e_ax, e_crop):

        self.args={}
        # directories
        self.args['input']=str(e_input.get())
        setattr(self,'input',self.args['input'])
        self.args['output']=str(e_output.get())
        setattr(self,'output',self.args['output'])
        self.args['tmpdir']=str(e_tmpdir.get())
        setattr(self,'tmpdir',self.args['tmpdir'])
        #hor stitch half acq mode
        self.args['ax1']=int(e_ax1.get())
        setattr(self,'ax1',self.args['ax1'])
        self.args['ax2']=int(e_ax2.get())
        setattr(self,'ax2',self.args['ax2'])
        self.args['ax']=int(e_ax.get())
        setattr(self,'ax',self.args['ax'])
        self.args['crop']=int(e_crop.get())
        setattr(self,'crop',self.args['crop'])

class GUI:
    def __init__(self, A):
        self.A = A
        A.title("Stitches multiple images of the same type stored in subdirectories")
        r=0;

        #Select input directory
        self.input = os.getcwd()
        self.input_b = tk.Button(A,\
            text="Select Input directory with a 000,001,...00N subdirectories", \
            command=self.select_input)
        self.input_b.grid(row=r, column=0, columnspan=2)
        r+=1

        v = tk.StringVar(A, value=self.input)
        self.e_input = tk.Entry(A,textvariable=v, width=70)
        self.e_input.grid(row=r, column=0, columnspan=2, sticky=E)
        r+=1

        #Select temporary directory
        self.tmpdir = os.getcwd()
        self.tmpdir = os.path.join("/data", 'tmp-ezstitch-'+getpass.getuser() )
        self.tmpdir_b = tk.Button(A,\
            text="Select temporary directory - default value recommended", \
            command=self.select_tmpdir)
        self.tmpdir_b.grid(row=r, column=0, columnspan=2)
        self.tmpdir_b.configure(state=tk.DISABLED)
        r+=1

        v = tk.StringVar(A, value=self.tmpdir)
        self.e_tmpdir = tk.Entry(A,textvariable=v, width=70)
        self.e_tmpdir.grid(row=r, column=0, columnspan=2, sticky=E)
        r+=1

        #Select output directory
        cwd = os.getcwd() + '-stitched'
        #cwd = os.path.abspath(os.path.join(cwd, os.pardir))
        self.output = cwd
        self.output_b = tk.Button(A,\
            text="Directory to save stitched images", \
            command=self.select_output)
        self.output_b.grid(row=r, column=0, columnspan=2)
        r+=1

        v = tk.StringVar(A, value=self.output)
        self.e_output = tk.Entry(A,textvariable=v, width=70)
        self.e_output.grid(row=r, column=0, columnspan=2, sticky=E)
        r+=1

        #other parameters
        # tk.Label(A, text="Type of images to stitch (e.g. sli, tomo, proj-pr, etc.)"\
        #         ,fg="darkorange3").grid(row=r);
        # v = tk.StringVar(A, value='sli')
        # self.e_typ = tk.Entry(A,textvariable=v);
        # self.e_typ.grid(row=r, column=1, sticky=E)
        # r+=1

        # tmp="Stitch orthogonal sections"
        # self.e_ort = tk.BooleanVar(A, value=True)
        # tk.Checkbutton(A, text=tmp, fg="darkorange3", \
        #                 variable=self.e_ort).grid(row=r, column=0)
        # r+=1

        # tk.Label(A, text="Which images to be stitched: start,stop,step:"\
        #         ,fg="blue").grid(row=r);
        # v = tk.StringVar(A, value='200,2000,200')
        # self.e_slices = tk.Entry(A,textvariable=v);
        # self.e_slices.grid(row=r, column=1, sticky=E)
        # r+=1

        self.e_crop = tk.BooleanVar(A, value=True)
        tmp="crop all projections to match width of smallest stitched projection"
        tk.Checkbutton(A, text=tmp, fg="blue", \
                variable=self.e_crop).grid(row=r, column=0)
        r+=1

        # self.e_ipol = tk.IntVar(A, value=2)
        # tmp="Interpolate overlapping regions and equalize intensity"
        # tk.Radiobutton(A, text=tmp, fg="magenta4",\
        #             variable=self.e_ipol, value=0).grid(row=r, column=0)
        # r+=1

        # tk.Label(A, text="Number of overlapping rows"\
        #             ,fg="magenta4").grid(row=r);
        # v = tk.IntVar(A, value=60)
        # self.e_reprows = tk.Entry(A,textvariable=v);
        # self.e_reprows.grid(row=r, column=1, sticky=E); r+=1

        # ##########  Convert to 8 bit
        # self.e_gray256 = tk.BooleanVar(A, value=False)
        # tmp="Clip histogram and convert slices to 8bit before saving"
        # tk.Checkbutton(A, text=tmp, fg="magenta4", \
        #         variable=self.e_gray256).grid(row=r, column=0)
        # r+=1

        # tk.Label(A, text="Min value in 32-bit histogram"\
        #         ,fg="magenta4").grid(row=r);
        # v = tk.DoubleVar(A, value=-3e-4)
        # self.e_hmin = tk.Entry(A,textvariable=v);
        # self.e_hmin.grid(row=r, column=1, sticky=E); r+=1

        # tk.Label(A, text="Max value in 32-bit histogram"\
        #         ,fg="magenta4").grid(row=r);
        # v = tk.DoubleVar(A, value=2e-4)
        # self.e_hmax = tk.Entry(A,textvariable=v);
        # self.e_hmax.grid(row=r, column=1, sticky=E); r+=1

        # tmp="Concatenate only"
        # tk.Radiobutton(A, text=tmp, fg="darkgreen",\
        #             variable=self.e_ipol, value=1).grid(row=r, column=0)
        # r+=1

        # f2 = tk.Frame(A)
        # f2.grid(row=r, column=0)
        # br1 = tk.Label(f2, text="First row",fg="darkgreen")
        # self.e_r1 = tk.Entry(f2,textvariable=tk.IntVar(A, value=40),width=10);
        # br2 = tk.Label(f2, text="Last row",fg="darkgreen")
        # self.e_r2 = tk.Entry(f2,textvariable=tk.IntVar(A, value=440),width=10);
        # br1.pack(side="left")
        # self.e_r1.pack(side="left")
        # br2.pack(side="left")
        # self.e_r2.pack(side="left")
        # r+=1

        # tmp="Half acqusition mode"
        # tk.Radiobutton(A, text=tmp, fg="brown",\
        #             variable=self.e_ipol, value=2).grid(row=r, column=0)
        # r+=1

        tk.Label(A, text="Axis of Rotation at bottom (z00):"\
                    ,fg="brown").grid(row=r);
        v = tk.IntVar(A, value=245)
        self.e_ax1 = tk.Entry(A,textvariable=v);
        self.e_ax1.grid(row=r, column=1, sticky=E); 
        r+=1
        
        tk.Label(A, text="Axis of Rotation at top (ignored if not multi-slice):"\
                    ,fg="brown").grid(row=r);
        v = tk.IntVar(A, value=245)
        self.e_ax2 = tk.Entry(A,textvariable=v);
        self.e_ax2.grid(row=r, column=1, sticky=E); 
        r+=1
        
        self.e_ax = self.e_ax1


        #launch buttons
        f1 = tk.Frame(A)
        b1 = tk.Button(f1, text='Stitch', fg="red3", command=self.stitch)
        b2 = tk.Button(f1, text='Delete output dir', command=self.rm_rec_dir)
        b2.configure(state=tk.DISABLED)
        b3 = tk.Button(f1, text='Help', command=self.printhelp)
        b4 = tk.Button(f1, text='Quit', command=self.clean_and_quit)
        f1.grid(row=r, column = 0, columnspan = 2)
        b1.pack(side="left")
        b2.pack(side="left")
        b3.pack(side="left")
        b4.pack(side="left")

    def rm_rec_dir(self):
        if os.path.exists(self.e_output.get()):
           os.system( 'rm -r {}'.format(self.e_output.get()) )
           print("Directory with reconstructed data was removed")

    def select_input(self):
        cwd = '/mnt/BMIT_data/BMIT-USERS-DATA'
        tmp = "Select directory with CT scans"
        self.output = filedialog.askdirectory(\
                  initialdir = cwd, title = tmp)
        self.e_input.delete(0, tk.END)
        self.e_input.insert(0, self.output)

    def select_output(self):
        cwd = '/mnt/BMIT_data/BMIT-USERS-DATA/rec'
        tmp = "Select output directory"
        self.output = filedialog.askdirectory(\
                  initialdir = cwd, title = tmp)
        self.e_output.delete(0, tk.END)
        self.e_output.insert(0, self.output)

    def select_tmpdir(self):
        tmp = "Select temporary directory"
        self.tmpdir = filedialog.askdirectory(\
                  initialdir = "/data", title = tmp)
        self.e_tmpdir.delete(0, tk.END)
        self.e_tmpdir.insert(0, self.tmpdir)

    def stitch(self):
        args=tk_args(self.e_input, self.e_output, self.e_tmpdir, self.e_ax1, self.e_ax2, self.e_ax, self.e_crop)

        if os.path.exists(self.e_tmpdir.get()):
            os.system( 'rm -r {}'.format(self.e_tmpdir.get()) )

        if os.path.exists(self.e_output.get()):
            raise ValueError('Output directory exists')

        main_360_mp_depth2(args)

    def clean_and_quit(self):
        if os.path.exists(self.e_tmpdir.get()):
           os.system( 'rm -r {}'.format(self.e_tmpdir.get()) )
           print("==== Directory with temporary data was removed. ===")
        self.A.quit()

    def printhelp(self):
        h="Stitches images horizontally\n"
        h+="Directory structure is, f.i., Input/000, Input/001,...Input/00N\n"
        h+="Each 000, 001, ... 00N directory must have identical subdirectory \"Type\"\n"
        h+="Selected range of images from \"Type\" directory will be stitched vertically\n"
        h+="across all subdirectories in the Input directory"
        h+="to be added as options:\n"
        h+="(1) orthogonal reslicing, (2) interpolation, (3) horizontal stitching"
        print(h)


if __name__=="__main__":
    A = tk.Tk()
    gui = GUI(A)
    A.mainloop()








