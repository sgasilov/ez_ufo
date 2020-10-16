#!/usr/bin/env python2
'''
Created on Aug 3, 2018

@author: SGasilov
'''
import glob
import os
import argparse
from concert.storage import read_image, write_libtiff, write_tiff
import numpy as np
from tofu.util import get_filenames
from scipy.signal import medfilt as medf
import multiprocessing as mp
from functools import partial

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--sinos', type=str, help='Input directory')
    parser.add_argument('--mws', type=int, help='Median window size')
    return parser.parse_args()

def RR(mws, odir, fname):
    im = read_image(fname).astype(np.float32)
    N = im.shape[0]
    tmp = np.sum(im,0)/N
    tmp = medf(tmp,(mws,))
    tmp = np.array([tmp,]*N)
    im-=tmp
    filt_sin_name = os.path.join(odir, os.path.split(fname)[1])
    write_tiff( filt_sin_name, (im).astype(np.float32))

def main():
    args = parse_args()
    sinos=get_filenames(os.path.join(args.sinos, '*.tif'))
    #create output directory
    wdir = os.path.split(args.sinos)[0]
    odir = os.path.join(wdir, 'sinos-filt')
    if not os.path.exists(odir):
        os.makedirs(odir)
    pool = mp.Pool(processes=mp.cpu_count())
    exec_func = partial(RR,args.mws,odir)
    pool.map(exec_func, sinos)

if __name__ == '__main__':
    main()
