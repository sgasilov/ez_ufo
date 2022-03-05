from PyQt5.QtWidgets import QGroupBox, QPushButton, QCheckBox, QLabel, QLineEdit, QGridLayout, QFileDialog, QMessageBox
import logging
import os
import getpass
import yaml
from ez_ufo_qt.Helpers.stitch_funcs import main_360_mp_depth2
# Params
import ez_ufo_qt.GUI.params_io as params_io

class MultiStitch360Group(QGroupBox):
    def __init__(self):
        super().__init__()

        self.setTitle("360 Multi Stitch")
        self.setStyleSheet('QGroupBox {color: red;}')

        self.input_dir_button = QPushButton("Select input directory")
        self.input_dir_button.clicked.connect(self.input_button_pressed)

        self.input_dir_entry = QLineEdit()
        self.input_dir_entry.textChanged.connect(self.set_input_entry)

        self.temp_dir_button = QPushButton("Select temporary directory - default value recommended")
        self.temp_dir_button.clicked.connect(self.temp_button_pressed)

        self.temp_dir_entry = QLineEdit()
        self.temp_dir_entry.textChanged.connect(self.set_temp_entry)

        self.output_dir_button = QPushButton("Directory to save stitched images")
        self.output_dir_button.clicked.connect(self.output_button_pressed)

        self.output_dir_entry = QLineEdit()
        self.output_dir_entry.textChanged.connect(self.set_output_entry)

        self.crop_checkbox = QCheckBox("Crop all projections to match the width of smallest stitched projection")
        self.crop_checkbox.clicked.connect(self.set_crop_projections_checkbox)

        self.axis_bottom_label = QLabel()
        self.axis_bottom_label.setText("Axis of Rotation (Dir 00):")

        self.axis_bottom_entry = QLineEdit()
        self.axis_bottom_entry.textChanged.connect(self.set_axis_bottom)

        self.axis_top_label = QLabel("Axis of Rotation (Dir 0N):")

        self.axis_group = QGroupBox("Enter axis of rotation manually")
        self.axis_group.clicked.connect(self.set_axis_group)

        self.axis_top_entry = QLineEdit()
        self.axis_top_entry.textChanged.connect(self.set_axis_top)

        self.axis_z000_label = QLabel("Axis of Rotation (Dir 00):")
        self.axis_z000_entry = QLineEdit()
        self.axis_z000_entry.textChanged.connect(self.set_z000)

        self.axis_z001_label = QLabel("Axis of Rotation (Dir 01):")
        self.axis_z001_entry = QLineEdit()
        self.axis_z001_entry.textChanged.connect(self.set_z001)

        self.axis_z002_label = QLabel("Axis of Rotation (Dir 02):")
        self.axis_z002_entry = QLineEdit()
        self.axis_z002_entry.textChanged.connect(self.set_z002)

        self.axis_z003_label = QLabel("Axis of Rotation (Dir 03):")
        self.axis_z003_entry = QLineEdit()
        self.axis_z003_entry.textChanged.connect(self.set_z003)

        self.axis_z004_label = QLabel("Axis of Rotation (Dir 04):")
        self.axis_z004_entry = QLineEdit()
        self.axis_z004_entry.textChanged.connect(self.set_z004)

        self.axis_z005_label = QLabel("Axis of Rotation (Dir 05):")
        self.axis_z005_entry = QLineEdit()
        self.axis_z005_entry.textChanged.connect(self.set_z005)

        self.axis_z006_label = QLabel("Axis of Rotation (Dir 06):")
        self.axis_z006_entry = QLineEdit()
        self.axis_z006_entry.textChanged.connect(self.set_z006)

        self.axis_z007_label = QLabel("Axis of Rotation (Dir 07):")
        self.axis_z007_entry = QLineEdit()
        self.axis_z007_entry.textChanged.connect(self.set_z007)

        self.axis_z008_label = QLabel("Axis of Rotation (Dir 08):")
        self.axis_z008_entry = QLineEdit()
        self.axis_z008_entry.textChanged.connect(self.set_z008)

        self.axis_z009_label = QLabel("Axis of Rotation (Dir 09):")
        self.axis_z009_entry = QLineEdit()
        self.axis_z009_entry.textChanged.connect(self.set_z009)

        self.axis_z010_label = QLabel("Axis of Rotation (Dir 10):")
        self.axis_z010_entry = QLineEdit()
        self.axis_z010_entry.textChanged.connect(self.set_z010)

        self.axis_z011_label = QLabel("Axis of Rotation (Dir 11):")
        self.axis_z011_entry = QLineEdit()
        self.axis_z011_entry.textChanged.connect(self.set_z011)

        self.stitch_button = QPushButton("Stitch")
        self.stitch_button.clicked.connect(self.stitch_button_pressed)
        self.stitch_button.setStyleSheet("color:royalblue;font-weight:bold")

        self.delete_button = QPushButton("Delete output dir")
        self.delete_button.clicked.connect(self.delete_button_pressed)

        self.help_button = QPushButton("Help")
        self.help_button.clicked.connect(self.help_button_pressed)

        self.import_parameters_button = QPushButton("Import Parameters from File")
        self.import_parameters_button.clicked.connect(self.import_parameters_button_pressed)

        self.save_parameters_button = QPushButton("Save Parameters to File")
        self.save_parameters_button.clicked.connect(self.save_parameters_button_pressed)

        self.set_layout()

    def set_layout(self):
        layout = QGridLayout()

        layout.addWidget(self.input_dir_button, 0, 0, 1, 4)
        layout.addWidget(self.input_dir_entry, 1, 0, 1, 4)
        layout.addWidget(self.temp_dir_button, 2, 0, 1, 4)
        layout.addWidget(self.temp_dir_entry, 3, 0, 1, 4)
        layout.addWidget(self.output_dir_button, 4, 0, 1, 4)
        layout.addWidget(self.output_dir_entry, 5, 0, 1, 4)
        layout.addWidget(self.crop_checkbox, 6, 0, 1, 4)

        layout.addWidget(self.axis_bottom_label, 7, 0)
        layout.addWidget(self.axis_bottom_entry, 7, 1)
        layout.addWidget(self.axis_top_label, 7, 2)
        layout.addWidget(self.axis_top_entry, 7, 3)

        self.axis_group.setCheckable(True)
        self.axis_group.setChecked(False)
        axis_layout = QGridLayout()

        axis_layout.addWidget(self.axis_z000_label, 0, 0)
        axis_layout.addWidget(self.axis_z000_entry, 0, 1)
        axis_layout.addWidget(self.axis_z006_label, 0, 2)
        axis_layout.addWidget(self.axis_z006_entry, 0, 3)

        axis_layout.addWidget(self.axis_z001_label, 1, 0)
        axis_layout.addWidget(self.axis_z001_entry, 1, 1)
        axis_layout.addWidget(self.axis_z007_label, 1, 2)
        axis_layout.addWidget(self.axis_z007_entry, 1, 3)

        axis_layout.addWidget(self.axis_z002_label, 2, 0)
        axis_layout.addWidget(self.axis_z002_entry, 2, 1)
        axis_layout.addWidget(self.axis_z008_label, 2, 2)
        axis_layout.addWidget(self.axis_z008_entry, 2, 3)

        axis_layout.addWidget(self.axis_z003_label, 3, 0)
        axis_layout.addWidget(self.axis_z003_entry, 3, 1)
        axis_layout.addWidget(self.axis_z009_label, 3, 2)
        axis_layout.addWidget(self.axis_z009_entry, 3, 3)

        axis_layout.addWidget(self.axis_z004_label, 4, 0)
        axis_layout.addWidget(self.axis_z004_entry, 4, 1)
        axis_layout.addWidget(self.axis_z010_label, 4, 2)
        axis_layout.addWidget(self.axis_z010_entry, 4, 3)

        axis_layout.addWidget(self.axis_z005_label, 5, 0)
        axis_layout.addWidget(self.axis_z005_entry, 5, 1)
        axis_layout.addWidget(self.axis_z011_label, 5, 2)
        axis_layout.addWidget(self.axis_z011_entry, 5, 3)
        self.axis_group.setLayout(axis_layout)

        self.axis_group.setTabOrder(self.axis_z000_entry, self.axis_z001_entry)
        self.axis_group.setTabOrder(self.axis_z001_entry, self.axis_z002_entry)
        self.axis_group.setTabOrder(self.axis_z002_entry, self.axis_z003_entry)
        self.axis_group.setTabOrder(self.axis_z003_entry, self.axis_z004_entry)
        self.axis_group.setTabOrder(self.axis_z004_entry, self.axis_z005_entry)
        self.axis_group.setTabOrder(self.axis_z005_entry, self.axis_z006_entry)
        self.axis_group.setTabOrder(self.axis_z006_entry, self.axis_z007_entry)
        self.axis_group.setTabOrder(self.axis_z007_entry, self.axis_z008_entry)
        self.axis_group.setTabOrder(self.axis_z008_entry, self.axis_z009_entry)
        self.axis_group.setTabOrder(self.axis_z009_entry, self.axis_z010_entry)
        self.axis_group.setTabOrder(self.axis_z010_entry, self.axis_z011_entry)

        layout.addWidget(self.axis_group, 8, 0, 1, 4)

        layout.addWidget(self.help_button, 9, 0)
        layout.addWidget(self.delete_button, 9, 1)
        layout.addWidget(self.stitch_button, 9, 2, 1, 2)

        layout.addWidget(self.import_parameters_button, 10, 0, 1, 2)
        layout.addWidget(self.save_parameters_button, 10, 2, 1, 2)

        self.setLayout(layout)

    def init_values(self):
        self.parameters = {'parameters_type': '360_multi_stitch'}
        self.parameters['360multi_input_dir'] = os.getcwd()
        self.input_dir_entry.setText(self.parameters['360multi_input_dir'])
        self.parameters['360multi_temp_dir'] = os.path.join("/data", "tmp-ezstitch-" + getpass.getuser())
        self.temp_dir_entry.setText(self.parameters['360multi_temp_dir'])
        self.parameters['360multi_output_dir'] = os.getcwd() + '-stitched'
        self.output_dir_entry.setText(self.parameters['360multi_output_dir'])
        self.parameters['360multi_crop_projections'] = True
        self.crop_checkbox.setChecked(self.parameters['360multi_crop_projections'])
        self.parameters['360multi_bottom_axis'] = 245
        self.axis_bottom_entry.setText(str(self.parameters['360multi_bottom_axis']))
        self.parameters['360multi_top_axis'] = 245
        self.axis_top_entry.setText(str(self.parameters['360multi_top_axis']))
        self.parameters['360multi_axis'] = self.parameters['360multi_bottom_axis']
        self.parameters['360multi_manual_axis'] = False
        self.parameters['360multi_axis_dict'] = dict.fromkeys(['z000', 'z001', 'z002', 'z003', 'z004', 'z005',
                                                               'z006', 'z007', 'z008', 'z009', 'z010', 'z011'])

    def update_parameters(self, new_parameters):
        logging.debug("Update parameters")
        if new_parameters['parameters_type'] != '360_multi_stitch':
            print("Error: Invalid parameter file type: " + str(new_parameters['parameters_type']))
            return -1
        # Update parameters dictionary (which is passed to auto_stitch_funcs)
        self.parameters = new_parameters
        # Update displayed parameters for GUI
        self.input_dir_entry.setText(self.parameters['360multi_input_dir'])
        self.temp_dir_entry.setText(self.parameters['360multi_temp_dir'])
        self.output_dir_entry.setText(self.parameters['360multi_output_dir'])
        self.crop_checkbox.setChecked(self.parameters['360multi_crop_projections'])
        self.axis_bottom_entry.setText(str(self.parameters['360multi_bottom_axis']))
        self.axis_top_entry.setText(str(self.parameters['360multi_top_axis']))
        self.axis_group.setChecked(bool(self.parameters['360multi_manual_axis']))
        self.axis_z000_entry.setText(str(self.parameters['360multi_axis_dict']['z000']))
        self.axis_z001_entry.setText(str(self.parameters['360multi_axis_dict']['z001']))
        self.axis_z002_entry.setText(str(self.parameters['360multi_axis_dict']['z002']))
        self.axis_z003_entry.setText(str(self.parameters['360multi_axis_dict']['z003']))
        self.axis_z004_entry.setText(str(self.parameters['360multi_axis_dict']['z004']))
        self.axis_z005_entry.setText(str(self.parameters['360multi_axis_dict']['z005']))
        self.axis_z006_entry.setText(str(self.parameters['360multi_axis_dict']['z006']))
        self.axis_z007_entry.setText(str(self.parameters['360multi_axis_dict']['z007']))
        self.axis_z008_entry.setText(str(self.parameters['360multi_axis_dict']['z008']))
        self.axis_z009_entry.setText(str(self.parameters['360multi_axis_dict']['z009']))
        self.axis_z010_entry.setText(str(self.parameters['360multi_axis_dict']['z010']))
        self.axis_z011_entry.setText(str(self.parameters['360multi_axis_dict']['z011']))
        return 0

    def input_button_pressed(self):
        logging.debug("Input button pressed")
        dir_explore = QFileDialog(self)
        self.parameters['360multi_input_dir'] = dir_explore.getExistingDirectory()
        self.input_dir_entry.setText(self.parameters['360multi_input_dir'])

    def set_input_entry(self):
        logging.debug("Input directory: " + str(self.input_dir_entry.text()))
        self.parameters['360multi_input_dir'] = str(self.input_dir_entry.text())

    def temp_button_pressed(self):
        logging.debug("Temp button pressed")
        dir_explore = QFileDialog(self)
        self.parameters['360multi_temp_dir'] = dir_explore.getExistingDirectory()
        self.temp_dir_entry.setText(self.parameters['360multi_temp_dir'])

    def set_temp_entry(self):
        logging.debug("Temp directory: " + str(self.temp_dir_entry.text()))
        self.parameters['360multi_temp_dir'] = str(self.temp_dir_entry.text())

    def output_button_pressed(self):
        logging.debug("Output button pressed")
        dir_explore = QFileDialog(self)
        self.parameters['360multi_output_dir'] = dir_explore.getExistingDirectory()
        self.output_dir_entry.setText(self.parameters['360multi_output_dir'])

    def set_output_entry(self):
        logging.debug("Output directory: " + str(self.output_dir_entry.text()))
        self.parameters['360multi_output_dir'] = str(self.output_dir_entry.text())

    def set_crop_projections_checkbox(self):
        logging.debug("Crop projections: " + str(self.crop_checkbox.isChecked()))
        self.parameters['360multi_crop_projections'] = bool(self.crop_checkbox.isChecked())

    def set_axis_bottom(self):
        logging.debug("Axis Bottom : " + str(self.axis_bottom_entry.text()))
        self.parameters['360multi_bottom_axis'] = int(self.axis_bottom_entry.text())

    def set_axis_top(self):
        logging.debug("Axis Top: " + str(self.axis_top_entry.text()))
        self.parameters['360multi_top_axis'] = int(self.axis_top_entry.text())

    def set_axis_group(self):
        if self.axis_group.isChecked():
            self.axis_bottom_label.setEnabled(False)
            self.axis_bottom_entry.setEnabled(False)
            self.axis_top_label.setEnabled(False)
            self.axis_top_entry.setEnabled(False)
            self.parameters['360multi_manual_axis'] = True
            logging.debug("Enter axis of rotation manually: " + str(self.parameters['360multi_manual_axis']))
        else:
            self.axis_bottom_label.setEnabled(True)
            self.axis_bottom_entry.setEnabled(True)
            self.axis_top_label.setEnabled(True)
            self.axis_top_entry.setEnabled(True)
            self.parameters['360multi_manual_axis'] = False
            logging.debug("Enter axis of rotation manually: " + str(self.parameters['360multi_manual_axis']))

    def set_z000(self):
        logging.debug("z000 axis: " + str(self.axis_z000_entry.text()))
        self.parameters['360multi_axis_dict']['z000'] = str(self.axis_z000_entry.text())

    def set_z001(self):
        logging.debug("z001 axis: " + str(self.axis_z001_entry.text()))
        self.parameters['360multi_axis_dict']['z001'] = str(self.axis_z001_entry.text())

    def set_z002(self):
        logging.debug("z002 axis: " + str(self.axis_z002_entry.text()))
        self.parameters['360multi_axis_dict']['z002'] = str(self.axis_z002_entry.text())

    def set_z003(self):
        logging.debug("z003 axis: " + str(self.axis_z003_entry.text()))
        self.parameters['360multi_axis_dict']['z003'] = str(self.axis_z003_entry.text())

    def set_z004(self):
        logging.debug("z004 axis: " + str(self.axis_z004_entry.text()))
        self.parameters['360multi_axis_dict']['z004'] = str(self.axis_z004_entry.text())

    def set_z005(self):
        logging.debug("z005 axis: " + str(self.axis_z005_entry.text()))
        self.parameters['360multi_axis_dict']['z005'] = str(self.axis_z005_entry.text())

    def set_z006(self):
        logging.debug("z006 axis: " + str(self.axis_z006_entry.text()))
        self.parameters['360multi_axis_dict']['z006'] = str(self.axis_z006_entry.text())

    def set_z007(self):
        logging.debug("z007 axis: " + str(self.axis_z007_entry.text()))
        self.parameters['360multi_axis_dict']['z007'] = str(self.axis_z007_entry.text())

    def set_z008(self):
        logging.debug("z008 axis: " + str(self.axis_z008_entry.text()))
        self.parameters['360multi_axis_dict']['z008'] = str(self.axis_z008_entry.text())

    def set_z009(self):
        logging.debug("z009 axis: " + str(self.axis_z009_entry.text()))
        self.parameters['360multi_axis_dict']['z009'] = str(self.axis_z009_entry.text())

    def set_z010(self):
        logging.debug("z010 axis: " + str(self.axis_z010_entry.text()))
        self.parameters['360multi_axis_dict']['z010'] = str(self.axis_z010_entry.text())

    def set_z011(self):
        logging.debug("z011 axis: " + str(self.axis_z011_entry.text()))
        self.parameters['360multi_axis_dict']['z011'] = str(self.axis_z011_entry.text())

    def stitch_button_pressed(self):
        logging.debug("Stitch button pressed")
        if os.path.exists(self.parameters['360multi_temp_dir']):
            os.system('rm -r {}'.format(self.parameters['360multi_temp_dir']))

        if os.path.exists(self.parameters['360multi_output_dir']):
            # raise ValueError('Output directory exists')
            print("Output directory exists - delete before stitching")

        print("======= Begin 360 Multi-Stitch =======")
        main_360_mp_depth2(self.parameters)
        params_io.save_parameters(self.parameters, self.parameters['360multi_output_dir'])
        print("==== Waiting for Next Task ====")

    def delete_button_pressed(self):
        print("---- Deleting Data From Output Directory ----")
        logging.debug("Delete button pressed")
        if os.path.exists(self.parameters['360multi_output_dir']):
            os.system('rm -r {}'.format(self.parameters['360multi_output_dir']))
            print(" - Directory with stitched data was removed")

    def help_button_pressed(self):
        logging.debug("Help button pressed")
        h = "Stitches images horizontally\n"
        h += "Directory structure is, f.i., Input/000, Input/001,...Input/00N\n"
        h += "Each 000, 001, ... 00N directory must have identical subdirectory \"Type\"\n"
        h += "Selected range of images from \"Type\" directory will be stitched vertically\n"
        h += "across all subdirectories in the Input directory"
        h += "to be added as options:\n"
        h += "(1) orthogonal reslicing, (2) interpolation, (3) horizontal stitching"
        QMessageBox.information(self, "Help", h)

    def import_parameters_button_pressed(self):
        logging.debug("Import params button clicked")
        dir_explore = QFileDialog(self)
        params_file_path = dir_explore.getOpenFileName(filter="*.yaml")
        try:
            file_in = open(params_file_path[0], 'r')
            new_parameters = yaml.load(file_in, Loader=yaml.FullLoader)
            if self.update_parameters(new_parameters) == 0:
                print("Parameters file loaded from: " + str(params_file_path[0]))
        except FileNotFoundError:
            print("You need to select a valid input file")

    def save_parameters_button_pressed(self):
        logging.debug("Save params button clicked")
        dir_explore = QFileDialog(self)
        params_file_path = dir_explore.getSaveFileName(filter="*.yaml")
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

