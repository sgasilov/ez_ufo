#!/usr/bin/env python2
'''
Created on Feb 5, 2019

@author: gasilos
'''

import Tkinter as tk
import tkFileDialog as filedialog
import numpy as np
import os
from ezufo_helpers.mview_main import main_prep

E=tk.E; W=tk.W

class GUI:
    def __init__(self, A):
        self.A = A
        self.args={}
        A.title("Convert CT file sequence to flats/darks/tomo directories")
        r=0;

        #Select directory
        self.indir = os.getcwd()
        self.indir_b = tk.Button(A,\
            text="Select directory with a CT sequence", \
            command=self.select_indir)
        self.indir_b.grid(row=r, column=0, columnspan=2)
        r+=1

        v = tk.StringVar(A, value=self.indir)
        self.e_indir = tk.Entry(A,textvariable=v, width=70)
        self.e_indir.grid(row=r, column=0, columnspan=2, sticky=E)
        r+=1

        #other parameters
        tk.Label(A, text="Number of projections").grid(row=r);
        v = tk.IntVar(A, value=3000)
        self.e_nproj = tk.Entry(A,textvariable=v);
        self.e_nproj.grid(row=r, column=1, sticky=E); r+=1

        tk.Label(A, text="Number of flats").grid(row=r);
        v = tk.IntVar(A, value=10)
        self.e_nflats = tk.Entry(A,textvariable=v);
        self.e_nflats.grid(row=r, column=1, sticky=E); r+=1

        tk.Label(A, text="Number of darks").grid(row=r);
        v = tk.IntVar(A, value=10)
        self.e_ndarks = tk.Entry(A,textvariable=v);
        self.e_ndarks.grid(row=r, column=1, sticky=E); r+=1

        tk.Label(A, text="Number of vertical steps").grid(row=r);
        v = tk.IntVar(A, value=1)
        self.e_nviews = tk.Entry(A,textvariable=v);
        self.e_nviews.grid(row=r, column=1, sticky=E); r+=1

        f2=tk.Frame(A)
        f2.grid(row=r, column = 0, columnspan = 2)
        r+=1

        tmp="No trailing flats/darks"
        self.e_noflats2 = tk.BooleanVar(A, value=False)
        #tk.Checkbutton(A, text=tmp, variable=self.e_noflats2)\
        #                .grid(row=r, column=0,sticky=E);
        o1 = tk.Checkbutton(f2, text=tmp, variable=self.e_noflats2)
        o1.pack(side="left")

        tmp="File names without zero padding"
        self.e_Andor = tk.BooleanVar(A, value=False)
        #tk.Checkbutton(A, text=tmp, variable=self.e_Andor)\
        #                .grid(row=r, column=0,sticky=E); r+=1
        o2 = tk.Checkbutton(f2, text=tmp, variable=self.e_Andor)
        o2.pack(side="left")

        #launch buttons
        f1 = tk.Frame(A)
        b1 = tk.Button(f1, text='Convert', command=self.convert)
        b2 = tk.Button(f1, text='Undo', command=self.undo)
        b3 = tk.Button(f1, text='Help', command=self.printhelp)
        b4 = tk.Button(f1, text='Quit', command=self.A.quit)
        f1.grid(row=r, column = 0, columnspan = 2)
        b1.pack(side="left")
        b2.pack(side="left")
        b3.pack(side="left")
        b4.pack(side="left")


    def select_indir(self):
        cwd = os.getcwd()
        tmp = "Select directory with MView sequence"
        self.indir = filedialog.askdirectory(\
                  initialdir = cwd, title = tmp)
        self.e_indir.delete(0, tk.END)
        self.e_indir.insert(0, self.indir)

    def convert(self):
        self.args['input']=str(self.e_indir.get())
        setattr(self,'input',self.args['input'])
        self.args['output']=str(self.e_indir.get())
        setattr(self,'output',self.args['output'])
        self.args['nproj']=int(self.e_nproj.get())
        setattr(self,'nproj',self.args['nproj'])
        self.args['nflats']=int(self.e_nflats.get())
        setattr(self,'nflats',self.args['nflats'])
        self.args['ndarks']=int(self.e_ndarks.get())
        setattr(self,'ndarks',self.args['ndarks'])
        self.args['nviews']=int(self.e_nviews.get())
        setattr(self,'nviews',self.args['nviews'])
        self.args['noflats2']=bool(int(self.e_noflats2.get()))
        setattr(self,'noflats2',self.args['noflats2'])
        self.args['Andor']=bool(int(self.e_Andor.get()))
        setattr(self,'Andor',self.args['Andor'])

        main_prep(self)

    def undo(self):
        cmd = "find {} -type f -name \"*.tif\" -exec mv -t {} {{}} +"
        cmd = cmd.format( str(self.e_indir.get()), str(self.e_indir.get()) )
        os.system(cmd)

    def printhelp(self):
        h="Distributes a sequence of CT frames in flats/darks/tomo/flats2 directories\n"
        h="assuming that acqusition sequence is flats->darks->tomo->flats2\n"
        h+='Use only for sequences with flat fields acquired at 0 and 180!\n'
        h+="Conversions happens in-place but can be undone"
        print (h)

if __name__=="__main__":
    A = tk.Tk()
    gui = GUI(A)
    A.mainloop()








