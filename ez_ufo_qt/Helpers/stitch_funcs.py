"""
Last modified on Dec 2, 2020
@author: sergei gasilov
"""

import glob
import os
import shutil

import numpy as np
import tifffile
from ez_ufo_qt.Helpers.helper_util import read_image
from ez_ufo_qt.Helpers.find_360_overlap import findCTdirs
import multiprocessing as mp
from functools import partial
import re
import warnings
import time


def prepare(parameters, dir_type: int, ctdir: str):
    """
    :param parameters: GUI params
    :param dir_type 1 if CTDir containing Z00-Z0N slices - 2 if parent directory containing CTdirs each containing Z slices:
    :param ctdir Name of the ctdir - blank string if not using multiple ctdirs:
    :return:
    """
    hmin, hmax = 0.0, 0.0
    if parameters['ezstitch_clip_histo']:
        if parameters['ezstitch_histo_min'] == parameters['ezstitch_histo_max']:
            raise ValueError(' - Define hmin and hmax correctly in order to convert to 8bit')
        else:
            hmin, hmax = parameters['ezstitch_histo_min'], parameters['ezstitch_histo_max']
    start, stop, step = [int(value) for value in parameters['ezstitch_start_stop_step'].split(',')]
    if not os.path.exists(parameters['ezstitch_output_dir']):
        os.makedirs(parameters['ezstitch_output_dir'])
    Vsteps = sorted(os.listdir(os.path.join(parameters['ezstitch_input_dir'], ctdir)))
    #determine input data type
    if dir_type == 1:
        tmp = os.path.join(parameters['ezstitch_input_dir'], Vsteps[0], parameters['ezstitch_type_image'], '*.tif')
        tmp = sorted(glob.glob(tmp))[0]
        indtype = type(read_image(tmp)[0][0])
    elif dir_type == 2:
        tmp = os.path.join(parameters['ezstitch_input_dir'], ctdir, Vsteps[0], parameters['ezstitch_type_image'], '*.tif')
        tmp = sorted(glob.glob(tmp))[0]
        indtype = type(read_image(tmp)[0][0])

    if parameters['ezstitch_stitch_orthogonal']:
        for vstep in Vsteps:
            if dir_type == 1:
                in_name = os.path.join(parameters['ezstitch_input_dir'], vstep, parameters['ezstitch_type_image'])
                out_name = os.path.join(parameters['ezstitch_temp_dir'], vstep, parameters['ezstitch_type_image'], 'sli-%04i.tif')
            elif dir_type == 2:
                in_name = os.path.join(parameters['ezstitch_input_dir'], ctdir, vstep, parameters['ezstitch_type_image'])
                out_name = os.path.join(parameters['ezstitch_temp_dir'], ctdir, vstep, parameters['ezstitch_type_image'], 'sli-%04i.tif')
            cmd = 'tofu sinos --projections {} --output {}'.format(in_name, out_name)
            cmd += " --y {} --height {} --y-step {}".format(start, stop-start, step)
            cmd += " --output-bytes-per-file 0"
            os.system(cmd)
            time.sleep(10)
        indir = parameters['ezstitch_temp_dir']
    else:
        indir = parameters['ezstitch_input_dir']
    return indir, hmin, hmax, start, stop, step, indtype


def exec_sti_mp(start, step, N, Nnew, Vsteps, indir, dx, M, parameters, ramp, hmin, hmax, indtype, ctdir, dir_type, j):
    index = start+j*step
    Large = np.empty((Nnew*len(Vsteps)+dx, M), dtype=np.float32)
    for i, vstep in enumerate(Vsteps[:-1]):
        if dir_type == 1:
            tmp = os.path.join(indir, Vsteps[i], parameters['ezstitch_type_image'], '*.tif')
            tmp1 = os.path.join(indir, Vsteps[i+1], parameters['ezstitch_type_image'], '*.tif')
        elif dir_type == 2:
            tmp = os.path.join(indir, ctdir, Vsteps[i], parameters['ezstitch_type_image'], '*.tif')
            tmp1 = os.path.join(indir, ctdir, Vsteps[i + 1], parameters['ezstitch_type_image'], '*.tif')
        if parameters['ezstitch_stitch_orthogonal']:
            tmp = sorted(glob.glob(tmp))[j]
            tmp1 = sorted(glob.glob(tmp1))[j]
        else:
            tmp = sorted(glob.glob(tmp))[index]
            tmp1 = sorted(glob.glob(tmp1))[index]
        first = read_image(tmp)
        second = read_image(tmp1)
        # sample moved downwards
        if parameters['ezstitch_sample_moved_down']:
            first, second = np.flipud(first), np.flipud(second)

        k = np.mean(first[N - dx:, :]) / np.mean(second[:dx, :])
        second = second * k

        a, b, c = i*Nnew, (i+1)*Nnew, (i+2)*Nnew
        Large[a:b, :] = first[:N-dx, :]
        Large[b:b+dx, :] = np.transpose(np.transpose(first[N-dx:, :])*(1 - ramp) + np.transpose(second[:dx, :]) * ramp)
        Large[b+dx:c+dx, :] = second[dx:, :]

    pout = os.path.join(parameters['ezstitch_output_dir'], ctdir, parameters['ezstitch_type_image']+'-sti-{:>04}.tif'.format(index))
    if not parameters['ezstitch_clip_histo']:
        tifffile.imsave(pout, Large.astype(indtype))
    else:
        Large = 255.0/(hmax-hmin) * (np.clip(Large, hmin, hmax) - hmin)
        tifffile.imsave(pout, Large.astype(np.uint8))

def main_sti_mp(parameters):
    #Check whether indir is CTdir or parent containing CTdirs
    #if indir + some z00 subdir + sli + *.tif does not exist then use original
    subdirs = sorted(os.listdir(parameters['ezstitch_input_dir']))
    if os.path.exists(os.path.join(parameters['ezstitch_input_dir'], subdirs[0], parameters['ezstitch_type_image'])):
        dir_type = 1
        ctdir = ""
        print(" - Using CT directory containing slices")
        if parameters['ezstitch_stitch_orthogonal']:
            print(" - Creating orthogonal sections")
        indir, hmin, hmax, start, stop, step, indtype = prepare(parameters, dir_type, "")
        dx = int(parameters['ezstitch_num_overlap_rows'])
        # second: stitch them
        Vsteps = sorted(os.listdir(indir))
        tmp = glob.glob(os.path.join(indir, Vsteps[0], parameters['ezstitch_type_image'], '*.tif'))[0]
        first = read_image(tmp)
        N, M = first.shape
        Nnew = N - dx
        ramp = np.linspace(0, 1, dx)

        J = range(int((stop - start) / step))
        pool = mp.Pool(processes=mp.cpu_count())
        exec_func = partial(exec_sti_mp, start, step, N, Nnew, \
                            Vsteps, indir, dx, M, parameters, ramp, hmin, hmax, indtype, ctdir, dir_type)
        print(" - Adjusting and stitching")
        # start = time.time()
        pool.map(exec_func, J)
        print("========== Done ==========")
    else:
        second_subdirs = sorted(os.listdir(os.path.join(parameters['ezstitch_input_dir'], subdirs[0])))
        if os.path.exists(os.path.join(parameters['ezstitch_input_dir'], subdirs[0], second_subdirs[0], parameters['ezstitch_type_image'])):
            print(" - Using parent directory containing CT directories, each of which contains slices")
            dir_type = 2
            #For each subdirectory do the same thing
            for ctdir in subdirs:
                print("-> Working on " + str(ctdir))
                if not os.path.exists(os.path.join(parameters['ezstitch_output_dir'], ctdir)):
                    os.makedirs(os.path.join(parameters['ezstitch_output_dir'], ctdir))
                if parameters['ezstitch_stitch_orthogonal']:
                    print(" - Creating orthogonal sections")
                indir, hmin, hmax, start, stop, step, indtype = prepare(parameters, dir_type, ctdir)
                dx = int(parameters['ezstitch_num_overlap_rows'])
                # second: stitch them
                Vsteps = sorted(os.listdir(os.path.join(indir, ctdir)))
                tmp = glob.glob(os.path.join(indir, ctdir, Vsteps[0], parameters['ezstitch_type_image'], '*.tif'))[0]
                first = read_image(tmp)
                N, M = first.shape
                Nnew = N - dx
                ramp = np.linspace(0, 1, dx)

                J = range(int((stop - start) / step))
                pool = mp.Pool(processes=mp.cpu_count())
                exec_func = partial(exec_sti_mp, start, step, N, Nnew, \
                                    Vsteps, indir, dx, M, parameters, ramp, hmin, hmax, indtype, ctdir, dir_type)
                print(" - Adjusting and stitching")
                # start = time.time()
                pool.map(exec_func, J)
                print("========== Done ==========")
                # Clear temp directory
                clear_tmp(parameters)
        else:
            print("Invalid input directory")
        complete_message()


def make_buf(tmp, l, a, b):
    first = read_image(tmp)
    N, M = first[a:b, :].shape
    return np.empty((N*l, M), dtype=first.dtype), N, first.dtype


def exec_conc_mp(start, step, example_im, l, parameters, zfold, indir, ctdir, j):
    index = start+j*step
    Large, N, dtype = make_buf(example_im, l, parameters['ezstitch_first_row'], parameters['ezstitch_last_row'])
    for i, vert in enumerate(zfold):
        tmp = os.path.join(indir, ctdir, vert, parameters['ezstitch_type_image'], '*.tif')
        if parameters['ezstitch_stitch_orthogonal']:
            fname=sorted(glob.glob(tmp))[j]
        else:
            fname=sorted(glob.glob(tmp))[index]
        frame = read_image(fname)[parameters['ezstitch_first_row']:parameters['ezstitch_last_row'], :]
        if parameters['ezstitch_sample_moved_down']:
            Large[i*N:N*(i+1), :] = np.flipud(frame)
        else:
            Large[i*N:N*(i+1), :] = frame

    pout = os.path.join(parameters['ezstitch_output_dir'], ctdir, parameters['ezstitch_type_image']+'-sti-{:>04}.tif'.format(index))
    #print "input data type {:}".format(dtype)
    tifffile.imsave(pout, Large)


def main_conc_mp(parameters):
    # Check whether indir is CTdir or parent containing CTdirs
    # if indir + some z00 subdir + sli + *.tif does not exist then use original
    subdirs = sorted(os.listdir(parameters['ezstitch_input_dir']))
    if os.path.exists(os.path.join(parameters['ezstitch_input_dir'], subdirs[0], parameters['ezstitch_type_image'])):
        dir_type = 1
        ctdir = ""
        print(" - Using CT directory containing slices")
        if parameters['ezstitch_stitch_orthogonal']:
            print(" - Creating orthogonal sections")
        #start = time.time()
        indir, hmin, hmax, start, stop, step, indtype = prepare(parameters, dir_type, ctdir)
        subdirs = [dI for dI in os.listdir(parameters['ezstitch_input_dir']) if os.path.isdir(os.path.join(parameters['ezstitch_input_dir'], dI))]
        zfold = sorted(subdirs)
        l = len(zfold)
        tmp = glob.glob(os.path.join(indir, zfold[0], parameters['ezstitch_type_image'], '*.tif'))
        J = range(int((stop-start)/step))
        pool = mp.Pool(processes=mp.cpu_count())
        exec_func = partial(exec_conc_mp, start, step, tmp[0], l, parameters, zfold, indir, ctdir)
        print(" - Concatenating")
        #start = time.time()
        pool.map(exec_func, J)
        #print "Images stitched in {:.01f} sec".format(time.time()-start)
        print("============ Done ============")
    else:
        second_subdirs = sorted(os.listdir(os.path.join(parameters['ezstitch_input_dir'], subdirs[0])))
        if os.path.exists(os.path.join(parameters['ezstitch_input_dir'], subdirs[0], second_subdirs[0], parameters['ezstitch_type_image'])):
            print(" - Using parent directory containing CT directories, each of which contains slices")
            dir_type = 2
            for ctdir in subdirs:
                print(" == Working on " + str(ctdir) + " ==")
                if not os.path.exists(os.path.join(parameters['ezstitch_output_dir'], ctdir)):
                    os.makedirs(os.path.join(parameters['ezstitch_output_dir'], ctdir))
                if parameters['ezstitch_stitch_orthogonal']:
                    print("   - Creating orthogonal sections")
                # start = time.time()
                indir, hmin, hmax, start, stop, step, indtype = prepare(parameters, dir_type, ctdir)
                zfold = sorted(os.listdir(os.path.join(indir, ctdir)))
                l = len(zfold)
                tmp = glob.glob(os.path.join(indir, ctdir, zfold[0], parameters['ezstitch_type_image'], '*.tif'))
                J = range(int((stop - start) / step))
                pool = mp.Pool(processes=mp.cpu_count())
                exec_func = partial(exec_conc_mp, start, step, tmp[0], l, parameters, zfold, indir, ctdir)
                print("   - Concatenating")
                # start = time.time()
                pool.map(exec_func, J)
                # print "Images stitched in {:.01f} sec".format(time.time()-start)
                print("============ Done ============")
                #Clear temp directory
                clear_tmp(parameters)
    complete_message()


############################## HALF ACQ ##############################
def stitch(first, second, axis, crop):
    h, w = first.shape
    if axis > w / 2:
        dx = int(2 * (w - axis) + 0.5)
    else:
        dx = int(2 * axis + 0.5)
        tmp = np.copy(first)
        first = second
        second = tmp
    result = np.empty((h, 2 * w - dx), dtype=first.dtype)
    ramp = np.linspace(0, 1, dx)

    # Mean values of the overlapping regions must match, which corrects flat-field inconsistency
    # between the two projections
    # We clip the values in second so that there are no saturated pixel overflow problems
    k = np.mean(first[:, w - dx:]) / np.mean(second[:, :dx])
    second = np.clip(second * k, np.iinfo(np.uint16).min, np.iinfo(np.uint16).max).astype(np.uint16)

    result[:, :w - dx] = first[:, :w - dx]
    result[:, w - dx:w] = first[:, w - dx:] * (1 - ramp) + second[:, :dx] * ramp
    result[:, w:] = second[:, dx:]

    return result[:, slice(int(crop), int(2*(w - axis) - crop), 1)]


def st_mp_idx(offst, ax, crop, in_fmt, out_fmt, idx):
    #we pass index and formats as argument
    first = read_image(in_fmt.format(idx))
    second = read_image(in_fmt.format(idx+offst))[:, ::-1]
    stitched = stitch(first, second, ax, crop)
    tifffile.imwrite(out_fmt.format(idx), stitched)


def main_360_mp_depth1(parameters):
    if not os.path.exists(parameters['ezstitch_output_dir']):
        os.makedirs(parameters['ezstitch_output_dir'])

    subdirs = [dI for dI in os.listdir(parameters['ezstitch_input_dir']) \
            if os.path.isdir(os.path.join(parameters['ezstitch_input_dir'], dI))]
    for i, sdir in enumerate(subdirs):
        names = sorted(glob.glob(os.path.join(parameters['ezstitch_input_dir'], sdir, '*.tif')))
        num_projs = len(names)
        if num_projs<2:
            warnings.warn("Warning: less than 2 files")
        print(str(num_projs) + ' files in ' + str(sdir))

        os.makedirs(os.path.join(parameters['ezstitch_output_dir'], sdir))
        out_fmt = os.path.join(parameters['ezstitch_output_dir'], sdir, 'sti-{:>04}.tif')

        # extraxt input file format
        firstfname = names[0]
        firstnum = re.match('.*?([0-9]+)$', firstfname[:-4]).group(1)
        n_dgts = len(firstnum) #number of significant digits
        idx0 = int(firstnum)
        trnc_len = n_dgts + 4 #format + .tif
        in_fmt = firstfname[:-trnc_len] + '{:0'+str(n_dgts)+'}.tif'

        pool = mp.Pool(processes=mp.cpu_count())
        offst = int(num_projs / 2)
        exec_func = partial(st_mp_idx, offst, parameters['ezstitch_axis_of_rotation'], 0, in_fmt, out_fmt)
        idxs = range(idx0, idx0+offst)
        # double check if names correspond - to remove later
        for nmi in idxs:
            #print(names[nmi-idx0], in_fmt.format(nmi))
            if names[nmi-idx0] != in_fmt.format(nmi):
                print('Something wrong with file name format')
                continue
        #pool.map(exec_func, names[0:num_projs/2])
        pool.map(exec_func, idxs)

    print("========== Done ==========")


def main_360_mp_depth2(parameters):

    if parameters['360multi_manual_axis']:
        print("Axis values: ", end='')
        print(parameters['360multi_axis_dict'])
        axis_list = list(parameters['360multi_axis_dict'].values())
        last_index = check_last_index(axis_list)

    ctdirs, lvl0 = findCTdirs(parameters['360multi_input_dir'], "tomo")

    ctlist = []
    for item in ctdirs:
        head, tail = os.path.split(item)
        ctlist.append(head)
    ctlist = sorted(list(set(ctlist)))
    print("Found the following directories:", ctlist)

    for ctdir in ctlist:
        print("================================================================")
        print(" -> Working On: " + str(ctdir))
        subdirs = [dI for dI in os.listdir(ctdir) if os.path.isdir(os.path.join(ctdir, dI))]
        print(" -> Contents: ", end="")
        print(sorted(subdirs))

        if len(glob.glob(os.path.join(ctdir, 'z??'))) > 0:

            num_slices = len(glob.glob(os.path.join(ctdir, 'z??')))
            print(str(num_slices) + " slices detected. stitching all slices....")

            if parameters['360multi_bottom_axis'] < parameters['360multi_top_axis']:
                axis_incr = float((parameters['360multi_top_axis'] - parameters['360multi_bottom_axis']) / float(num_slices - 1))
                range_start = 0
                range_end = num_slices
                range_increment = 1
            elif parameters['360multi_bottom_axis'] > parameters['360multi_top_axis']:
                axis_incr = float((parameters['360multi_bottom_axis'] - parameters['360multi_top_axis']) / float(num_slices - 1))
                range_start = num_slices - 1
                range_end = -1
                range_increment = -1

            for j in range(range_start, range_end, range_increment):
                head, tail = os.path.split(ctdir)
                if not os.path.exists(os.path.join(parameters['360multi_output_dir'], tail)):
                    os.makedirs(os.path.join(parameters['360multi_output_dir'], tail, "z" + str(j).zfill(2)))
                out_dir = os.path.join(parameters['360multi_output_dir'], tail, "z" + str(j).zfill(2))
                print("Output directory: " + out_dir)

                if parameters['360multi_manual_axis']:
                    curr_ax = int(list(axis_list)[j])
                    parameters['360multi_bottom_axis'] = int(list(axis_list)[0])
                    parameters['360multi_top_axis'] = int(list(axis_list)[last_index])
                else:
                    if parameters['360multi_bottom_axis'] < parameters['360multi_top_axis']:
                        curr_ax = parameters['360multi_bottom_axis'] + j * axis_incr
                    elif parameters['360multi_bottom_axis'] > parameters['360multi_top_axis']:
                        curr_ax = parameters['360multi_top_axis'] + j * axis_incr

                if parameters['360multi_crop_projections']:
                    if axis_incr < 0:
                        crop_amt = abs(parameters['360multi_bottom_axis'] - round(curr_ax))
                    else:
                        crop_amt = abs(parameters['360multi_top_axis'] - round(curr_ax))
                else:
                    crop_amt = 0

                subdirs = [dI for dI in os.listdir(os.path.join(ctdir, "z" + str(j).zfill(2))) \
                           if os.path.isdir(os.path.join(ctdir, "z" + str(j).zfill(2), dI))]

                print("processing slice: z" + str(j).zfill(2) + " using axis: " + str(
                    round(curr_ax)) + " and cropping by: " + str(crop_amt))
                print("axis_incr = " + str(axis_incr))
                print("curr_ax = " + str(curr_ax))

                for i, sdir in enumerate(subdirs):
                    names = sorted(glob.glob(os.path.join(ctdir, "z" + str(j).zfill(2), sdir, '*.tif')))
                    num_projs = len(names)
                    if num_projs < 2:
                        warnings.warn("Warning: less than 2 files")
                    print('{} files in {}'.format(num_projs, sdir))

                    os.makedirs(os.path.join(out_dir, sdir))
                    out_fmt = os.path.join(out_dir, sdir, 'sti-{:>04}.tif')

                    # extract input file format
                    firstfname = names[0]
                    firstnum = re.match('.*?([0-9]+)$', firstfname[:-4]).group(1)
                    n_dgts = len(firstnum)  # number of significant digits
                    idx0 = int(firstnum)
                    trnc_len = n_dgts + 4  # format + .tif
                    in_fmt = firstfname[:-trnc_len] + '{:0' + str(n_dgts) + '}.tif'

                    pool = mp.Pool(processes=mp.cpu_count())
                    offst = int(num_projs / 2)
                    exec_func = partial(st_mp_idx, offst, round(curr_ax), round(crop_amt), in_fmt, out_fmt)
                    idxs = range(idx0, idx0 + offst)
                    # double check if names correspond - to remove later
                    for nmi in idxs:
                        if names[nmi - idx0] != in_fmt.format(nmi):
                            print('Something wrong with file name format')
                            continue
                    pool.map(exec_func, idxs)

                print("=========== Done ===========")

        else:
            if not os.path.exists(parameters['360multi_output_dir']):
                os.makedirs(parameters['360multi_output_dir'])

            for i, sdir in enumerate(subdirs):
                names = sorted(glob.glob(os.path.join(ctdir, sdir, '*.tif')))
                num_projs = len(names)
                if num_projs < 2:
                    warnings.warn("Warning: less than 2 files")
                print('{} files in {}'.format(num_projs, sdir))

                os.makedirs(os.path.join(parameters['360multi_output_dir'], sdir))
                out_fmt = os.path.join(parameters['360multi_output_dir'], sdir, 'sti-{:>04}.tif')

                # extract input file format
                firstfname = names[0]
                firstnum = re.match('.*?([0-9]+)$', firstfname[:-4]).group(1)
                n_dgts = len(firstnum)  # number of significant digits
                idx0 = int(firstnum)
                trnc_len = n_dgts + 4  # format + .tif
                in_fmt = firstfname[:-trnc_len] + '{:0' + str(n_dgts) + '}.tif'

                pool = mp.Pool(processes=mp.cpu_count())
                offst = int(num_projs / 2)
                exec_func = partial(st_mp_idx, offst, parameters['360multi_axis'], in_fmt, out_fmt)
                idxs = range(idx0, idx0 + offst)
                # double check if names correspond - to remove later
                for nmi in idxs:
                    if names[nmi - idx0] != in_fmt.format(nmi):
                        print('Something wrong with file name format')
                        continue
                pool.map(exec_func, idxs)

            print("=========== Done ===========")
        print("-> Finished: " + str(ctdir))
    print("==== Finished processing all directories. ====")


def clear_tmp(parameters):
    tmp_dirs = os.listdir(parameters['ezstitch_temp_dir'])
    for tmp_dir in tmp_dirs:
        shutil.rmtree(os.path.join(parameters['ezstitch_temp_dir'], tmp_dir))


def check_last_index(axis_list):
    """
    Return the index of item in list immediately before first 'None' type
    :param axis_list:
    :return: the index of last non-None value
    """
    last_index = 0
    for index, item in enumerate(axis_list):
        if item is None:
            last_index = index - 1
            break
        else:
            last_index = axis_list.__len__() - 1
    return last_index

def complete_message():
    print("             __.-/|")
    print("             \\`o_O'")
    print("              =( )=  +-----+")
    print("                U|   | FIN |")
    print("      /\\  /\\   / |   +-----+")
    print("     ) /^\\) ^\\/ _)\\     |")
    print("     )   /^\\/   _) \\    |")
    print("     )   _ /  / _)  \\___|_")
    print(" /\\  )/\\/ ||  | )_)\\___,|))")
    print("<  >      |(,,) )__)    |")
    print(" ||      /    \\)___)\\")
    print(" | \\____(      )___) )____")
    print("  \\______(_______;;;)__;;;)")