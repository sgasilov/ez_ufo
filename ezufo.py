#!/usr/bin/env python2
import Tkinter as tk
from ez_ufo import ez_ufo_launcher

A = tk.Tk()
ez_ufo_gui = ez_ufo_launcher.GUI(A)
A.mainloop()
