import os
import glob
import numpy as np
import tifffile
import shutil
import math
import time
import yaml
import multiprocessing as mp
from functools import partial
from skimage import exposure, feature, filters


class AutoVerticalStitchFunctions:
    def __init__(self, parameters):
        self.lvl0 = os.path.abspath(parameters["projections_input_dir"])
        self.parameters = parameters
        self.z_dirs = []
        self.ct_dirs = []
        self.ct_stitch_pixel_dict = {}

    def run_vertical_auto_stitch(self):
        """
        Main function that calls all other functions
        """
        # Write parameters to .yaml file - quit if something goes wrong
        if self.write_yaml_params() == -1:
            return -1

        self.make_temp_dir()

        self.print_parameters()

        # Check input directory and find structure
        print("--> Finding Z-Directories")
        self.find_z_dirs()
        print(self.z_dirs)

        # Determine CT-directories from list of z-directories
        print("\n--> Finding CT-Directories")
        self.find_ct_dirs()
        print(self.ct_dirs)

        print("\n--> Finding Stitch Index")
        self.find_stitch_pixel()
        print("\nFound the following stitch pixel(s): ")
        print(self.ct_stitch_pixel_dict)

        # TODO: Need to maintain input ct-directory structure when slicing or stitching
        if not self.parameters['dry_run']:
            print("\n--> Stitching Images")
            if self.parameters['equalize_intensity']:
                print("Stitching using intensity equalization")
                self.main_stitch_multiproc()
            elif self.parameters['concatenate']:
                print("Stitching using concatenation")
                self.main_concatenate_multiproc()
        else:
            print("--> Finished Dry Run")

    def write_yaml_params(self):
        try:
            # Create the output directory root and save the parameters.yaml file
            os.makedirs(self.parameters['output_dir'], mode=0o777)
            file_path = os.path.join(self.parameters['output_dir'], 'auto_vertical_stitch_parameters.yaml')
            file_out = open(file_path, 'w')
            yaml.dump(self.parameters, file_out)
            print("Parameters file saved at: " + str(file_path))
            return 0
        except FileExistsError:
            print("--> Output Directory Exists - Delete Before Proceeding")
            return -1

    def find_z_dirs(self):
        """
        Walks directories rooted at "Input Directory" location
        Appends their absolute path to ct-dir if they contain a directory with same name as "tomo" entry in GUI
        :return: Sets a list of z-directory paths in class member self.z_dirs
        """
        for root, dirs, files in os.walk(self.lvl0):
            for name in dirs:
                if name == "tomo":
                    self.z_dirs.append(root)
        self.z_dirs = sorted(list(set(self.z_dirs)))

    def find_ct_dirs(self):
        """
        Gets absolute path to parent directories containing z-subdirectories.
        :return: Sets a list of ct-directory paths in class member self.ct_dirs
        """
        temp_ct_dirs = []
        for z_path in self.z_dirs:
            ct_dir_path, z_dir = os.path.split(z_path)
            temp_ct_dirs.append(ct_dir_path)
        self.ct_dirs = sorted(list(set(temp_ct_dirs)))

    def find_stitch_pixel(self):
        """
        Looks at each ct-directory, finds the midpoint z-directory and it's successor
        We then use images from the "tomo" directory to determine the point of overlap
        """
        index = 0
        for ct_dir in self.ct_dirs:
            z_list = sorted([dI for dI in os.listdir(ct_dir) if os.path.isdir(os.path.join(ct_dir, dI))])
            print(z_list)

            # Get list of z-directories within each ct directory
            midpoint_zdir = z_list[int(len(z_list) / 2)-1]
            one_after_midpoint_zdir = z_list[int(len(z_list) / 2)]

            print("Working on: " + ct_dir)
            print("Using middle z-directories for correlation:")
            print("-  " + midpoint_zdir)
            print("-  " + one_after_midpoint_zdir)

            # Get the 'middle' z-directories
            midpoint_zdir_tomo = os.path.join(ct_dir, midpoint_zdir, "tomo")
            one_after_midpoint_zdir_tomo = os.path.join(ct_dir, one_after_midpoint_zdir, "tomo")
            # Get the list of images in these 'middle' z-directories
            midpoint_image_list = sorted(glob.glob(os.path.join(midpoint_zdir_tomo, '*.tif')))
            one_after_midpoint_image_list = sorted(glob.glob(os.path.join(one_after_midpoint_zdir_tomo, '*.tif')))

            stitch_pixel_list = []
            # We divide total number of images by 10 to get step value. For 1500 images we compare every 150th image
            step_value = int(len(midpoint_image_list) / 10)
            image_index = range(0, len(midpoint_image_list)+step_value, step_value)
            pool = mp.Pool(processes=mp.cpu_count())
            exec_func = partial(self.find_stitch_pixel_multiproc, midpoint_image_list, one_after_midpoint_image_list)
            stitch_pixel_list = pool.map(exec_func, image_index)

            #print(stitch_pixel_list)
            most_common_value = max(set(stitch_pixel_list), key=stitch_pixel_list.count)
            self.ct_stitch_pixel_dict[ct_dir] = int(most_common_value)

    def find_stitch_pixel_multiproc(self, midpoint_image_list, one_after_midpoint_image_list, image_index):
        """
        Determines the point at which the two images overlap
        :param midpoint_image_list: List of images in the middle vertical step directory (z-directory)
        :param one_after_midpoint_image_list: List of images in vertical step directory one after the middle
        :param image_index: Index of images to compare between the two vertical step directories
        :return: The pixel row at which the two images overlap
        """
        if image_index > 0:
            image_index = image_index - 1
        midpoint_first_image_path = midpoint_image_list[image_index]
        one_after_midpoint_first_image_path = one_after_midpoint_image_list[image_index]
        return self.compute_stitch_pixel(midpoint_first_image_path, one_after_midpoint_first_image_path)

    def compute_stitch_pixel(self, upper_image: str, lower_image: str):
        """
        Takes two pairs of images with vertical overlap, determines the point at which to stitch the images
        :param upper_image: Absolute path to the top image
        :param lower_image: Absolute path t the lower image
        :return:
        """
        print("Correlating images:")
        print(upper_image)
        print(lower_image)

        # Read in the images to numpy array
        if not self.parameters['sample_moved_down']:
            first = self.read_image(upper_image, False)
            second = self.read_image(lower_image, False)
        elif self.parameters['sample_moved_down']:
            first = self.read_image(upper_image, True)
            second = self.read_image(lower_image, True)

        #tifffile.imwrite(os.path.join(self.parameters['temp_dir'], 'first.tif'), first)
        #tifffile.imwrite(os.path.join(self.parameters['temp_dir'], 'second.tif'), second)

        # Do flat field correction using flats/darks directory in same ctdir as input images
        if not self.parameters['common_flats_darks']:
            tomo_path, filename = os.path.split(upper_image)
            zdir_path, tomo_name = os.path.split(tomo_path)
            flats_path = os.path.join(zdir_path, "flats")
            darks_path = os.path.join(zdir_path, "darks")
            flat_files = self.get_filtered_filenames(flats_path)
            dark_files = self.get_filtered_filenames(darks_path)
        elif self.parameters['common_flats_darks']:
            flat_files = self.get_filtered_filenames(self.parameters['flats_dir'])
            dark_files = self.get_filtered_filenames(self.parameters['darks_dir'])
        
        flats = np.array([tifffile.TiffFile(x).asarray().astype(np.float) for x in flat_files])
        darks = np.array([tifffile.TiffFile(x).asarray().astype(np.float) for x in dark_files])
        dark = np.mean(darks, axis=0)
        flat = np.mean(flats, axis=0) - dark
        first = (first - dark) / flat
        second = (second - dark) / flat

        #tifffile.imwrite(os.path.join(self.parameters['temp_dir'], 'first_flat_corrected.tif'), first)
        #tifffile.imwrite(os.path.join(self.parameters['temp_dir'], 'second_flat_corrected.tif'), second)

        # Equalize the histograms and match them so that images are more similar
        first = exposure.equalize_hist(first)
        second = exposure.equalize_hist(second)
        second = exposure.match_histograms(second, first)

        # Apply sobel filtering to find gradients of images
        first = filters.sobel(first)
        second = filters.sobel(second)

        # Equalize the histograms and match them so that images are more similar
        first = exposure.equalize_hist(first)
        second = exposure.equalize_hist(second)
        second = exposure.match_histograms(second, first)

        # Apply canny edge detection on sobel filtered and equalized images
        first = feature.canny(first)
        second = feature.canny(second)

        #tifffile.imwrite(os.path.join(self.parameters['temp_dir'], 'first_edges.tif'), first)
        #tifffile.imwrite(os.path.join(self.parameters['temp_dir'], 'second_edges.tif'), second)

        # Flip and rotate the images so that they have same orientation as auto_horizontal_stitch
        first = np.rot90(first)
        second = np.rot90(second)
        first = np.fliplr(first)

        #tifffile.imwrite(os.path.join(self.parameters['temp_dir'], 'first_fliprot_edges.tif'), first)
        #tifffile.imwrite(os.path.join(self.parameters['temp_dir'], 'second_fliprot_edges.tif'), second)

        # We must crop the both images from left column of image until overlap region
        first_cropped = first[:, :int(self.parameters['overlap_region'])]
        second_cropped = second[:, :int(self.parameters['overlap_region'])]

        #tifffile.imwrite(os.path.join(self.parameters['temp_dir'], 'first_cropped.tif'), first_cropped)
        #tifffile.imwrite(os.path.join(self.parameters['temp_dir'], 'second_cropped.tif'), second_cropped)

        return self.compute_rotation_axis(first_cropped, second_cropped)

    # Stitching Functions
    def prepare(self, ct_dir):
        """
        Creates resliced orthogonal images in temp dirctory if 'reslice' radio button selected
        :param ct_dir: path to ct_directory containing z-directories "vertical views"
        :return: "indir" - input directory to be used at next stage for stitching,
                 "start, stop, step" determine which images to stitch
                 "input_data_type" type of images to stitch
        """
        start, stop, step = [int(value) for value in self.parameters['images_to_stitch'].split(',')]

        if not os.path.exists(self.parameters['output_dir']):
            os.makedirs(self.parameters['output_dir'])
        print("Preparing to stitch: " + str(ct_dir))
        vertical_steps = sorted([dI for dI in os.listdir(ct_dir) if os.path.isdir(os.path.join(ct_dir, dI))])
        # determine input data type
        tmp = os.path.join(ct_dir, vertical_steps[0], 'tomo', '*.tif')
        tmp = sorted(glob.glob(tmp))[0]
        input_data_type = type(self.read_image(tmp, flip_image=False)[0][0])

        # Could use os.path.relpath too
        ct_path = self.build_ct_path(ct_dir)
        print("ct_path: ", end="")
        print(ct_path)

        if self.parameters['reslice']:
            print("Creating orthogonal sections")
            for v_step in vertical_steps:
                in_name = os.path.join(self.parameters['recon_slices_input_dir'], ct_path, v_step, "sli")
                out_name = os.path.join(self.parameters['temp_dir'], ct_path, v_step, 'sli-%04i.tif')
                cmd = 'tofu sinos --projections {} --output {}'.format(in_name, out_name)
                cmd += " --y {} --height {} --y-step {}".format(start, stop - start, step)
                cmd += " --output-bytes-per-file 0"
                os.system(cmd)
                time.sleep(10)
            stitch_input_dir_path = os.path.join(self.parameters['temp_dir'],  ct_path)
        else:
            if self.parameters['stitch_reconstructed_slices']:
                stitch_input_dir_path = os.path.join(self.parameters['recon_slices_input_dir'], ct_path)
            elif self.parameters['stitch_projections']:
                stitch_input_dir_path = os.path.join(self.parameters['projections_input_dir'], ct_path)
        return stitch_input_dir_path, start, stop, step, input_data_type, ct_path

    def build_ct_path(self, ct_dir):
        """
        Gets the suffix difference of the ct_dir and projections_input_dir
        :param ct_dir:
        :return: diff of two strings
        """
        head = ct_dir
        tail_list = []
        while head != self.parameters['projections_input_dir']:
            head, tail = os.path.split(head)
            tail_list.append(tail)
        if len(tail_list) > 1:
            tail_list.reverse()
        str_buff = ''
        for dir_str in tail_list:
            str_buff += dir_str
            str_buff += '/'
        return str_buff[:-1]

    # Interpolate and Equalize Intensity
    def main_stitch_multiproc(self):
        """
        Stitch images using interpolation and intensity equalization
        :return: None
        """
        for ct_dir in self.ct_dirs:
            stitch_input_dir_path, start, stop, step, input_dir_type, ct_path = self.prepare(ct_dir)
            # We multiply this by two when using interpolation and intensity equalization
            dx = 2 * int(self.ct_stitch_pixel_dict[ct_dir])
            # second: stitch them
            if self.parameters['stitch_reconstructed_slices']:
                if self.parameters['reslice']:
                    vertical_steps = sorted(os.listdir(stitch_input_dir_path))
                    tmp = glob.glob(os.path.join(stitch_input_dir_path, vertical_steps[0], '*.tif'))[0]
                elif not self.parameters['reslice']:
                    vertical_steps = sorted(os.listdir(self.parameters['recon_slices_input_dir']))
                    tmp = glob.glob(os.path.join(stitch_input_dir_path, vertical_steps[0], 'sli', '*.tif'))[0]
            elif self.parameters['stitch_projections']:
                vertical_steps = sorted(os.listdir(self.parameters['projections_input_dir']))
                tmp = glob.glob(os.path.join(stitch_input_dir_path, vertical_steps[0], 'tomo', '*.tif'))[0]

            first = self.read_image(tmp, flip_image=False)
            num_rows, num_columns = first.shape
            num_rows_new = num_rows - dx
            ramp = np.linspace(0, 1, dx)

            j_index = range(int((stop - start) / step))
            pool = mp.Pool(processes=mp.cpu_count())
            exec_func = partial(self.exec_stitch_multiproc, stitch_input_dir_path, start, step, num_rows,
                                num_rows_new, vertical_steps, dx, num_columns, ramp, input_dir_type, ct_path)
            print("Adjusting and stitching")
            pool.map(exec_func, j_index)
            print(f"========== Finished Stitching {ct_dir} ==========")
        print("========== Completed Stitching For All CT-Directories ==========")

    def exec_stitch_multiproc(self, stitch_input_dir_path, start, step, num_rows, num_rows_new, vertical_steps,
                              dx, num_columns, ramp, input_dir_type, ct_path, j):
        """
        Stitch images using interpolation and intensity equalization
        :param start: Image index to start stitching
        :param step: Value to skip for each image stitched
        :param num_rows: Number of rows in the original image
        :param num_rows_new: Number of rows in the new stitched image
        :param vertical_steps: List of vertical steps (z-directories)
        :param dx:
        :param num_columns: Number of columns in the original image
        :param ramp:
        :param input_dir_type:
        :param j:
        :return: None - writes stitched image to output directory
        """
        index = start + j * step
        large_image_buffer = np.empty((num_rows_new * len(vertical_steps) + dx, num_columns), dtype=np.float32)
        for i, v_step in enumerate(vertical_steps[:-1]):
            if self.parameters['stitch_reconstructed_slices']:
                if self.parameters['reslice']:
                    dir_type = ''
                elif not self.parameters['reslice']:
                    dir_type = 'sli'
            elif self.parameters['stitch_projections']:
                dir_type = 'tomo'

            tmp = os.path.join(stitch_input_dir_path, vertical_steps[i], dir_type, '*.tif')
            tmp1 = os.path.join(stitch_input_dir_path, vertical_steps[i + 1], dir_type, '*.tif')

            if self.parameters['reslice']:
                tmp = sorted(glob.glob(tmp))[j]
                tmp1 = sorted(glob.glob(tmp1))[j]
            else:
                tmp = sorted(glob.glob(tmp))[index]
                tmp1 = sorted(glob.glob(tmp1))[index]
            first = self.read_image(tmp, flip_image=False)
            second = self.read_image(tmp1, flip_image=False)
            if self.parameters['sample_moved_down']:
                first, second = np.flipud(first), np.flipud(second)

            k = np.mean(first[num_rows - dx:, :]) / np.mean(second[:dx, :])
            second = second * k

            a, b, c = i * num_rows_new, (i + 1) * num_rows_new, (i + 2) * num_rows_new
            large_image_buffer[a:b, :] = first[:num_rows - dx, :]
            large_image_buffer[b:b + dx, :] = np.transpose(
                np.transpose(first[num_rows - dx:, :]) * (1 - ramp) + np.transpose(second[:dx, :]) * ramp)
            large_image_buffer[b + dx:c + dx, :] = second[dx:, :]

        output_path = os.path.join(self.parameters['output_dir'], ct_path)
        if not os.path.isdir(output_path):
            os.makedirs(output_path, exist_ok=True, mode=0o777)
        output_path = os.path.join(output_path, '-sti-{:>04}.tif'.format(index))
        # TODO: Make sure to preserve bitdepth
        tifffile.imsave(output_path, large_image_buffer.astype(input_dir_type))

    # TODO : Also stitch flats/darks for both common and not common for concat and equalize intensity
    # Concatenation
    def main_concatenate_multiproc(self):
        """
        Stitches images using concatenation, splits across multiple processes/cpu-cores
        :return:
        """
        for ct_dir in self.ct_dirs:
            print(ct_dir, end=' ')
            print(self.ct_stitch_pixel_dict[ct_dir])
            stitch_input_dir_path, start, stop, step, input_data_type, ct_path = self.prepare(ct_dir)
            print("Finished preparation")
            z_fold = sorted([dI for dI in os.listdir(ct_dir) if os.path.isdir(os.path.join(ct_dir, dI))])
            num_z_dirs = len(z_fold)

            if self.parameters['stitch_reconstructed_slices']:
                if self.parameters['reslice']:
                    dir_type = ''
                    image_path = os.path.join(self.parameters['temp_dir'], ct_path, z_fold[0], dir_type, '*.tif')
                elif not self.parameters['reslice']:
                    dir_type = 'sli/'
                    image_path = os.path.join(self.parameters['recon_slices_input_dir'], ct_path,
                                              z_fold[0], dir_type, '*.tif')
            elif self.parameters['stitch_projections']:
                dir_type = 'tomo/'
                image_path = os.path.join(ct_dir, z_fold[0], dir_type, '*.tif')
            image_list = glob.glob(image_path)

            j_index = range(int((stop - start) / step))
            pool = mp.Pool(processes=mp.cpu_count())
            exec_func = partial(self.exec_concatenate_multiproc, start, step, image_list[0],
                                num_z_dirs, z_fold, stitch_input_dir_path, ct_dir, ct_path)
            print("Concatenating")
            pool.map(exec_func, j_index)
            print(f"========== Finished Stitching {ct_dir} ==========")
        print("========== Completed Stitching For All CT-Directories ==========")

    def exec_concatenate_multiproc(self, start, step, example_image_path, num_z_dirs, z_fold,
                                   stitch_input_dir_path, ct_dir, ct_path, j):
        """
        Stitches images using concatenation
        :param start: starting image index
        :param step: distance between images to be stitched
        :param example_image_path: Image from input dir, used to determine dimensions
        :param num_z_dirs: Number of vertical steps (z-directories) in the input ct directory
        :param z_fold: List of paths to the z-directories in current ct directory
        :param stitch_input_dir_path: Path to input images to be stitched
        :param ct_dir: Path to the ct_directory
        :param j: Index for multiprocessing
        :return: None - writes stitched images to output directory
        """
        index = start + j * step
        # r1 stitch pixel value - we just concatenate here by appending one image to the other
        example_image_array = self.read_image(example_image_path, flip_image=False)
        image_height = np.shape(example_image_array)[0]
        r1 = self.ct_stitch_pixel_dict[ct_dir]
        # r2 image height - stitch pixel value
        r2 = image_height - self.ct_stitch_pixel_dict[ct_dir]

        large_stitch_buffer, image_rows, dtype = self.make_buf(example_image_path, num_z_dirs, r1, r2)
        for i, z_dir in enumerate(z_fold):
            if self.parameters['stitch_reconstructed_slices']:
                if self.parameters['reslice']:
                    tmp = os.path.join(stitch_input_dir_path, z_dir, '*.tif')
                elif not self.parameters['reslice']:
                    tmp = os.path.join(stitch_input_dir_path, z_dir, 'sli', '*.tif')
            elif self.parameters['stitch_projections']:
                tmp = os.path.join(stitch_input_dir_path, z_dir, 'tomo', '*.tif')
            if self.parameters['reslice']:
                file_name = sorted(glob.glob(tmp))[j]
            else:
                file_name = sorted(glob.glob(tmp))[index]
            frame = self.read_image(file_name, flip_image=False)[r1:r2, :]
            if self.parameters['sample_moved_down']:
                large_stitch_buffer[i * image_rows:image_rows * (i + 1), :] = np.flipud(frame)
            else:
                large_stitch_buffer[i * image_rows:image_rows * (i + 1), :] = frame

        output_path = os.path.join(self.parameters['output_dir'], ct_path)
        if not os.path.exists(output_path):
            os.makedirs(output_path, exist_ok=True, mode=0o777)
        output_path = os.path.join(output_path, '-sti-{:>04}.tif'.format(index))
        # print "input data type {:}".format(dtype)
        # TODO: Make sure to preserve bitdepth
        tifffile.imsave(output_path, large_stitch_buffer)

    def make_buf(self, tmp, num_z_dirs, a, b):
        """
        Creates a large buffer image to store the stitched images in memory before writing
        :param tmp: Path to an example input image
        :param num_z_dirs: Number of vertical steps (z-directories)
        :param a: stitch pixel value
        :param b: image height - stitch pixel value
        :return: Empty array large enough to hold stitched images in RAM
        """
        first = self.read_image(tmp, flip_image=False)
        image_rows, image_columns = first[a:b, :].shape
        return np.empty((image_rows * num_z_dirs, image_columns), dtype=first.dtype), image_rows, first.dtype

    def make_temp_dir(self):
        if os.path.isdir(self.parameters['temp_dir']):
            shutil.rmtree(self.parameters['temp_dir'])
        os.makedirs(self.parameters['temp_dir'], mode=0o777)

    def print_parameters(self):
        """
        Prints parameter values with line formatting
        """
        print()
        print("**************************** Running Auto Vertical Stitch ****************************")
        print("======================== Parameters ========================")
        print("Projections Input Directory: " + self.parameters['projections_input_dir'])
        print("Reconstructed Slices Input Directory: " + self.parameters['recon_slices_input_dir'])
        print("Output Directory: " + self.parameters['output_dir'])
        print("Temp Directory: " + self.parameters['temp_dir'])
        print("Using common set of flats and darks: " + str(self.parameters['common_flats_darks']))
        print("Flats Directory: " + self.parameters['flats_dir'])
        print("Darks Directory: " + self.parameters['darks_dir'])
        print("Sample moved down: " + str(self.parameters['sample_moved_down']))
        print("Overlap Region Size: " + self.parameters['overlap_region'])
        print("Stitch Reconstructed Slices: " + str(self.parameters['stitch_reconstructed_slices']))
        print("Stitch Projections: " + str(self.parameters['stitch_projections']))
        print("Reslice: " + str(self.parameters['reslice']))
        print("Equalize Intensity: " + str(self.parameters['equalize_intensity']))
        print("Concatenate: " + str(self.parameters['concatenate']))
        print("Which images to stitch - start,stop,step: " + str(self.parameters['images_to_stitch']))
        print("Dry Run: " + str(self.parameters['dry_run']))
        print("============================================================")

    """****** BORROWED FUNCTIONS ******"""
    def get_filtered_filenames(self, path, exts=['.tif', '.edf']):
        result = []
        try:
            for ext in exts:
                result += [os.path.join(path, f) for f in os.listdir(path) if f.endswith(ext)]
        except OSError:
            return []
        return sorted(result)

    def compute_rotation_axis(self, first_projection, last_projection):
        """
        Compute the tomographic rotation axis based on cross-correlation technique.
        *first_projection* is the projection at 0 deg, *last_projection* is the projection
        at 180 deg.
        """
        from scipy.signal import fftconvolve
        width = first_projection.shape[1]
        first_projection = first_projection - first_projection.mean()
        last_projection = last_projection - last_projection.mean()

        # The rotation by 180 deg flips the image horizontally, in order
        # to do cross-correlation by convolution we must also flip it
        # vertically, so the image is transposed and we can apply convolution
        # which will act as cross-correlation
        convolved = fftconvolve(first_projection, last_projection[::-1, :], mode='same')
        #tifffile.imwrite(os.path.join(self.parameters['temp_dir'], 'convolved.tif'), convolved)
        center = np.unravel_index(convolved.argmax(), convolved.shape)[1]

        return (width / 2.0 + center) / 2

    def read_image(self, file_name, flip_image):
        """
        Reads in a tiff image from disk at location specified by file_name, returns a numpy array
        :param file_name: Str - path to file
        :param flip_image: Bool - Whether image is to be flipped vertically or not
        :return: A numpy array of type float
        """
        with tifffile.TiffFile(file_name) as tif:
            image = tif.pages[0].asarray(out='memmap')
        if flip_image is True:
            image = np.flipud(image)
        return image

    def col_round(self, x):
        frac = x - math.floor(x)
        if frac < 0.5:
            return math.floor(x)
        return math.ceil(x)
