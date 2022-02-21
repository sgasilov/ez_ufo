from PyQt5.QtWidgets import QGroupBox, QPushButton, QCheckBox, QLabel, QLineEdit, QGridLayout, QFileDialog, QMessageBox
import logging
import os
import getpass
import yaml
from ez_ufo_qt.Helpers.stitch_funcs import main_360_mp_depth2


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
        self.axis_bottom_label.setText("Bottom Axis of Rotation (z00):")

        self.axis_bottom_entry = QLineEdit()
        self.axis_bottom_entry.textChanged.connect(self.set_axis_bottom)

        self.axis_top_label = QLabel("Top Axis of Rotation (z0N):")

        self.axis_group = QGroupBox("Enter axis of rotation manually")
        self.axis_group.clicked.connect(self.set_axis_group)

        self.axis_top_entry = QLineEdit()
        self.axis_top_entry.textChanged.connect(self.set_axis_top)

        self.axis_z00_label = QLabel("Axis of Rotation (z00):")
        self.axis_z00_entry = QLineEdit()
        self.axis_z00_entry.textChanged.connect(self.set_z00)

        self.axis_z01_label = QLabel("Axis of Rotation (z01):")
        self.axis_z01_entry = QLineEdit()
        self.axis_z01_entry.textChanged.connect(self.set_z01)

        self.axis_z02_label = QLabel("Axis of Rotation (z02):")
        self.axis_z02_entry = QLineEdit()
        self.axis_z02_entry.textChanged.connect(self.set_z02)

        self.axis_z03_label = QLabel("Axis of Rotation (z03):")
        self.axis_z03_entry = QLineEdit()
        self.axis_z03_entry.textChanged.connect(self.set_z03)

        self.axis_z04_label = QLabel("Axis of Rotation (z04):")
        self.axis_z04_entry = QLineEdit()
        self.axis_z04_entry.textChanged.connect(self.set_z04)

        self.axis_z05_label = QLabel("Axis of Rotation (z05):")
        self.axis_z05_entry = QLineEdit()
        self.axis_z05_entry.textChanged.connect(self.set_z05)

        self.axis_z06_label = QLabel("Axis of Rotation (z06):")
        self.axis_z06_entry = QLineEdit()
        self.axis_z06_entry.textChanged.connect(self.set_z06)

        self.axis_z07_label = QLabel("Axis of Rotation (z07):")
        self.axis_z07_entry = QLineEdit()
        self.axis_z07_entry.textChanged.connect(self.set_z07)

        self.axis_z08_label = QLabel("Axis of Rotation (z08):")
        self.axis_z08_entry = QLineEdit()
        self.axis_z08_entry.textChanged.connect(self.set_z08)

        self.axis_z09_label = QLabel("Axis of Rotation (z09):")
        self.axis_z09_entry = QLineEdit()
        self.axis_z09_entry.textChanged.connect(self.set_z09)

        self.axis_z010_label = QLabel("Axis of Rotation (z010):")
        self.axis_z010_entry = QLineEdit()
        self.axis_z010_entry.textChanged.connect(self.set_z010)

        self.axis_z011_label = QLabel("Axis of Rotation (z011):")
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

        axis_layout.addWidget(self.axis_z00_label, 0, 0)
        axis_layout.addWidget(self.axis_z00_entry, 0, 1)
        axis_layout.addWidget(self.axis_z06_label, 0, 2)
        axis_layout.addWidget(self.axis_z06_entry, 0, 3)

        axis_layout.addWidget(self.axis_z01_label, 1, 0)
        axis_layout.addWidget(self.axis_z01_entry, 1, 1)
        axis_layout.addWidget(self.axis_z07_label, 1, 2)
        axis_layout.addWidget(self.axis_z07_entry, 1, 3)

        axis_layout.addWidget(self.axis_z02_label, 2, 0)
        axis_layout.addWidget(self.axis_z02_entry, 2, 1)
        axis_layout.addWidget(self.axis_z08_label, 2, 2)
        axis_layout.addWidget(self.axis_z08_entry, 2, 3)

        axis_layout.addWidget(self.axis_z03_label, 3, 0)
        axis_layout.addWidget(self.axis_z03_entry, 3, 1)
        axis_layout.addWidget(self.axis_z09_label, 3, 2)
        axis_layout.addWidget(self.axis_z09_entry, 3, 3)

        axis_layout.addWidget(self.axis_z04_label, 4, 0)
        axis_layout.addWidget(self.axis_z04_entry, 4, 1)
        axis_layout.addWidget(self.axis_z010_label, 4, 2)
        axis_layout.addWidget(self.axis_z010_entry, 4, 3)

        axis_layout.addWidget(self.axis_z05_label, 5, 0)
        axis_layout.addWidget(self.axis_z05_entry, 5, 1)
        axis_layout.addWidget(self.axis_z011_label, 5, 2)
        axis_layout.addWidget(self.axis_z011_entry, 5, 3)
        self.axis_group.setLayout(axis_layout)

        self.axis_group.setTabOrder(self.axis_z00_entry, self.axis_z01_entry)
        self.axis_group.setTabOrder(self.axis_z01_entry, self.axis_z02_entry)
        self.axis_group.setTabOrder(self.axis_z02_entry, self.axis_z03_entry)
        self.axis_group.setTabOrder(self.axis_z03_entry, self.axis_z04_entry)
        self.axis_group.setTabOrder(self.axis_z04_entry, self.axis_z05_entry)
        self.axis_group.setTabOrder(self.axis_z05_entry, self.axis_z06_entry)
        self.axis_group.setTabOrder(self.axis_z06_entry, self.axis_z07_entry)
        self.axis_group.setTabOrder(self.axis_z07_entry, self.axis_z08_entry)
        self.axis_group.setTabOrder(self.axis_z08_entry, self.axis_z09_entry)
        self.axis_group.setTabOrder(self.axis_z09_entry, self.axis_z010_entry)
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
        self.parameters['360multi_axis_dict'] = dict.fromkeys(['z00', 'z01', 'z02', 'z03', 'z04', 'z05',
                                                               'z06', 'z07', 'z08', 'z09', 'z010', 'z011'])

    def update_parameters(self, new_parameters):
        logging.debug("Update parameters")
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
        self.axis_z00_entry.setText(str(self.parameters['360multi_axis_dict']['z00']))
        self.axis_z01_entry.setText(str(self.parameters['360multi_axis_dict']['z01']))
        self.axis_z02_entry.setText(str(self.parameters['360multi_axis_dict']['z02']))
        self.axis_z03_entry.setText(str(self.parameters['360multi_axis_dict']['z03']))
        self.axis_z04_entry.setText(str(self.parameters['360multi_axis_dict']['z04']))
        self.axis_z05_entry.setText(str(self.parameters['360multi_axis_dict']['z05']))
        self.axis_z06_entry.setText(str(self.parameters['360multi_axis_dict']['z06']))
        self.axis_z07_entry.setText(str(self.parameters['360multi_axis_dict']['z07']))
        self.axis_z08_entry.setText(str(self.parameters['360multi_axis_dict']['z08']))
        self.axis_z09_entry.setText(str(self.parameters['360multi_axis_dict']['z09']))
        self.axis_z010_entry.setText(str(self.parameters['360multi_axis_dict']['z010']))
        self.axis_z011_entry.setText(str(self.parameters['360multi_axis_dict']['z011']))

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

    def set_z00(self):
        logging.debug("z00 axis: " + str(self.axis_z00_entry.text()))
        self.parameters['360multi_axis_dict']['z00'] = str(self.axis_z00_entry.text())

    def set_z01(self):
        logging.debug("z01 axis: " + str(self.axis_z01_entry.text()))
        self.parameters['360multi_axis_dict']['z01'] = str(self.axis_z01_entry.text())

    def set_z02(self):
        logging.debug("z02 axis: " + str(self.axis_z02_entry.text()))
        self.parameters['360multi_axis_dict']['z02'] = str(self.axis_z02_entry.text())

    def set_z03(self):
        logging.debug("z03 axis: " + str(self.axis_z03_entry.text()))
        self.parameters['360multi_axis_dict']['z03'] = str(self.axis_z03_entry.text())

    def set_z04(self):
        logging.debug("z04 axis: " + str(self.axis_z04_entry.text()))
        self.parameters['360multi_axis_dict']['z04'] = str(self.axis_z04_entry.text())

    def set_z05(self):
        logging.debug("z05 axis: " + str(self.axis_z05_entry.text()))
        self.parameters['360multi_axis_dict']['z05'] = str(self.axis_z05_entry.text())

    def set_z06(self):
        logging.debug("z06 axis: " + str(self.axis_z06_entry.text()))
        self.parameters['360multi_axis_dict']['z06'] = str(self.axis_z06_entry.text())

    def set_z07(self):
        logging.debug("z07 axis: " + str(self.axis_z07_entry.text()))
        self.parameters['360multi_axis_dict']['z07'] = str(self.axis_z07_entry.text())

    def set_z08(self):
        logging.debug("z08 axis: " + str(self.axis_z08_entry.text()))
        self.parameters['360multi_axis_dict']['z08'] = str(self.axis_z08_entry.text())

    def set_z09(self):
        logging.debug("z09 axis: " + str(self.axis_z09_entry.text()))
        self.parameters['360multi_axis_dict']['z09'] = str(self.axis_z09_entry.text())

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
        print("==== Waiting for Next Task ====")

    def delete_button_pressed(self):
        print("---- Deleting Data From Output Directory ----")
        logging.debug("Delete button pressed")
        if os.path.exists(self.e_output):
            os.system('rm -r {}'.format(self.e_output))
            print(" - Directory with reconstructed data was removed")

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
            self.update_parameters(new_parameters)
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

