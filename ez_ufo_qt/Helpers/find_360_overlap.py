'''
This script takes as input a CT scan that has been collected in "half-acquisition" mode
and produces a series of reconstructed slices, each of which are generated by cropping and
concatenating opposing projections together over a range of "overlap" values (i.e. the pixel column
at which the images are cropped and concatenated).
The objective is to review this series of images to determine the pixel column at which the axis of rotation
is located (much like the axis search function commonly used in reconstruction software).
Created by Toby Bond. Modified by Iain Emslie
'''

import os
import shutil
import numpy as np
import tifffile
from ez_ufo_qt.util import read_image


def open_tif_sequence(dir_name, row):
    sequence = []
    filenames = os.listdir(dir_name)
    filenames.sort()

    for filename in filenames:
        if '.tif' in filename:
            tif_img = read_image(os.path.join(dir_name, filename)).astype(np.uint16)
            sequence.append(np.array(tif_img)[(row - 10):(row + 10), :])
    return np.array(sequence)

def findCTdirs(root: str, tomo_name: str):
    """
    Walks directories rooted at "Input ctset" location
    Appends their absolute path to ctdir if they contain a ctset with same name as "tomo" entry in GUI
    """
    lvl0 = os.path.abspath(root)
    ctdirs = []
    for root, dirs, files in os.walk(lvl0):
        for name in dirs:
            if name == tomo_name:
                ctdirs.append(root)
    return ctdirs, lvl0

def find_overlap(args):
    # assign GUI arguments to variables

    root = args.indir
    proc = args.tmpdir
    output = args.outdir
    row_num = args.row_num
    overlap_min = args.overlap_min
    overlap_max = args.overlap_max
    overlap_increment = args.overlap_increment
    axis_on_left = args.axis_on_left

    # recursively create output temporary ctset if it doesn't exist
    if os.path.exists(proc):
        shutil.rmtree(proc)
        os.makedirs(proc)
    else:
        os.makedirs(proc)

    print("Finding CTDirs...")
    ctdirs, lvl0 = findCTdirs(root, "tomo")
    ctdirs.sort()
    print(ctdirs)

    # concatenate images end-to-end and generate a sinogram
    print('Opening half-acquisition image sequence...')

    for ctset in ctdirs:
        print("Working on ctset:" + str(ctset))
        index_dir = os.path.basename(os.path.normpath(ctset))

        os.makedirs(os.path.join(proc, index_dir, 'sinos'))

        tomo = open_tif_sequence(os.path.join(ctset, 'tomo'), row_num)

        # open flats and darks and average them
        flat = np.mean(open_tif_sequence(os.path.join(ctset, 'flats'), row_num) / 65535.0, axis=0)
        dark = np.mean(open_tif_sequence(os.path.join(ctset, 'darks'), row_num) / 65535.0, axis=0)
        if os.path.exists(os.path.join(ctset, 'flats2')):
            flat2 = np.mean(open_tif_sequence(os.path.join(ctset, 'flats2'), row_num) / 65535.0, axis=0)
        else:
            flat2 = flat

        tomo_single_row = tomo[:, tomo.shape[1] // 2, :] / 65535.0
        dark_single_row = np.tile(dark[tomo.shape[1] // 2, :], (tomo.shape[0], 1))
        flat_single_row = np.zeros((tomo.shape[0], tomo.shape[2]))
        img_height = tomo.shape[0]
        img_width = tomo.shape[1]

        del tomo

        # create interpolated sinogram of flats on the same row as we use for the projections, then carry out flat/dark correction
        print('Creating stitched sinograms...')
        for i in range(0, img_height):
            flat_single_row[i, :] = (flat[img_width // 2, :] * (float(i) / float(img_height)) + flat2[img_width // 2, :] * (
                        1.0 - float(i) / float(img_height)))

        tomo_sino_corr = (tomo_single_row - dark_single_row) / (flat_single_row - dark_single_row)
        max_gray_value = tomo_sino_corr.max()
        tomo_sino_corr = tomo_sino_corr / max_gray_value

        tomo_first_half = tomo_sino_corr[:int(tomo_sino_corr.shape[0] / 2), :]
        tomo_second_half = tomo_sino_corr[int(tomo_sino_corr.shape[0] / 2):tomo_sino_corr.shape[0], :]

        tomo_first_half = -1.0 * np.log(tomo_first_half)
        tomo_second_half = -1.0 * np.log(tomo_second_half)

        # flip half of corrected unstitched sinos (depending on right- or left-hand axis) and produce stitched sinos at regular increments TODO: fix code for right-hand axis case
        if axis_on_left:
            tomo_second_half_flipped = np.fliplr(tomo_second_half)

            for axis in range(overlap_min, overlap_max, overlap_increment):
                sino_halves = []
                sino_halves.append(tomo_second_half_flipped[:, :tomo_second_half_flipped.shape[1] - axis])
                sino_halves.append(tomo_first_half[:, axis:])
                stitched_sino = np.concatenate(sino_halves, axis=1)

                output_img = stitched_sino

                tifffile.imsave(os.path.join(proc, index_dir, 'sinos', 'axis-' + str(axis).zfill(4) + '.tif'),
                                output_img.astype(np.float32))

        # perform reconstructions for each sinogram and save to output folder
        print('Reconstructing stitched sinograms:')

        setid = ctset[len(lvl0)+1:]
        #print("setid: " + setid)
        out_pattern = os.path.join(args.outdir, setid)

        for filename in os.listdir(os.path.join(proc, index_dir, 'sinos')):
            if '.tif' in filename:
                current_img = np.array(read_image(os.path.join(proc, index_dir, 'sinos', filename)))
                axis = current_img.shape[1] / 2

                recon_cmd = 'tofu tomo  --output-bytes-per-file 0 --sinograms '\
                            + os.path.join(proc, index_dir, 'sinos', filename) + ' --output '\
                            + os.path.join(out_pattern, filename) + ' --axis ' + str(axis)
                os.system(recon_cmd)

        shutil.rmtree(os.path.join(proc, index_dir))
        print("Finished processing: " + str(index_dir))
        print("********************DONE********************")

    shutil.rmtree(proc)
    print("Finished processing: " + str(root))
