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
from ez_ufo.util import enquote
from ez_ufo.evaluate_sharpness import process as process_metrics

def fmt_in_out_path(tmpdir, indir, raw_proj_dir_name, croutdir = True):
    #suggests input and output path to directory with proj
    #depending on number of processing steps applied so far
    li = sorted(glob.glob(os.path.join(tmpdir, "proj-step*")))
    proj_dirs=[d for d in li if os.path.isdir(d)]
    Nsteps=len(proj_dirs)
    in_proj_dir, out_proj_dir = "qqq", "qqq"
    if Nsteps == 0: #no projections in temporary directory
        in_proj_dir=os.path.join(indir, raw_proj_dir_name)
        out_proj_dir="proj-step1"
    elif Nsteps>0: # there are directories proj-stepX in tmp dir
        in_proj_dir=proj_dirs[-1]
        out_proj_dir="{}{}".format(in_proj_dir[:-1],Nsteps+1)
    else:
        raise ValueError('Something is wrong with in/out filenames')
    #physically create output directory
    tmp = os.path.join(tmpdir,out_proj_dir)
    if croutdir and not os.path.exists(tmp):
        os.makedirs(tmp)
    #return names of input directory and output pattern with abs path
    return in_proj_dir, os.path.join( tmp, 'proj-%04i.tif' )

class ufo_cmds(object):
    '''
    Generates partially formatted ufo-launch and tofu commands
    Parameters are included in the string; pathnames must be added 
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

    def check_vcrop(self, cmd, vcrop, y, yheight, ystep):
        if vcrop:
            cmd += " --y {} --height {} --y-step {}"\
                    .format(y, yheight, ystep)
        return cmd

    def check_bigtif(self, cmd, swi):
        if not swi:
            cmd += " bytes-per-file=0"
        return cmd

    def get_pr_ufo_cmd(self, ctset, args, tmpdir, nviews, WH):
        in_proj_dir, out_pattern = fmt_in_out_path(args.tmpdir,args.indir,self._fdt_names[2] )
        cmds=[]
        cmd = 'ufo-launch read path={} height={} number={}'.format(in_proj_dir, WH[0], nviews)
        cmd +=' ! fft dimensions=2 ! retrieve-phase'
        cmd += ' energy={} distance={} pixel-size={} regularization-rate={:0.2f}'\
               .format(args.energy, args.z, args.pixel, args.log10db)
        cmd += ' ! ifft dimensions=2 crop-width={} crop-height={}'\
                .format(WH[1],WH[0])
        cmd += ' ! opencl kernel=\'absorptivity\' ! opencl kernel=\'fix_nan_and_inf\' !'
        cmd += ' write filename={}'.format(enquote(out_pattern))
        cmds.append(cmd)
        if not args.keep_tmp:
            cmds.append( 'rm -rf {}'.format(in_proj_dir) )
        return cmds

    def get_filter_sinos_cmd(self, ctset, tmpdir,RR, nviews, w):
        sin_in = os.path.join(tmpdir,'sinos')
        out_pattern = os.path.join(tmpdir,'sinos-filt/sin-%04i.tif')
        cmd = 'ufo-launch read path={}'.format(sin_in)
        #cmd += ' ! fft dimensions=2 ! filter-stripes sigma={}'.format(RR)
        #cmd += ' ! ifft dimensions=2 crop-width={} crop-height={}'.format(w, nviews)
        #cmd += ' ! write filename={}'.format(enquote(out_pattern))
        cmd += ' ! transpose ! fft dimensions=1 !  filter-stripes1d strength={}'.format(RR)
        cmd += ' ! ifft dimensions=1 crop-width={} ! transpose'.format(nviews)
        cmd += ' ! write filename={}'.format(enquote(out_pattern))
        return cmd

        
    def get_pre_cmd(self, ctset, pre_cmd, tmpdir, dryrun):
        indir = self.make_inpaths(ctset[0],ctset[1])
        outdir = self.make_inpaths(tmpdir,ctset[1])
        #add index to the name of th eoutput directory with projections
        #if enabled preprocessing is always the first step
        outdir[2]=os.path.join(tmpdir, "proj-step1")
        #we also must create this directory to format pathes correcly
        if not os.path.exists(outdir[2]):
            os.makedirs(outdir[2])
        cmds=[]
        for i, fol in enumerate(indir):
            in_pattern = os.path.join(fol,'*.tif')
            out_pattern = os.path.join(outdir[i],'frame-%04i.tif')
            cmds.append('ufo-launch')
            cmds[i] += ' read path={} ! '.format(enquote(in_pattern))
            cmds[i] += pre_cmd
            cmds[i] += " ! write filename={}".format(enquote(out_pattern))
        return cmds

    def get_inp_cmd(self, ctset, tmpdir, args, N, nviews, any_flat):
        indir = self.make_inpaths(ctset[0],ctset[1])
        outdir = self.make_inpaths(tmpdir,ctset[1])
        cmds=[]
        ######### CREATE MASK #########
        mask_file = os.path.join(tmpdir, "mask.tif")
        #generate mask
        cmd = 'tofu find-large-spots --images {}'.format(any_flat)
        cmd +=' --spot-threshold {} --gauss-sigma {}'.format(args.inp_thr, args.inp_sig)
        cmd += ' --output {} --output-bytes-per-file 0'.format(mask_file)
        cmds.append(cmd)
        ######### FLAT-CORRECT #########
        in_proj_dir, out_pattern = fmt_in_out_path(args.tmpdir,args.indir,self._fdt_names[2])
        cmd = 'tofu flatcorrect --fix-nan-and-inf'
        cmd += ' --darks {} --flats {}'.format(indir[0],indir[1])
        cmd += ' --projections {}'.format(in_proj_dir)
        cmd += ' --output {}'.format(out_pattern)
        if ctset[1]==4:
            cmd += ' --flats2 {}'.format(indir[3])
        if not args.PR:
            cmd += ' --absorptivity'
        cmds.append(cmd)
        if not args.keep_tmp and args.pre:
            cmds.append( 'rm -rf {}'.format(indir[0]) )
            cmds.append( 'rm -rf {}'.format(indir[1]) )
            cmds.append( 'rm -rf {}'.format(in_proj_dir) )
            if len(indir)>3:
                cmds.append( 'rm -rf {}'.format(indir[3]) )
        ######### INPAINT #########
        in_proj_dir, out_pattern = fmt_in_out_path(args.tmpdir,args.indir,self._fdt_names[2])
        cmd = 'ufo-launch [read path={} height={} number={}'.format(in_proj_dir, N, nviews)
        cmd += ', read path={}]'.format(mask_file)
        cmd +=' ! horizontal-interpolate ! '
        cmd += 'write filename={}'.format(enquote(out_pattern))
        cmds.append(cmd)
        if not args.keep_tmp:
            cmds.append( 'rm -rf {}'.format(in_proj_dir) )
        return cmds

    def get_crop_sli(self, out_pattern, args):
        cmd = 'ufo-launch read path={}/*.tif ! '.format(os.path.dirname(out_pattern))
        cmd +='crop x={} width={} y={} height={} ! '.\
                format(args.x0, args.dx, args.y0, args.dy)
        cmd +='write filename={}'.format(out_pattern)
        if args.gray256:
            cmd +=' bits=8 rescale=False'
        return cmd




    
    
    
    
    
    
    
    
        
