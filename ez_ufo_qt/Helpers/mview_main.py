#!/bin/python
import glob
import os
import argparse
import sys
import numpy
from tofu.util import get_filenames
import shutil
import re


def check_folders(p, noflats2):
    if not os.path.exists(p):
        os.makedirs(p)
    tmp = p + '/darks'
    if not os.path.exists(tmp):
        os.makedirs(tmp)
    tmp = p + '/flats'
    if not os.path.exists(tmp):
        os.makedirs(tmp)
    if noflats2 == False:
        tmp = p + '/flats2'
        if not os.path.exists(tmp):
            os.makedirs(tmp)
    tmp = p + '/tomo'
    if not os.path.exists(tmp):
        os.makedirs(tmp)


def rename_Andor(parameters):
    names = get_filenames(os.path.join(parameters['ezmview_input_dir'], '*.tif'))
    maxnum = re.match('.*?([0-9]+)$', names[0][:-4]).group(1)
    n_dgts = len(maxnum)
    trnc_len = n_dgts + 4
    prefix = names[0][:-trnc_len]
    maxnum = int(maxnum)
    for name in names:
        num = int(re.match('.*?([0-9]+)$', name[:-4]).group(1))
        maxnum = num if (num > maxnum) else maxnum
    n_dgts = len(str(maxnum))
    lin_fmt = prefix + '{:0' + str(n_dgts) + '}.tif'
    for name in names:
        num = re.match('.*?([0-9]+)$', name[:-4]).group(1)
        if name == lin_fmt.format(int(num)):
            continue
        else:
            cmd = "mv {} {}".format(name, lin_fmt.format(int(num)))
            os.system(cmd)


def main_prep(parameters):
    if parameters['ezmview_zero_padding']:
        rename_Andor(parameters)
    frames = get_filenames(os.path.join(parameters['ezmview_input_dir'], '*.tif'))

    nframes = len(frames)
    if nframes == 0:
        tmp = 'Check INPUT directory: there are no tif files there'
        raise ValueError(tmp)

    # replace first frame with the second to get rid of
    # corrupted first file in the PCO Edge sequencies
    cmd = "rm {}; cp {} {}".format(frames[0], frames[1], frames[0])
    os.system(cmd)

    FFinterval = parameters['ezmview_num_projections']
    int_tot = parameters['ezmview_num_vertical_steps']  # (args.nproj/FFinterval)*args.nviews
    int_1view = 1.0  # args.nproj/FFinterval

    files_in_int = parameters['ezmview_num_flats'] + parameters['ezmview_num_darks'] + FFinterval
    files_input = (parameters['ezmview_num_flats'] + parameters['ezmview_num_darks'] + FFinterval) * int_tot
    if not parameters['ezmview_flats2']:
        files_input += parameters['ezmview_num_flats'] + parameters['ezmview_num_darks']

    if files_input != nframes:
        tmp = 'Sequence length (found {} files) does not match '.format(nframes) + \
              'one calculated from input parameters ' + \
              '(expected {} files)'.format(files_input)
        raise ValueError(tmp)

    print("=> Begin Processing Files")

    for i in range(parameters['ezmview_num_vertical_steps']):
        if parameters['ezmview_num_vertical_steps'] > 1:
            pout = os.path.join(parameters['ezmview_input_dir'], 'z{:02d}'.format(i))
        else:
            pout = parameters['ezmview_input_dir']
        check_folders(pout, parameters['ezmview_flats2'])
        # offset to heading flats and darks
        o = i * files_in_int
        for j in range(parameters['ezmview_num_flats']):
            cmd = "mv {} {}/flats/".format(frames[o + j], pout)
            os.system(cmd)
            # print(cmd)
        o += parameters['ezmview_num_flats']
        for j in range(parameters['ezmview_num_darks']):
            cmd = "mv {} {}/darks/".format(frames[o + j], pout)
            os.system(cmd)
            # print(cmd)
        o += parameters['ezmview_num_darks']
        for j in range(parameters['ezmview_num_projections']):
            cmd = "mv {} {}/tomo/".format(frames[o + j], pout)
            os.system(cmd)
            # print(cmd)
        o += parameters['ezmview_num_projections']
        if parameters['ezmview_flats2']:
            continue
        for j in range(parameters['ezmview_num_flats']):
            cmd = "cp {} {}/flats2/".format(frames[o + i], pout)
            os.system(cmd)
            # print(cmd)

    print("========== Done ==========")
