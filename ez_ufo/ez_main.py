#!/bin/python
'''
Created on Apr 5, 2018

@author: gasilos
'''

from Tkinter import *
import argparse
import glob
import os
from tofu.util import get_filenames, read_image
import warnings
warnings.filterwarnings("ignore")
import time
from shutil import rmtree

from ez_ufo.ez_ctdir_walker import WalkCTdirs
from ez_ufo.ez_tofu_cmd_gen import tofu_cmds
from ez_ufo.ez_ufo_launch_cmd_gen import ufo_cmds
from ez_ufo.ez_find_axis_cmd_gen import findCOR_cmds
from ez_ufo.util import enquote


#    '''Tested combinations
#    ** w/o RingRemoval
#    1. straight CT                             <--tested
#    2. if prepro and nothing else:             <--tested
#    3. elif prepro and inp:                    <--tested
#    4. elif prepro and inp and PR:             <--tested
#    5. if (not prepro) and inp:                <--tested
#    6. elif (not prepro) and inp and PR:       <--tested
#    7. if (not prepro) and (not inp) and PR:   <--tested
#    ** with RingRemoval
#    8. if RR and nothing else:                 <--tested both
#    9. if RR and PR and no other preprocessing <--tested
#    10. if RR and PR and inp                   <--tested
#    11. if RR and PR and inp and prepro        <--tested

def get_CTdirs_list(inpath,dirtype):
    W = WalkCTdirs(inpath,dirtype)
    W.findCTdirs()
    W.checkCTdirs()
    W.checkCTfiles()
    W.SortBadGoodSets()
    return W.ctsets, W.lvl0

def get_dims(pth):
    # get number of projections and projections dimensions
    tomos = get_filenames(pth)
    image = read_image(tomos[0])
    return len(tomos), image.shape

def clean_tmp_proj_dirs(tmpdir):
    '''Pre-creates a number of directories with projections
    in temporary directory according to number of pre-processing steps'''
    tmp_pattern =  ['proj','sino','mask','flat','dark']
    #clean temporary directory
    if os.path.exists(tmpdir):
        for filename in os.listdir(tmpdir):
            if filename[:4] in tmp_pattern:
                file_path = os.path.join(tmpdir, filename)
    #            print '{} found in tmpdir and will be removed'.format(file_path)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        rmtree(file_path)
                except Exception as e:
                    print('Failed to clean temporary directory {}. Reason: {}'.format (file_path, e))


def frmt_ufo_cmds(cmds, ctset, out_pattern, ax, args, Tofu, Ufo, FindCOR):
    '''formats list of processing commands for a CT set'''
    # determine initial number of projections and their shape
    nviews, WH = get_dims( os.path.join(ctset[0],Tofu._fdt_names[2],'*.tif') )
    tmp="Number of projections: {}, dimensions: {}". format(nviews, WH)
    cmds.append("echo \"{}\"".format(tmp))
    ############ Preprocessing commands: working on projections
    any_flat = get_filenames(os.path.join(ctset[0],Tofu._fdt_names[1]))[1]
    # make a copy of original flat-field file in case if inp is enabled
    if args.inp and args.pre:
        any_flat_copy = os.path.join(args.tmpdir,'flat.tif')
        cmds.append ("cp {} {}".format(any_flat, any_flat_copy))
        any_flat=any_flat_copy
    if args.pre:
        cmds.append("echo \" - Preprocessing \"")
        cmds_prepro = Ufo.get_pre_cmd(ctset, args.pre_cmd, args.tmpdir)
        cmds.extend(cmds_prepro)
        # reset location of input data
        ctset = (args.tmpdir, ctset[1])
    ###################################################
    if args.inp: # generate commands to "inpaint" projections
        cmds.append("echo \" - Inpainting\"")
        cmds_inpaint = Ufo.get_inp_cmd(ctset, args.tmpdir, args, WH[0], nviews, any_flat)
        # reset location of input data
        ctset = (args.tmpdir, ctset[1])
        cmds.extend(cmds_inpaint)
    ######### Projections ready #############
    ######### If RR is not enabled we do not need sinograms ########
    if (not args.RR):
        if args.inp and (not args.PR):
            cmds.append("echo \" - CT with axis {}; no ffc, no PR\"".format(ax))
            cmds.append(Tofu.get_reco_cmd(ctset, out_pattern, ax, args, nviews, WH, False, False))
        elif args.inp and args.PR:
            cmds.append("echo \" - Phase retrieval from inpainted projections\"")
            cmds.append(Ufo.get_pr_ufo_cmd(ctset, args, args.tmpdir, nviews, WH))
            cmds.append("echo \" - CT with axis {}; no ffc, no PR\"".format(ax))
            cmds.append(Tofu.get_reco_cmd(ctset, out_pattern, ax, args, nviews, WH, False, False))
        elif (not args.inp) and args.PR:
            cmds.append("echo \" - CT with axis {}; ffc and PR\"".format(ax))
            cmds.append(Tofu.get_reco_cmd(ctset, out_pattern, ax, args, nviews, WH, True, True))
        elif (not args.inp) and (not args.PR):
            cmds.append("echo \" - CT with axis {}; ffc, no PR\"".format(ax))
            cmds.append(Tofu.get_reco_cmd(ctset, out_pattern, ax, args, nviews, WH, True, False))
    ################# RING REMOVAL #######################
    if args.RR:
        # Generate sinograms
        if args.PR: # we need to do phase retrieval
            if args.inp: # if inp was requested flat field correction has been done already
                cmds.append("echo \" - Phase retrieval from inpainted projections\"")
                cmds.append(Ufo.get_pr_ufo_cmd(ctset, args, args.tmpdir, nviews, WH))
            else:
                cmds.append("echo \" - Phase retrieval with flat-correction\"")
                cmds.append(Tofu.get_pr_tofu_cmd(ctset, args, nviews, WH[0]))
            cmds.append("echo \" - Make sinograms from phase-retrieved projections\"")
            cmds.append(Tofu.get_sinos_noffc_cmd(args.tmpdir,args, nviews, WH))
        else: # we do not need to do phase retrieval
            if args.inp: # if inp was requested flat field correction has been done already
                cmds.append("echo \" - Make sinograms from inpainted projections\"")
                cmds.append(Tofu.get_sinos_noffc_cmd(args.tmpdir,args, nviews, WH))
            else:
                cmds.append("echo \" - Make sinograms with flat-correction\"")
                cmds.append(Tofu.get_sinos_ffc_cmd(ctset, args.tmpdir,args, nviews, WH))
        # Filter sinograms
        if (args.RR_par >=1) and (args.RR_par <=3):
            cmds.append("echo \" - Ring removal - ufo 1d stripes filter\"")
            cmds.append(Ufo.get_filter_sinos_cmd(ctset[0], args.tmpdir, args.RR_par, nviews, WH[1]))
        elif args.RR_par > 5:
            cmds.append("echo \" - Ring removal - median filter\"")
            #note - calling an external program, not ufo-kit script
            tmp = os.path.dirname(os.path.abspath(__file__))
            path_to_filt = os.path.join(tmp,'ez_RR_simple.py' )
            if os.path.isfile(path_to_filt):
                tmp = os.path.join(args.tmpdir, "sinos")
                cmdtmp = '{} --sinos {} --mws {}'\
                    .format(path_to_filt, tmp, args.RR_par)
                cmds.append(cmdtmp)
            else:
                cmds.append("echo \"Omitting RR because file with filter does not exist\"")
        # Preparation for final CT command
        cmds.append("echo \" - Generating proj from filtered sinograms\"")
        cmds.append(Tofu.get_sinos2proj_cmd(args, WH[0]))
        # reset location of input data
        ctset = (args.tmpdir, ctset[1])
        #Finally tofu reco without ffc and PR
        cmds.append("echo \" - CT with axis {}\"".format(ax))
        cmds.append(Tofu.get_reco_cmd(ctset, out_pattern, ax, args, nviews, WH, False, False))

def main_tk(args,fdt_names):
    # rm files in temporary directory first of all to avoid problems
    # when reconstructing ct sets with variable number of rows or projections
    if args.gray256:
        if args.hmin>=args.hmax:
            raise ValueError('hmin must be smaller than hmax to convert to 8bit without contrast inversion')
    print "**** Phase retrieval: {}; Ring removal: {}; Ufo-launch command {};"\
                .format(args.PR, args.RR, args.pre)
    #get list of all good CT directories to be reconstructed
    W, lvl0 = get_CTdirs_list(args.indir, fdt_names)
    # W is an array of tuples (path, type)
    # get list of already reconstructed sets
    recd_sets = findSlicesDirs(args.outdir)
    #generate list of commands
    cmds = []
    #initialize command generators
    FindCOR = findCOR_cmds(fdt_names)
    Tofu = tofu_cmds(fdt_names)
    Ufo = ufo_cmds(fdt_names)
    #populate list of reconstruction commands
    if not os.path.exists(args.tmpdir):
            os.makedirs(args.tmpdir)
    for i, ctset in enumerate(W):
        if not already_recd(ctset[0], lvl0, recd_sets ):
            if args.ax==1:
                ax=FindCOR.find_axis_corr(ctset,args.vcrop, args.y,args.yheight)
                print ax
            elif args.ax==2:
                ax=FindCOR.find_axis_std(ctset,args.tmpdir,\
                                args.ax_range, args.ax_p_size,args.ax_row)
            else:
                ax=args.ax_fix+i*args.dax
            setid = ctset[0][len(lvl0)+1:]
            out_pattern=os.path.join(args.outdir, setid, 'sli/sli-%04i.tif')
            cmds.append("echo \">>>>> PROCESSING {}\"".format(setid))
            clean_tmp_proj_dirs(args.tmpdir)
            frmt_ufo_cmds(cmds, ctset, out_pattern, ax, args, Tofu, Ufo, FindCOR)
            print '*********** AXIS INFO ************'
            print '{:>30}\t{}'.format('CTset','Axis')
            print '{:>30}\t{}'.format(ctset[0], ax)
        else:
            print '{} has been already reconstructed'.format(ctset[0])
    #execute commands = start reconstruction
    if not os.path.exists(args.outdir):
        os.makedirs(args.outdir)
    start = time.time()
    for cmd in cmds:
        if not args.dryrun:
            os.system(cmd)
        else:
            print cmd
    print "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    print "*** Done. Total processing time {} sec.".format(int(time.time() - start))
    print "*** Waiting for the next job..........."
    #cmnds, axes = get_ufo_cmnds(W, tmpdir, recodir, fol, axes = None, dryrun = False)

def already_recd(ctset, indir, recd_sets):
    x=False
    if ctset[len(indir)+1:] in recd_sets:
        x=True
    return x

def findSlicesDirs(lvl0):
    recd_sets = []
    for root, dirs, files in os.walk(lvl0):
        for name in dirs:
            if name == 'sli':
                recd_sets.append(root[len(lvl0)+1:])
    return recd_sets


    








