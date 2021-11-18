import os
import sys
import logging
import shutil
import yaml

from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QGroupBox, QLabel, QCheckBox, QFileDialog, QMessageBox,\
                            QApplication, QGridLayout, QRadioButton
from ez_ufo_qt.GUI.StitchTools.auto_vertical_stitch_funcs import AutoVerticalStitchFunctions


class AutoVerticalStitchGUI(QGroupBox):
    def __init__(self):
        super().__init__()
        self.setTitle('Auto Vertical Stitch')

        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        self.parameters = {'parameters_type': 'auto_vertical_stitch'}
        self.auto_vertical_stitch_funcs = None

        self.projections_input_button = QPushButton("Select Projections Input Path")
        self.projections_input_button.clicked.connect(self.projections_input_button_pressed)
        self.projections_input_entry = QLineEdit()
        self.projections_input_entry.textChanged.connect(self.set_projections_input_entry)

        self.recon_slices_input_button = QPushButton("Select Reconstructed Slices Input Path")
        self.recon_slices_input_button.clicked.connect(self.recon_slices_input_button_pressed)
        self.recon_slices_input_entry = QLineEdit()
        self.recon_slices_input_entry.textChanged.connect(self.set_recon_slices_input_entry)

        self.output_button = QPushButton("Select Output Path")
        self.output_button.clicked.connect(self.output_button_pressed)
        self.output_entry = QLineEdit()
        self.output_entry.textChanged.connect(self.set_output_entry)

        self.temp_button = QPushButton("Select Temporary Directory")
        self.temp_button.clicked.connect(self.temp_button_pressed)
        self.temp_entry = QLineEdit()
        self.temp_entry.textChanged.connect(self.set_temp_entry)

        self.flats_darks_group = QGroupBox("Use Common Set of Flats and Darks")
        self.flats_darks_group.clicked.connect(self.set_flats_darks_group)

        self.flats_button = QPushButton("Select Flats Path")
        self.flats_button.clicked.connect(self.flats_button_pressed)
        self.flats_entry = QLineEdit()
        self.flats_entry.textChanged.connect(self.set_flats_entry)

        self.darks_button = QPushButton("Select Darks Path")
        self.darks_button.clicked.connect(self.darks_button_pressed)
        self.darks_entry = QLineEdit()
        self.darks_entry.textChanged.connect(self.set_darks_entry)

        self.overlap_region_label = QLabel("Overlapping Pixels")
        self.overlap_region_entry = QLineEdit()
        self.overlap_region_entry.textChanged.connect(self.set_overlap_region_entry)

        self.sample_moved_down_checkbox = QCheckBox("Was the sample moved down during experiment?")
        self.sample_moved_down_checkbox.stateChanged.connect(self.set_sample_moved_down_checkbox)

        self.stitch_reconstructed_slices_rButton = QRadioButton("Stitch Reconstructed Slices")
        self.stitch_reconstructed_slices_rButton.clicked.connect(self.stitch_reconstructed_slices_rButton_clicked)

        self.stitch_projections_rButton = QRadioButton("Stitch Projections")
        self.stitch_projections_rButton.clicked.connect(self.stitch_projections_rButton_clicked)

        self.equalize_intensity_rButton = QRadioButton("Equalize Intensity")
        self.equalize_intensity_rButton.clicked.connect(self.equalize_intensity_rButton_clicked)

        self.concatenate_rButton = QRadioButton("Concatenate")
        self.concatenate_rButton.clicked.connect(self.concatenate_rButton_clicked)

        self.reslice_checkbox = QCheckBox("Reslice")
        self.reslice_checkbox.stateChanged.connect(self.set_reslice_checkbox)

        self.which_images_to_stitch_label = QLabel("Which images to be stitched: start,stop,step:")
        self.which_images_to_stitch_entry = QLineEdit()
        self.which_images_to_stitch_entry.textChanged.connect(self.set_which_images_to_stitch)

        self.save_params_button = QPushButton("Save parameters")
        self.save_params_button.clicked.connect(self.save_params_button_clicked)

        self.import_params_button = QPushButton("Import parameters")
        self.import_params_button.clicked.connect(self.import_params_button_clicked)

        self.help_button = QPushButton("Help")
        self.help_button.clicked.connect(self.help_button_pressed)

        self.delete_temp_button = QPushButton("Delete Output Directory")
        self.delete_temp_button.clicked.connect(self.delete_button_pressed)

        self.stitch_button = QPushButton("Stitch")
        self.stitch_button.clicked.connect(self.stitch_button_pressed)

        self.dry_run_checkbox = QCheckBox("Dry Run")
        self.dry_run_checkbox.stateChanged.connect(self.set_dry_run_checkbox)

        self.set_layout()
        #self.resize(800, 0)
        #self.setFixedSize(800, 0)

        self.init_values()
        self.show()

    def set_layout(self):
        self.setMaximumSize(900, 450)

        layout = QGridLayout()
        layout.addWidget(self.projections_input_button, 0, 0, 1, 2)
        layout.addWidget(self.projections_input_entry, 0, 2, 1, 4)

        layout.addWidget(self.recon_slices_input_button, 1, 0, 1, 2)
        layout.addWidget(self.recon_slices_input_entry, 1, 2, 1, 4)

        layout.addWidget(self.output_button, 2, 0, 1, 2)
        layout.addWidget(self.output_entry, 2, 2, 1, 4)

        layout.addWidget(self.temp_button, 3, 0, 1, 2)
        layout.addWidget(self.temp_entry, 3, 2, 1, 4)

        self.flats_darks_group.setCheckable(True)
        self.flats_darks_group.setChecked(False)
        flats_darks_layout = QGridLayout()
        flats_darks_layout.addWidget(self.flats_button, 0, 0, 1, 2)
        flats_darks_layout.addWidget(self.flats_entry, 0, 2, 1, 2)
        flats_darks_layout.addWidget(self.darks_button, 1, 0, 1, 2)
        flats_darks_layout.addWidget(self.darks_entry, 1, 2, 1, 2)
        self.flats_darks_group.setLayout(flats_darks_layout)
        layout.addWidget(self.flats_darks_group, 4, 0, 1, 4)

        layout.addWidget(self.overlap_region_label, 5, 2)
        layout.addWidget(self.overlap_region_entry, 5, 3)
        layout.addWidget(self.sample_moved_down_checkbox, 5, 0, 1, 2)

        stitch_group = QGroupBox()
        stitch_layout = QGridLayout()
        stitch_layout.addWidget(self.stitch_reconstructed_slices_rButton, 0, 0)
        stitch_layout.addWidget(self.stitch_projections_rButton, 0, 1)
        stitch_layout.addWidget(self.reslice_checkbox, 1, 0)
        stitch_group.setLayout(stitch_layout)
        layout.addWidget(stitch_group, 6, 0, 1, 2)

        stitch_type_group = QGroupBox()
        stitch_type_layout = QGridLayout()
        stitch_type_layout.addWidget(self.equalize_intensity_rButton, 0, 0)
        stitch_type_layout.addWidget(self.concatenate_rButton, 0, 1)
        stitch_type_group.setLayout(stitch_type_layout)
        layout.addWidget(stitch_type_group, 6, 2, 1, 2)

        layout.addWidget(self.which_images_to_stitch_label, 7, 0, 1, 2)
        layout.addWidget(self.which_images_to_stitch_entry, 7, 2, 1, 2)

        layout.addWidget(self.save_params_button, 8, 0, 1, 2)
        layout.addWidget(self.import_params_button, 8, 3, 1, 1)
        layout.addWidget(self.help_button, 8, 2, 1, 1)

        layout.addWidget(self.stitch_button, 9, 0, 1, 2)
        layout.addWidget(self.dry_run_checkbox, 9, 2, 1, 1)
        layout.addWidget(self.delete_temp_button, 9, 3, 1, 1)
        self.setLayout(layout)

    def init_values(self):
        self.projections_input_entry.setText("...enter input directory containing projections")
        self.recon_slices_input_entry.setText("...enter directory containing reconstructed slices")
        self.output_entry.setText("...enter output directory")
        self.temp_entry.setText("...enter temporary directory")
        self.flats_entry.setText("...enter flats directory")
        self.parameters['common_flats_darks'] = False
        self.parameters['flats_dir'] = ""
        self.darks_entry.setText("...enter darks directory")
        self.parameters['darks_dir'] = ""
        self.overlap_region_entry.setText("300")
        self.parameters['overlap_region'] = "300"
        self.sample_moved_down_checkbox.setChecked(False)
        self.parameters['sample_moved_down'] = False
        self.stitch_reconstructed_slices_rButton.setChecked(True)
        self.parameters['stitch_reconstructed_slices'] = True
        self.stitch_projections_rButton.setChecked(False)
        self.parameters['stitch_projections'] = False
        self.reslice_checkbox.setChecked(True)
        self.parameters['reslice'] = True
        self.equalize_intensity_rButton.setChecked(True)
        self.parameters['equalize_intensity'] = True
        self.concatenate_rButton.setChecked(False)
        self.parameters['concatenate'] = False
        self.parameters['images_to_stitch'] = "0,2000,1"
        self.which_images_to_stitch_entry.setText("0,2000,1")
        self.dry_run_checkbox.setChecked(False)
        self.parameters['dry_run'] = False

    def update_parameters(self, new_parameters):
        logging.debug("Update parameters")
        # Update parameters dictionary (which is passed to auto_stitch_funcs)
        self.parameters = new_parameters
        # Update displayed parameters for GUI
        self.projections_input_entry.setText(self.parameters['projections_input_dir'])
        self.recon_slices_input_entry.setText(self.parameters['recon_slices_input_dir'])
        self.output_entry.setText(self.parameters['output_dir'])
        self.temp_entry.setText(self.parameters['temp_dir'])
        self.flats_darks_group.setChecked(bool(self.parameters['common_flats_darks']))
        self.flats_entry.setText(self.parameters['flats_dir'])
        self.darks_entry.setText(self.parameters['darks_dir'])
        self.sample_moved_down_checkbox.setChecked(bool(self.parameters['sample_moved_down']))
        self.overlap_region_entry.setText(self.parameters['overlap_region'])
        if self.parameters['stitch_reconstructed_slices']:
            self.reslice_checkbox.setEnabled(True)
            self.recon_slices_input_entry.setEnabled(True)
            self.recon_slices_input_button.setEnabled(True)
        self.stitch_reconstructed_slices_rButton.setChecked(bool(self.parameters['stitch_reconstructed_slices']))
        self.stitch_projections_rButton.setChecked(bool(self.parameters['stitch_projections']))
        self.reslice_checkbox.setChecked(bool(self.parameters['reslice']))
        self.which_images_to_stitch_entry.setText(self.parameters['images_to_stitch'])
        self.equalize_intensity_rButton.setChecked(bool(self.parameters['equalize_intensity']))
        self.concatenate_rButton.setChecked(bool(self.parameters['concatenate']))
        self.dry_run_checkbox.setChecked(bool(self.parameters['dry_run']))

    def projections_input_button_pressed(self):
        logging.debug("Projections Input Button Pressed")
        dir_explore = QFileDialog(self)
        projections_input_dir = dir_explore.getExistingDirectory(directory="/")
        self.projections_input_entry.setText(projections_input_dir)
        self.parameters['projections_input_dir'] = projections_input_dir

    def set_projections_input_entry(self):
        logging.debug("Projections Input Entry: " + str(self.projections_input_entry.text()))
        self.parameters['projections_input_dir'] = str(self.projections_input_entry.text())

    def recon_slices_input_button_pressed(self):
        logging.debug("Reconstructed Slices Input Button Pressed")
        dir_explore = QFileDialog(self)
        recon_slices_input_dir = dir_explore.getExistingDirectory(directory="/")
        self.recon_slices_input_entry.setText(recon_slices_input_dir)
        self.parameters['recon_slices_input_dir'] = recon_slices_input_dir

    def set_recon_slices_input_entry(self):
        logging.debug("Reconstructed Slices Input Entry: " + str(self.recon_slices_input_entry.text()))
        self.parameters['recon_slices_input_dir'] = str(self.recon_slices_input_entry.text())

    def output_button_pressed(self):
        logging.debug("Output Button Pressed")
        dir_explore = QFileDialog(self)
        output_dir = dir_explore.getExistingDirectory(directory="/")
        self.output_entry.setText(output_dir)
        self.parameters['output_dir'] = output_dir

    def set_output_entry(self):
        logging.debug("Output Entry: " + str(self.output_entry.text()))
        self.parameters['output_dir'] = str(self.output_entry.text())

    def temp_button_pressed(self):
        logging.debug("Temp Button Pressed")
        dir_explore = QFileDialog(self)
        temp_dir = dir_explore.getExistingDirectory(directory="/")
        self.temp_entry.setText(temp_dir)
        self.parameters['temp_dir'] = temp_dir

    def set_temp_entry(self):
        logging.debug("Temp Entry: " + str(self.temp_entry.text()))
        self.parameters['temp_dir'] = str(self.temp_entry.text())

    def set_flats_darks_group(self):
        logging.debug("Use Common Flats/Darks: " + str(self.flats_darks_group.isChecked()))
        if self.parameters['common_flats_darks'] is True:
            self.parameters['common_flats_darks'] = False
        else:
            self.parameters['common_flats_darks'] = True

    def flats_button_pressed(self):
        logging.debug("Flats Button Pressed")
        dir_explore = QFileDialog(self)
        flats_dir = dir_explore.getExistingDirectory()
        self.flats_entry.setText(flats_dir)
        self.parameters['flats_dir'] = flats_dir

    def set_flats_entry(self):
        logging.debug("Flats Entry: " + str(self.flats_entry.text()))
        self.parameters['flats_dir'] = str(self.flats_entry.text())

    def darks_button_pressed(self):
        logging.debug("Darks Button Pressed")
        dir_explore = QFileDialog(self)
        darks_dir = dir_explore.getExistingDirectory()
        self.darks_entry.setText(darks_dir)
        self.parameters['darks_dir'] = darks_dir

    def set_darks_entry(self):
        logging.debug("Darks Entry: " + str(self.darks_entry.text()))
        self.parameters['darks_dir'] = str(self.darks_entry.text())

    def set_overlap_region_entry(self):
        logging.debug("Overlap Region: " + str(self.overlap_region_entry.text()))
        self.parameters['overlap_region'] = str(self.overlap_region_entry.text())

    def set_sample_moved_down_checkbox(self):
        logging.debug("Sample was moved down: " + str(self.sample_moved_down_checkbox.isChecked()))
        self.parameters['sample_moved_down'] = self.sample_moved_down_checkbox.isChecked()

    def stitch_reconstructed_slices_rButton_clicked(self):
        logging.debug("Stitch Reconstructed Slices: " + str(self.stitch_reconstructed_slices_rButton.isChecked()))
        self.parameters['stitch_reconstructed_slices'] = self.stitch_reconstructed_slices_rButton.isChecked()
        self.parameters['stitch_projections'] = self.stitch_projections_rButton.isChecked()
        if self.stitch_reconstructed_slices_rButton.isChecked():
            self.recon_slices_input_button.setEnabled(True)
            self.recon_slices_input_entry.setEnabled(True)
            self.reslice_checkbox.setEnabled(True)
            self.reslice_checkbox.setChecked(True)
            self.parameters['reslice'] = True

    def stitch_projections_rButton_clicked(self):
        logging.debug("Stitch Projections: " + str(self.stitch_projections_rButton.isChecked()))
        self.parameters['stitch_projections'] = self.stitch_projections_rButton.isChecked()
        self.parameters['stitch_reconstructed_slices'] = self.stitch_reconstructed_slices_rButton.isChecked()
        if self.stitch_projections_rButton.isChecked():
            self.recon_slices_input_button.setDisabled(True)
            self.recon_slices_input_entry.setDisabled(True)
            self.reslice_checkbox.setDisabled(True)
            self.reslice_checkbox.setChecked(False)
            self.parameters['reslice'] = False

    def equalize_intensity_rButton_clicked(self):
        logging.debug("Equalize Intensity: " + str(self.equalize_intensity_rButton.isChecked()))
        self.parameters['equalize_intensity'] = self.equalize_intensity_rButton.isChecked()
        self.parameters['concatenate'] = self.concatenate_rButton.isChecked()

    def concatenate_rButton_clicked(self):
        logging.debug("Concatenate: " + str(self.concatenate_rButton.isChecked()))
        self.parameters['concatenate'] = self.concatenate_rButton.isChecked()
        self.parameters['equalize_intensity'] = self.equalize_intensity_rButton.isChecked()

    def set_reslice_checkbox(self):
        logging.debug("Reslice: " + str(self.reslice_checkbox.isChecked()))
        self.parameters['reslice'] = self.reslice_checkbox.isChecked()

    def set_which_images_to_stitch(self):
        logging.debug("Which images to be stitched: " + str(self.which_images_to_stitch_entry.text()))
        self.parameters['images_to_stitch'] = self.which_images_to_stitch_entry.text()

    def save_params_button_clicked(self):
        logging.debug("Save params button clicked")
        dir_explore = QFileDialog(self)
        params_file_path = dir_explore.getSaveFileName(filter="*.yaml", directory="/")
        # TODO: Only create output file is user selects valid params file
        garbage, file_name = os.path.split(params_file_path[0])
        file_extension = os.path.splitext(file_name)
        # If the user doesn't enter the .yaml extension then append it to filepath
        if file_extension[-1] == "":
            file_path = params_file_path[0] + ".yaml"
        else:
            file_path = params_file_path[0]
        try:
            file_out = open(file_path, 'w')
            yaml.dump(self.parameters, file_out)
            print("Parameters file saved at: " + str(file_path))
        except FileNotFoundError:
            print("You need to select a directory and use a valid file name")

    def import_params_button_clicked(self):
        logging.debug("Import params button clicked")
        dir_explore = QFileDialog(self)
        params_file_path = dir_explore.getOpenFileName(filter="*.yaml", directory="/")
        try:
            file_in = open(params_file_path[0], 'r')
            new_parameters = yaml.load(file_in, Loader=yaml.FullLoader)
            self.update_parameters(new_parameters)
            print("Parameters file loaded from: " + str(params_file_path[0]))
        except FileNotFoundError:
            print("You need to select a valid input file")

    def help_button_pressed(self):
        logging.debug("Help Button Pressed")
        h = "This tool is used to vertically stitch together overlapping images acquired" \
            " from parallel-beam CT, moving the sample stage vertically up or down between scans " \
            "of the rotated sample.\n\n"
        h += "We assume an input directory structure of at least one or more 'CT' directories." \
             " Each CT directory will contain two or more z-view directories;" \
             " z-directories are sets of images acquired through horizontal sample rotation" \
             ", they vertically overlap with subsequent z-directories of the same parent CT-directory.\n\n"
        h += "The program assumes that the images in each z-directory, within a parent CT-directory," \
             " have the same overlap. The overlap is determined by FFT correlation " \
             "and edge-detection of corresponding images " \
             "from the middle two z-directories. \n\n" #add info about flat-field-correction
        h += "'The Overlapping Pixels' value should be around twice what they think the overlap is.\n\n"
        h += "Default behaviour assumes that each z-view is higher than the previous." \
             " If each z-view is lower than the previous then select 'Was the sample moved down during experiment'\n\n"
        h += "The program can vertically stitch either tomogram projections or reconstructed slices:\n"\
             "Projections are used to find the overlap so the 'Select Projections Input Path'" \
             " must always point to a directory containing CT-directories." \
             " To stitch projections select the 'Stitch Projections' button.\n"
        h += "Reconstructed Slices can be stitched by selecting the 'Stitch Reconstructed Slices' button." \
             " The 'Select Reconstructed Slices Input Path' must be given a path to a directory" \
             " with the same structure as the 'Select Projections Input Path' where each z-directory contains" \
             " a single 'sli' subdirectory instead of 'tomo' and the optional 'flats', 'darks', 'flats2'" \
             " subdirectories.\n\n"
        h += "There are two methods for stitching images:\n"
        h += "'Equalize Intensity' will smoothly blend the overlapping images (like a crossfade).\n"
        h += "''Concatenate' simply appends one image to the other.\n\n"
        h += "Parameters can be saved to and loaded from .yaml files using the 'Save Parameters' and" \
             " 'Import Parameters' buttons.\n"
        h += "The 'Dry Run' checkbox makes the program find the pixel overlap for the projections input path" \
             " but does not stitch images. This is useful for finding the correct settings.\n"
        h += "Before running a stitch the program check that the output directory doesn't exist." \
             " This is to reduce the chance of accidentally overwriting data." \
             "The 'Delete Output Directory' button allows for the deletion of the output directory."
        QMessageBox.information(self, "Help", h)

    def delete_button_pressed(self):
        logging.debug("Delete Output Directory Button Pressed")
        delete_dialog = QMessageBox.question(self, 'Quit', 'Are you sure you want to delete the output directory?',
                                             QMessageBox.Yes | QMessageBox.No)
        if delete_dialog == QMessageBox.Yes:
            try:
                print("Deleting: " + self.parameters['output_dir'] + " ...")
                shutil.rmtree(self.parameters['output_dir'])
                print("Deleted directory: " + self.parameters['output_dir'])
            except FileNotFoundError:
                print("Directory does not exist: " + self.parameters['output_dir'])

    def stitch_button_pressed(self):
        logging.debug("Stitch Button Pressed")
        if self.parameters['temp_dir'] == "...enter temporary directory":
            print("Please enter a valid temporary directory")
            return
        self.auto_vertical_stitch_funcs = AutoVerticalStitchFunctions(self.parameters)
        self.auto_vertical_stitch_funcs.run_vertical_auto_stitch()

    def set_dry_run_checkbox(self):
        logging.debug("Dry Run Checkbox: " + str(self.dry_run_checkbox.isChecked()))
        self.parameters['dry_run'] = self.dry_run_checkbox.isChecked()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AutoVerticalStitchGUI()
    sys.exit(app.exec_())

