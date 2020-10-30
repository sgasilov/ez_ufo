#!/usr/bin/env python2
'''
Created on Apr 5, 2018

@author: gasilos
'''

import Tkinter as tk
import tkMessageBox
from tkFont import Font
from ez_ufo.nlm_gui import main_tk
import tkFileDialog as filedialog
import os
from shutil import rmtree
import getpass

E=tk.E; W=tk.W

class tk_args():
    class tk_args():
        def __init__(self, e_indir, e_outdir,
                     e_r, e_dx, e_h, e_sig,
                     e_w, e_fast, e_autosig):
            self.args = {}
            # PATHS
            self.args['indir'] = str(e_indir.get())
            setattr(self, 'indir', self.args['indir'])
            self.args['outdir'] = str(e_outdir.get())
            setattr(self, 'outdir', self.args['outdir'])
            # ALG PARAMS
            self.args['search-r'] = int(e_r.get())
            setattr(self, 'search-r', self.args['search-r'])
            self.args['patch-r'] = int(e_dx.get())
            setattr(self, 'patch-r', self.args['patch-r'])
            self.args['h'] = float(e_h.get())
            setattr(self, 'h', self.args['h'])
            self.args['sig'] = float(e_sig.get())
            setattr(self, 'sig', self.args['sig'])
            self.args['w'] = float(e_w.get())
            setattr(self, 'w', self.args['w'])

            #"fast": boolean
            #"estimate-sigma": boolean



class GUI:
    def __init__(self, A):
        self.A = A
        bold_font = Font(weight="bold")
        A.title("E&Z ufo-kit")
        r=0;

if __name__=="__main__":
    A = tk.Tk()
    ez_ufo_gui = GUI(A)
    A.mainloop()
