#!/usr/bin/env python2
'''
Created on Nov 5, 2020

@author: sergei gasilov
'''

import Tkinter as tk
import tkMessageBox
from tkFont import Font
from ez_ufo.main_nlm import main_tk
import tkFileDialog as filedialog
import os
from shutil import rmtree
import getpass

E=tk.E; W=tk.W

class tk_args():
    def __init__(self, e_indir, e_input_is_file,
                 e_outdir, e_bigtif,
                 e_r, e_dx, e_h, e_sig,
                 e_w, e_fast, e_autosig,
                  e_dryrun):
        self.args = {}
        # PATHS
        self.args['indir'] = str(e_indir.get())
        setattr(self, 'indir', self.args['indir'])
        self.args['input_is_file'] = e_input_is_file
        setattr(self, 'input_is_file', self.args['input_is_file'])
        self.args['outdir'] = str(e_outdir.get())
        setattr(self, 'outdir', self.args['outdir'])
        # ALG PARAMS - MAIN
        self.args['search_r'] = int(e_r.get())
        setattr(self, 'search_r', self.args['search_r'])
        self.args['patch_r'] = int(e_dx.get())
        setattr(self, 'patch_r', self.args['patch_r'])
        self.args['h'] = float(e_h.get())
        setattr(self, 'h', self.args['h'])
        self.args['sig'] = float(e_sig.get())
        setattr(self, 'sig', self.args['sig'])
        # ALG PARAMS - optional
        self.args['w'] = float(e_w.get())
        setattr(self, 'w', self.args['w'])
        self.args['fast'] = bool(e_fast.get())
        setattr(self, 'fast', self.args['fast'])
        self.args['autosig'] = bool(e_autosig.get())
        setattr(self, 'autosig', self.args['autosig'])
        # Misc
        # self.args['inplace'] = bool(e_inplace.get())
        # setattr(self, 'inplace', self.args['inplace'])
        self.args['bigtif'] = bool(e_bigtif.get())
        setattr(self, 'bigtif', self.args['bigtif'])
        self.args['dryrun']=bool(e_dryrun.get())
        setattr(self,'dryrun',self.args['dryrun'])



class GUI:
    def __init__(self, A):
        self.A = A
        bold_font = Font(weight="bold")
        A.title("E&Z nlm denoising with ufo-kit")
        r=0;

        ################### PATHS BLOCK ########################
        self.e_input_is_file = False
        #Select input directory
        f0 = tk.Frame(A)
        self.indir = os.path.abspath(os.getcwd())
        b0_1 = tk.Button(f0,\
            text="Select input directory", \
            font=bold_font, command=self.select_indir)
        b0_1file = tk.Button(f0, \
                         text="Select one image", \
                         font=bold_font, command=self.select_image)
        #Save in separate files of in one huge tiff file
        # self.e_inplace = tk.BooleanVar(A, value=False)
        # tmp="Filter in-place"
        # b0_2 = tk.Checkbutton(f0, text=tmp, variable=self.e_inplace)
        f0.grid(row=r, column=0, columnspan=2)
        b0_1.pack(side="left")
        b0_1file.pack(side="left")
        # b0_2.pack(side="right")
        r+=1
        v = tk.StringVar(A, value=self.indir)
        self.e_indir = tk.Entry(A,textvariable=v, width=70)
        self.e_indir.grid(row=r, column=0, columnspan=2, sticky=E)
        r+=1


        #Select output directory
        f0 = tk.Frame(A)
        self.outdir = os.path.abspath(os.getcwd() + '-nlmfilt')
        b0_1 = tk.Button(f0,\
            text="Select output directory or filename pattern", \
            font=bold_font, command=self.select_outdir)
        #Save in separate files of in one huge tiff file
        self.e_bigtif = tk.BooleanVar(A, value=False)
        tmp="Save in bigtiff container"
        b0_2 = tk.Checkbutton(f0, text=tmp, variable=self.e_bigtif)
        f0.grid(row=r, column=0, columnspan=2)
        b0_1.pack(side="left")
        b0_2.pack(side="right")
        r+=1

        v = tk.StringVar(A, value=self.outdir)
        self.e_outdir = tk.Entry(A,textvariable=v, width=70)
        self.e_outdir.grid(row=r, column=0, columnspan=2, sticky=E)
        r+=1

        self.lab = tk.Label(A, text="Radius for similarity search", fg="darkgreen")
        self.lab.grid(row=r, column=0, sticky=W);
        v = tk.IntVar(A, value=10)
        self.e_r = tk.Entry(A,textvariable=v);
        self.e_r.grid(row=r, column=1, sticky=E);
        r+=1

        self.lab = tk.Label(A, text="Radius of patches", fg="darkgreen")
        self.lab.grid(row=r, column=0, sticky=W);
        v = tk.IntVar(A, value=3)
        self.e_dx = tk.Entry(A,textvariable=v);
        self.e_dx.grid(row=r, column=1, sticky=E);
        r+=1

        self.lab = tk.Label(A, text="Smoothing control parameter", fg="darkgreen")
        self.lab.grid(row=r, column=0, sticky=W);
        v = tk.DoubleVar(A, value=0.0)
        self.e_h = tk.Entry(A,textvariable=v);
        self.e_h.grid(row=r, column=1, sticky=E);
        r+=1


        self.lab = tk.Label(A, text="Noise standard deviation", fg="darkgreen")
        self.lab.grid(row=r, column=0, sticky=W);
        v = tk.DoubleVar(A, value=0.0)
        self.e_sig = tk.Entry(A,textvariable=v);
        self.e_sig.grid(row=r, column=1, sticky=E);
        r+=1

        self.lab = tk.Label(A, text="Window (optional)")
        self.lab.grid(row=r, column=0, sticky=W)
        v = tk.DoubleVar(A, value=0.0)
        self.e_w = tk.Entry(A,textvariable=v)
        self.e_w.grid(row=r, column=1, sticky=E)
        r+=1

        f11 = tk.Frame(A)
        self.e_fast = tk.BooleanVar(A, value=True)
        opsw1 = tk.Checkbutton(f11, text="Fast", variable=self.e_fast)

        self.e_autosig = tk.BooleanVar(A,  value=False)
        opsw2 = tk.Checkbutton(f11, text="Estimate sigma", variable=self.e_autosig)

        f11.grid(row=r, column=0, columnspan=2)
        opsw1.pack(side="left")
        opsw2.pack(side="left")
        r+=1

        ############### EXECUTION BUTTONS ###################
        f1 = tk.Frame(A)
        b1 = tk.Button(f1, text='Quit', font=bold_font, command=self.quit)
        b2 = tk.Button(f1, text='Help', command=self.printhelp)
        b3 = tk.Button(f1, text='Delete reco dir', \
                       command=self.rm_rec_dir)
        self.e_dryrun = tk.BooleanVar(A, value=False)
        b4 = tk.Button(f1, text='Dry run', \
                       command=self.dry_run)

        f1.grid(row=r, column=0)
        b1.pack(side="left")
        b2.pack(side="left")
        b3.pack(side="left")
        b4.pack(side="left")

        b5 = tk.Button(A, text='Apply filter', font=bold_font, fg="red3", \
                       command=self.reco)
        b5.grid(row=r, column=1)

    def quit(self):
        self.A.quit()

    def select_indir(self):
        cwd = self.e_indir.get()
        if cwd=='':
            cwd = os.getcwd()
        tmp = "Select input directory"
        self.indir = filedialog.askdirectory(\
                  initialdir = cwd, title = tmp)
        self.e_indir.delete(0, tk.END)
        self.e_indir.insert(0, self.indir)
        self.e_outdir.delete(0, tk.END)
        self.e_outdir.insert(0, self.indir+'-nlmfilt')
        self.e_input_is_file = False

    def select_image(self):
        cwd = self.e_indir.get()
        if cwd=='':
            cwd = os.getcwd()
        tmp = "Select image (tif files only)"
        self.indir = filedialog.askopenfilename(initialdir=cwd, title=tmp,
                  filetypes=(("Image files", "*.tif"), ("Image files", "*.tiff")))
        self.e_indir.delete(0, tk.END)
        self.e_indir.insert(0, self.indir)
        try:
            imname, imext = os.path.splitext(self.indir)
            tmp = imname+'-nlmfilt-%05i'+imext
            self.e_outdir.delete(0, tk.END)
            self.e_outdir.insert(0, tmp)
        except:
            pass
        self.e_input_is_file = True

    def select_outdir(self):
        tmp = "Select output directory"
        cwd = self.e_outdir.get()
        if cwd=='':
            cwd = os.getcwd()
        self.outdir = filedialog.askdirectory(\
                  initialdir = cwd, title = tmp)
        self.e_outdir.delete(0, tk.END)
        self.e_outdir.insert(0, self.outdir)

    def reco(self):
        args=tk_args(self.e_indir, self.e_input_is_file,\
                    self.e_outdir,self.e_bigtif,\
                    self.e_r, self.e_dx, self.e_h, self.e_sig,\
                    self.e_w, self.e_fast, self.e_autosig, \
                    self.e_dryrun)
        if os.path.exists(args.outdir) and not self.e_dryrun.get():
            titletext = "Warning: files can be overwritten"
            text1 = "Output directory exists. Files can be overwritten. Proceed?"
            dd = tkMessageBox.askyesno(titletext, text1)
            if dd:
                main_tk(args)
                tkMessageBox.showinfo("Done", "Done")
        else:
            main_tk(args)
            tkMessageBox.showinfo("Done", "Done")

    def rm_rec_dir(self):
        titletext = "Warning: data can be lost"
        text1 = "Delete output directory?"
        text2 = "Cannot delete: output directory is the same as input"
        dd = tkMessageBox.askyesno(titletext,text1)
        if dd and os.path.exists(self.e_outdir.get()):
            if self.e_outdir.get() == self.e_indir.get():
                tkMessageBox.showinfo("Warning", text2)
            else:
                os.system('rm -rf {}'.format(self.e_outdir.get()))
                print ("Output directory was removed")

    def dry_run(self):
        self.e_dryrun = tk.BooleanVar(self.A, value=True)
        self.reco()
        self.e_dryrun = tk.BooleanVar(self.A, value=False)

    def printhelp(self):
      h=""
      h+="Note4: set to \"flats\" if \"flats2\" exist but you need to ignore them; \n"
      h+="SerG, BMIT CLS, Dec. 2020."
      print(h)

if __name__=="__main__":
    A = tk.Tk()
    ez_ufo_gui = GUI(A)
    A.mainloop()
