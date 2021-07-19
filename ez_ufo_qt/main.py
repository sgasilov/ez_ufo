'''
Created on Apr 5, 2018
@author: sergei gasilov
'''

import argparse
import glob
import os
from tofu.util import get_filenames, read_image
import warnings
import math

warnings.filterwarnings("ignore")
import time
#from shutil import rmtree

from ez_ufo_qt.ctdir_walker import WalkCTdirs
from ez_ufo_qt.tofu_cmd_gen import tofu_cmds
from ez_ufo_qt.ufo_cmd_gen import ufo_cmds
from ez_ufo_qt.find_axis_cmd_gen import findCOR_cmds
from ez_ufo_qt.util import *
#from tofu.util import get_filenames


def get_CTdirs_list(inpath, dirtype):
    W = WalkCTdirs(inpath, dirtype)
    W.findCTdirs()
    W.checkCTdirs()
    W.checkCTfiles()
    W.SortBadGoodSets()
    return W.ctsets, W.lvl0


def frmt_ufo_cmds(cmds, ctset, out_pattern, ax, args, Tofu, Ufo, FindCOR, nviews, WH):
    '''formats list of processing commands for a CT set'''
    # two helper variables to mark that PR/FFC has been done at some step
    swiFFC = True  # FFC is always required required
    swiPR = args.PR  # PR is an optional operation

    ####### PREPROCESSING #########
    flat_file_for_mask = os.path.join(args.tmpdir, 'flat.tif')
    if args.inp:
        flatdir = os.path.join(ctset[0], Tofu._fdt_names[1])
        cmd = make_copy_of_flat(flatdir, flat_file_for_mask, args.dryrun)
        cmds.append(cmd)
    if args.pre:
        cmds.append("echo \" - Applying filter(s) to images \"")
        cmds_prepro = Ufo.get_pre_cmd(ctset, args.pre_cmd, args.tmpdir, args.dryrun)
        cmds.extend(cmds_prepro)
        # reset location of input data
        ctset = (args.tmpdir, ctset[1])
    ###################################################
    if args.inp:  # generate commands to remove sci. spots from projections
        cmds.append("echo \" - Flat-correcting and removing large spots\"")
        cmds_inpaint = Ufo.get_inp_cmd(ctset, args.tmpdir, args, WH[0], nviews, flat_file_for_mask)
        # reset location of input data
        ctset = (args.tmpdir, ctset[1])
        cmds.extend(cmds_inpaint)
        swiFFC = False  # no need to do FFC anymore

    ######## PHASE-RETRIEVAL #######
    # Do PR separately if sinograms must be generate or if vertical ROI is defined
    if (args.PR and args.RR):  # or (args.PR and args.vcrop): #Phase Retrieval and Ring Removal
        if swiFFC:  # we still need need flat correction #Inpaint No
            cmds.append("echo \" - Phase retrieval with flat-correction\"")
            if args.sinFFC:
                cmds.append(Tofu.get_sinFFC_cmd(ctset, args, nviews, WH[0]))
            cmds.append(Tofu.get_pr_tofu_cmd(ctset, args, nviews, WH))
        else: #Inpaint Yes
            cmds.append("echo \" - Phase retrieval from flat-corrected projections\"")
            cmds.extend(Ufo.get_pr_ufo_cmd(args, nviews, WH))
        swiPR = False  # no need to do PR anymore
        swiFFC = False  # no need to do FFC anymore

    # if args.PR and args.vcrop: # have to reset location of input data
    #    ctset = (args.tmpdir, ctset[1])

    ################# RING REMOVAL #######################
    if args.RR:
        # Generate sinograms first
        if swiFFC:  # we still need to do flat-field correction
            if args.sinFFC:
                # Create flat corrected images using sinFFC
                cmds.append(Tofu.get_sinFFC_cmd(ctset, args, nviews, WH[0]))
                # Feed the flat corrected images to sinogram generation
                cmds.append(Tofu.get_sinos_noffc_cmd(ctset[0], args.tmpdir, args, nviews, WH))
            elif not args.sinFFC:
                cmds.append("echo \" - Make sinograms with flat-correction\"")
                cmds.append(Tofu.get_sinos_ffc_cmd(ctset, args.tmpdir, args, nviews, WH))
        else:  # we do not need flat-field correction
            cmds.append("echo \" - Make sinograms without flat-correction\"")
            cmds.append(Tofu.get_sinos_noffc_cmd(ctset[0], args.tmpdir, args, nviews, WH))
        swiFFC = False
        # Filter sinograms
        if args.RR_ufo:
            if args.RR_ufo_1d:
                cmds.append("echo \" - Ring removal - ufo 1d stripes filter\"")
                cmds.append(Ufo.get_filter1d_sinos_cmd(args.tmpdir, args.RR_par, nviews))
            else:
                cmds.append("echo \" - Ring removal - ufo 2d stripes filter\"")
                cmds.append(Ufo.get_filter2d_sinos_cmd(args.tmpdir, args.RR_par, nviews, WH[1]))
        else:
            cmds.append("echo \" - Ring removal - sarepy filter(s)\"")
            # note - calling an external program, not an ufo-kit script
            tmp = os.path.dirname(os.path.abspath(__file__))
            path_to_filt = os.path.join(tmp, 'RR_simple.py')
            if os.path.isfile(path_to_filt):
                tmp = os.path.join(args.tmpdir, "sinos")
                cmdtmp = 'python {} --sinos {} --mws {} --mws2 {} --snr {} --sort_only {}' \
                    .format(path_to_filt, tmp, args.RR_srp_wind_sort,
                            args.RR_srp_wide_wind, args.RR_srp_wide_snr, int(not args.RR_srp_wide))
                cmds.append(cmdtmp)
            else:
                cmds.append("echo \"Omitting RR because file with filter does not exist\"")
        if not args.keep_tmp:
            cmds.append('rm -rf {}'.format(os.path.join(args.tmpdir, 'sinos')))
        # Convert filtered sinograms back to projections
        cmds.append("echo \" - Generating proj from filtered sinograms\"")
        cmds.append(Tofu.get_sinos2proj_cmd(args, WH[0]))
        # reset location of input data
        ctset = (args.tmpdir, ctset[1])

    # Finally - call to tofu reco
    cmds.append("echo \" - CT with axis {}; ffc:{}, PR:{}\"".format(ax, swiFFC, swiPR))
    cmds.append(Tofu.get_reco_cmd(ctset, out_pattern, ax, args, nviews, WH, swiFFC, swiPR))

    return nviews, WH


def main_tk(args, fdt_names):
    # array with the list of commands
    cmds = []
    # clean temporary directory or create if it doesn't exist
    if not os.path.exists(args.tmpdir):
        os.makedirs(args.tmpdir)
    # else:
    #    clean_tmp_dirs(args.tmpdir, fdt_names)
    # input params consistency check
    if args.gray256:
        if args.hmin > args.hmax:
            raise ValueError('hmin must be smaller than hmax to convert to 8bit without contrast inversion')
    '''
    if args.gray256:
        if args.hmin >= args.hmax:
            raise ValueError('hmin must be smaller than hmax to convert to 8bit without contrast inversion')
    '''
    # get list of all good CT directories to be reconstructed
    print('*********** Analyzing input directory ************')
    W, lvl0 = get_CTdirs_list(args.indir, fdt_names)
    # W is an array of tuples (path, type)
    # get list of already reconstructed sets
    recd_sets = findSlicesDirs(args.outdir)
    # initialize command generators
    FindCOR = findCOR_cmds(fdt_names)
    Tofu = tofu_cmds(fdt_names)
    Ufo = ufo_cmds(fdt_names)
    # populate list of reconstruction commands
    print('*********** AXIS INFO ************')
    for i, ctset in enumerate(W):
        if not already_recd(ctset[0], lvl0, recd_sets):
            # determine initial number of projections and their shape
            path2proj = os.path.join(ctset[0], Tofu._fdt_names[2])
            nviews, WH, multipage = get_dims(path2proj)
            # e_axis_bypass is OFF then find centre of rotation
            if not args.e_axis_bypass:
                if args.vcrop and bad_vert_ROI(multipage, path2proj, args.y, args.yheight):
                    print('{:>30}\t{}'.format('CTset', 'Axis'))
                    print('{:>30}\t{}'.format(ctset[0], 'na'))
                    print('Vertical ROI does not contain any rows.')
                    print("Number of projections: {}, dimensions: {}".format(nviews, WH))
                    continue
                if args.ax == 1:
                    ax = FindCOR.find_axis_corr(ctset, args.vcrop, args.y, args.yheight, multipage)
                elif args.ax == 2:
                    cmds.append("echo \"Cleaning axis-search in tmp directory\"")
                    os.system('rm -rf {}'.format(os.path.join(args.tmpdir, 'axis-search')))
                    ax = FindCOR.find_axis_std(ctset, args.tmpdir, \
                                               args.ax_range, args.ax_p_size, args.ax_row, nviews)
                else:
                    ax = args.ax_fix + i * args.dax
            # e_axis_bypass is ON then image midpoint forms axis of rotation
            elif args.e_axis_bypass:
                ax = FindCOR.find_axis_image_midpoint(ctset, multipage, WH)
                print("Bypassing axis search and using image midpoint: {}".format(ax))

            setid = ctset[0][len(lvl0) + 1:]
            out_pattern = os.path.join(args.outdir, setid, 'sli/sli')
            cmds.append("echo \">>>>> PROCESSING {}\"".format(setid))
            # rm files in temporary directory first of all to
            # format paths correctly and to avoid problems
            # when reconstructing ct sets with variable number of rows or projections
            cmds.append("echo \"Cleaning temporary directory\"".format(setid))
            clean_tmp_dirs(args.tmpdir, fdt_names)
            # call function which formats commands for this data set
            nviews, WH = frmt_ufo_cmds(cmds, ctset, out_pattern, \
                                       ax, args, Tofu, Ufo, FindCOR, nviews, WH)
            save_params(args, setid, ax, nviews, WH)
            print('{:>30}\t{}'.format('CTset', 'Axis'))
            print('{:>30}\t{}'.format(ctset[0], ax))
            print("Number of projections: {}, dimensions: {}".format(nviews, WH))
            # tmp = "Number of projections: {}, dimensions: {}".format(nviews, WH)
            # cmds.append("echo \"{}\"".format(tmp))
        else:
            print('{} has been already reconstructed'.format(ctset[0]))
    # execute commands = start reconstruction
    start = time.time()
    print('*********** PROCESSING ************')
    for cmd in cmds:
        if not args.dryrun:
            os.system(cmd)
        else:
            print(cmd)
    print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    print("*** Done. Total processing time {} sec.".format(int(time.time() - start)))
    print("*** Waiting for the next job...........")
    # cmnds, axes = get_ufo_cmnds(W, tmpdir, recodir, fol, axes = None, dryrun = False)


def already_recd(ctset, indir, recd_sets):
    x = False
    if ctset[len(indir) + 1:] in recd_sets:
        x = True
    return x


def findSlicesDirs(lvl0):
    recd_sets = []
    for root, dirs, files in os.walk(lvl0):
        for name in dirs:
            if name == 'sli':
                recd_sets.append(root[len(lvl0) + 1:])
    return recd_sets