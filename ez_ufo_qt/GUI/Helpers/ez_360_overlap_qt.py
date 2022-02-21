from PyQt5.QtWidgets import QGroupBox, QPushButton, QCheckBox, QLabel, QLineEdit, QGridLayout, QFileDialog, QMessageBox
import logging
import os
import yaml
from ez_ufo_qt.Helpers.find_360_overlap import find_overlap

class Overlap360Group(QGroupBox):
    def __init__(self):
        super().__init__()

        self.setTitle("Find 360 Overlap")
        self.setStyleSheet('QGroupBox {color: Orange;}')

        self.input_dir_button = QPushButton("Select input directory")
        self.input_dir_button.clicked.connect(self.input_button_pressed)
        self.input_dir_entry = QLineEdit()
        self.input_dir_entry.textChanged.connect(self.set_input_entry)

        self.temp_dir_button = QPushButton("Select temp directory")
        self.temp_dir_button.clicked.connect(self.temp_button_pressed)
        self.temp_dir_entry = QLineEdit()
        self.temp_dir_entry.textChanged.connect(self.set_temp_entry)

        self.output_dir_button = QPushButton("Select output directory")
        self.output_dir_button.clicked.connect(self.output_button_pressed)
        self.output_dir_entry = QLineEdit()
        self.output_dir_entry.textChanged.connect(self.set_output_entry)

        self.pixel_row_label = QLabel("Pixel row to be used for sinogram")
        self.pixel_row_entry = QLineEdit()
        self.pixel_row_entry.textChanged.connect(self.set_pixel_row)

        self.min_label = QLabel("Lower limit of stitch/axis search range")
        self.min_entry = QLineEdit()
        self.min_entry.textChanged.connect(self.set_lower_limit)

        self.max_label = QLabel("Upper limit of stitch/axis search range")
        self.max_entry = QLineEdit()
        self.max_entry.textChanged.connect(self.set_upper_limit)

        self.step_label = QLabel("Value by which to increment through search range")
        self.step_entry = QLineEdit()
        self.step_entry.textChanged.connect(self.set_increment)

        self.axis_on_left = QCheckBox("Is the rotation axis on the left-hand side of the image?")
        self.axis_on_left.stateChanged.connect(self.set_axis_checkbox)

        self.help_button = QPushButton("Help")
        self.help_button.clicked.connect(self.help_button_pressed)

        self.find_overlap_button = QPushButton("Find Overlap")
        self.find_overlap_button.clicked.connect(self.overlap_button_pressed)
        self.find_overlap_button.setStyleSheet("color:royalblue;font-weight:bold")

        self.import_parameters_button = QPushButton("Import Parameters from File")
        self.import_parameters_button.clicked.connect(self.import_parameters_button_pressed)

        self.save_parameters_button = QPushButton("Save Parameters to File")
        self.save_parameters_button.clicked.connect(self.save_parameters_button_pressed)

        self.set_layout()

    def set_layout(self):
        layout = QGridLayout()
        layout.addWidget(self.input_dir_button, 0, 0, 1, 2)
        layout.addWidget(self.input_dir_entry, 1, 0, 1, 2)
        layout.addWidget(self.temp_dir_button, 2, 0, 1, 2)
        layout.addWidget(self.temp_dir_entry, 3, 0, 1, 2)
        layout.addWidget(self.output_dir_button, 4, 0, 1, 2)
        layout.addWidget(self.output_dir_entry, 5, 0, 1, 2)
        layout.addWidget(self.pixel_row_label, 6, 0)
        layout.addWidget(self.pixel_row_entry, 6, 1)
        layout.addWidget(self.min_label, 7, 0)
        layout.addWidget(self.min_entry, 7, 1)
        layout.addWidget(self.max_label, 8, 0)
        layout.addWidget(self.max_entry, 8, 1)
        layout.addWidget(self.step_label, 9, 0)
        layout.addWidget(self.step_entry, 9, 1)
        layout.addWidget(self.axis_on_left, 10, 0)
        layout.addWidget(self.help_button, 11, 0)
        layout.addWidget(self.find_overlap_button, 11, 1)
        layout.addWidget(self.import_parameters_button, 12, 0)
        layout.addWidget(self.save_parameters_button, 12, 1)
        self.setLayout(layout)

    def init_values(self):
        self.parameters = {'parameters_type': '360_overlap'}
        self.parameters['360overlap_input_dir'] = os.getcwd()
        self.input_dir_entry.setText(self.parameters['360overlap_input_dir'])
        self.parameters['360overlap_temp_dir'] = "/data/tmp-stitch_search"
        self.temp_dir_entry.setText(self.parameters['360overlap_temp_dir'])
        self.parameters['360overlap_output_dir'] = os.getcwd() + '-overlap'
        self.output_dir_entry.setText(self.parameters['360overlap_output_dir'])
        self.parameters['360overlap_start_row'] = 200
        self.pixel_row_entry.setText(str(self.parameters['360overlap_start_row']))
        self.parameters['360overlap_lower_limit'] = 100
        self.min_entry.setText(str(self.parameters['360overlap_lower_limit']))
        self.parameters['360overlap_upper_limit'] = 200
        self.max_entry.setText(str(self.parameters['360overlap_upper_limit']))
        self.parameters['360overlap_increment'] = 2
        self.step_entry.setText(str(self.parameters['360overlap_increment']))
        self.parameters['360overlap_axis_on_left'] = True
        self.axis_on_left.setChecked(bool(self.parameters['360overlap_axis_on_left']))

    def update_parameters(self, new_parameters):
        logging.debug("Update parameters")
        # Update parameters dictionary (which is passed to auto_stitch_funcs)
        self.parameters = new_parameters
        # Update displayed parameters for GUI
        self.input_dir_entry.setText(self.parameters['360overlap_input_dir'])
        self.temp_dir_entry.setText(self.parameters['360overlap_temp_dir'])
        self.output_dir_entry.setText(self.parameters['360overlap_output_dir'])
        self.pixel_row_entry.setText(str(self.parameters['360overlap_start_row']))
        self.min_entry.setText(str(self.parameters['360overlap_lower_limit']))
        self.max_entry.setText(str(self.parameters['360overlap_upper_limit']))
        self.step_entry.setText(str(self.parameters['360overlap_increment']))
        self.axis_on_left.setChecked(bool(self.parameters['360overlap_axis_on_left']))

    def input_button_pressed(self):
        logging.debug("Select input button pressed")
        dir_explore = QFileDialog(self)
        self.parameters['360overlap_input_dir'] = dir_explore.getExistingDirectory()
        self.input_dir_entry.setText(self.parameters['360overlap_input_dir'])

    def set_input_entry(self):
        logging.debug("Input: " + str(self.input_dir_entry.text()))
        self.parameters['360overlap_input_dir'] = str(self.input_dir_entry.text())

    def temp_button_pressed(self):
        logging.debug("Select temp button pressed")
        dir_explore = QFileDialog(self)
        self.parameters['360overlap_temp_dir'] = dir_explore.getExistingDirectory()
        self.temp_dir_entry.setText(self.parameters['360overlap_temp_dir'])

    def set_temp_entry(self):
        logging.debug("Temp: " + str(self.temp_dir_entry.text()))
        self.parameters['360overlap_temp_dir'] = str(self.temp_dir_entry.text())

    def output_button_pressed(self):
        logging.debug("Select output button pressed")
        dir_explore = QFileDialog(self)
        self.parameters['360overlap_output_dir'] = dir_explore.getExistingDirectory()
        self.output_dir_entry.setText(self.parameters['360overlap_output_dir'])

    def set_output_entry(self):
        logging.debug("Output: " + str(self.output_dir_entry.text()))
        self.parameters['360overlap_output_dir'] = str(self.output_dir_entry.text())

    def set_pixel_row(self):
        logging.debug("Pixel row: " + str(self.pixel_row_entry.text()))
        self.parameters['360overlap_start_row'] = int(self.pixel_row_entry.text())

    def set_lower_limit(self):
        logging.debug("Lower limit: " + str(self.min_entry.text()))
        self.parameters['360overlap_lower_limit'] = int(self.min_entry.text())

    def set_upper_limit(self):
        logging.debug("Upper limit: " + str(self.max_entry.text()))
        self.parameters['360overlap_upper_limit'] = int(self.max_entry.text())

    def set_increment(self):
        logging.debug("Value of increment: " + str(self.step_entry.text()))
        self.parameters['360overlap_increment'] = int(self.step_entry.text())

    def set_axis_checkbox(self):
        logging.debug("Is rotation axis on left-hand-side?: " + str(self.axis_on_left.isChecked()))
        self.parameters['360overlap_axis_on_left'] = bool(self.axis_on_left.isChecked())

    def overlap_button_pressed(self):
        logging.debug("Find overlap button pressed")
        find_overlap(self.parameters)

    def help_button_pressed(self):
        logging.debug("Help button pressed")
        h = "This script takes as input a CT scan that has been collected in 'half-acquisition' mode"
        h += " and produces a series of reconstructed slices, each of which are generated by cropping and"
        h += " concatenating opposing projections together over a range of 'overlap' values (i.e. the pixel column"
        h += " at which the images are cropped and concatenated)."
        h += " The objective is to review this series of images to determine the pixel column at which the axis of rotation"
        h += " is located (much like the axis search function commonly used in reconstruction software)."
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
