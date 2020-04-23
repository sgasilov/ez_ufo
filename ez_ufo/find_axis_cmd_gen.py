#!/bin/python
'''
Created on Apr 6, 2018

@author: gasilos
'''
import glob
import os
import argparse
import sys
import numpy as np
from concert.storage import read_image
from tofu.util import get_filenames, read_image
from ez_ufo.evaluate_sharpness import process as process_metrics
from ez_ufo.util import enquote

class findCOR_cmds(object):
    '''
    Generates commands to find the axis of rotation
    '''
    def __init__(self, fol):
        self._fdt_names = fol

    def make_inpaths(self,lvl0, flats2):
        indir = []
        for i in self._fdt_names[:3]:
            indir.append( os.path.join(lvl0, i) )
        if flats2-3:
            indir.append( os.path.join(lvl0, self._fdt_names[3]) )
        return indir

    def find_axis_std(self, ctset, tmpdir,ax_range, p_width,search_row):
        indir = self.make_inpaths(ctset[0], ctset[1])
        print indir[2]
        image = read_image(get_filenames(indir[2])[0])
        cmd =  'tofu lamino --absorptivity --fix-nan-and-inf --overall-angle 180'\
               ' --lamino-angle 90 --height 2'
        cmd += ' --darks {} --flats {} --projections {}'.\
                    format(indir[0], indir[1], enquote(indir[2]))
        if ctset[1]==4:
            cmd += ' --flats2 {}'.format(indir[3])
        out_pattern = os.path.join(tmpdir,"axis-search/slice")
        cmd += ' --output {}'.format(enquote(out_pattern))
        cmd += ' --x-region={},{},{}'.format(-p_width / 2, p_width / 2, 1)
        cmd += ' --y-region={},{},{}'.format(-p_width / 2, p_width / 2, 1)
        cmd += ' --y {} --height 2'.format(search_row)
        cmd += ' --z-parameter x-center'
        cmd += ' --region={}'.format(enquote(ax_range))
        cmd += ' --z 0'
        res = [float(num) for num in ax_range.split(',')]
        cmd += ' --axis {},{}'.format( (res[0]+res[1])/2., 1.0) #middle of ax search range?
        cmd += " --output-bytes-per-file 0"
        # cmd += ' --delete-slice-dir'
        print cmd
        os.system(cmd)
        points, maximum = evaluate_images_simp(out_pattern + '*.tif', "msag")
        return res[0] + res[2] * maximum
        

    def find_axis_corr(self, ctset, vcrop, y, height):
        indir = self.make_inpaths(ctset[0], ctset[1])
        """Use correlation to estimate center of rotation for tomography."""
        from scipy.signal import fftconvolve
        def flat_correct(flat, radio):
            nonzero = np.where(radio != 0)
            result = np.zeros_like(radio)
            result[nonzero] = flat[nonzero] / radio[nonzero]
            # log(1) = 0
            result[result <= 0] = 1

            return np.log(result)

        first = read_image(get_filenames(indir[2])[0]).astype(np.float)
        last = read_image(get_filenames(indir[2])[-1]).astype(np.float)

        dark = read_image(get_filenames(indir[0])[0]).astype(np.float)
        flat1 = read_image(get_filenames(indir[1])[-1]) - dark
        first = flat_correct(flat1, first - dark)
        if ctset[1]==4:
            flat2 = read_image(get_filenames(indir[3])[-1]) - dark
            last = flat_correct(flat2, last - dark)
        else:
            last = flat_correct(flat1, last - dark)

        if vcrop:
            y_region = slice(y, min(y + height, first.shape[0]), 1)
            first = first[y_region, :]
            last = last[y_region, :]

        width = first.shape[1]
        first = first - first.mean()
        last = last - last.mean()

        conv = fftconvolve(first, last[::-1, :], mode='same')
        center = np.unravel_index(conv.argmax(), conv.shape)[1]

        return (width / 2.0 + center) / 2.0


def evaluate_images_simp(input_pattern, metric, num_images_for_stats=0, out_prefix=None, fwhm=None,
                blur_fwhm=None, verbose=False):
    #simplified version of original evaluate_images function
    #from Tomas's optimize_parameters script
    names = sorted(glob.glob(input_pattern))
    res = process_metrics(names, num_images_for_stats=num_images_for_stats,
                          metric_names=(metric,), out_prefix=out_prefix,
                          fwhm=fwhm, blur_fwhm=blur_fwhm)[metric]
    return res, np.argmax(res)



    
    
    
    
    
    
    
    
        
