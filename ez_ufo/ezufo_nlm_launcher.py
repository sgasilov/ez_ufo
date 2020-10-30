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
        def __init__(self, e_indir, e_tmpdir, e_outdir, e_bigtif):
            self.args = {}
            # PATHS
            self.args['indir'] = str(e_indir.get())
            setattr(self, 'indir', self.args['indir'])

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
