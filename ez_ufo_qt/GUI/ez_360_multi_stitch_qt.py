import sys
from PyQt5.QtWidgets import QGroupBox, QPushButton, QCheckBox, QLabel, QLineEdit, QGridLayout, QWidget, QApplication, QVBoxLayout, QHBoxLayout
import logging
import os
import getpass

class MultiStitch360Group(QGroupBox):

    def __init__(self):
        super().__init__()

        self.e_input = ""
        self.e_output = ""
        self.e_tmpdir = ""
        self.e_ax1 = 0
        self.e_ax2 = 0
        self.e_ax = 0
        self.e_ax = 0

        self.setTitle("360 Multi Stitch")
        self.setStyleSheet('QGroupBox {color: red;}')

        self.input_dir_button = QPushButton()
        self.input_dir_button.setText("Select input directory with 000,001,...,00N subdirectories")
        self.input_dir_button.clicked.connect(self.input_button_pressed)

        self.input_dir_entry = QLineEdit()
        self.input_dir_entry.textChanged.connect(self.set_input_entry)

        self.temp_dir_button = QPushButton()
        self.temp_dir_button.setText("Select temporary directory - default value recommended")
        self.temp_dir_button.clicked.connect(self.temp_button_pressed)

        self.temp_dir_entry = QLineEdit()
        self.temp_dir_entry.textChanged.connect(self.set_temp_entry)

        self.output_dir_button = QPushButton()
        self.output_dir_button.setText("Directory to save stitched images")
        self.output_dir_button.clicked.connect(self.output_button_pressed)

        self.output_dir_entry = QLineEdit()
        self.output_dir_entry.textChanged.connect(self.set_output_entry)

        self.crop_checkbox = QCheckBox()
        self.crop_checkbox.setText("Crop all projections to match the width of smallest stitched projection")
        self.crop_checkbox.clicked.connect(self.set_crop_projections_checkbox)

        self.axis_bottom_label = QLabel()
        self.axis_bottom_label.setText("Axis of Rotation at bottom (z00):")

        self.axis_bottom_entry = QLineEdit()
        self.axis_bottom_entry.textChanged.connect(self.set_axis_bottom)

        self.axis_top_label = QLabel()
        self.axis_top_label.setText("Axis of Rotation at top (ignored if not multi-slice):")

        self.axis_top_entry = QLineEdit()
        self.axis_top_entry.textChanged.connect(self.set_axis_top)

        self.stitch_button = QPushButton()
        self.stitch_button.setText("Stitch")
        self.stitch_button.clicked.connect(self.stitch_button_pressed)

        self.delete_button = QPushButton()
        self.delete_button.setText("Delete")
        self.delete_button.clicked.connect(self.delete_button_pressed)

        self.help_button = QPushButton()
        self.help_button.setText("Help")
        self.help_button.clicked.connect(self.help_button_pressed)

        self.set_layout()

    def set_layout(self):
        layout = QGridLayout()

        vbox = QVBoxLayout()
        vbox.addWidget(self.input_dir_button)
        vbox.addWidget(self.input_dir_entry)
        vbox.addWidget(self.temp_dir_button)
        vbox.addWidget(self.temp_dir_entry)
        vbox.addWidget(self.output_dir_button)
        vbox.addWidget(self.output_dir_entry)
        layout.addItem(vbox, 0, 0)

        layout.addWidget(self.crop_checkbox, 1, 0)

        grid = QGridLayout()
        grid.addWidget(self.axis_bottom_label, 0, 0)
        grid.addWidget(self.axis_bottom_entry, 0, 1)
        grid.addWidget(self.axis_top_label, 1, 0)
        grid.addWidget(self.axis_top_entry, 1, 1)
        layout.addItem(grid)

        hbox = QHBoxLayout()
        hbox.addWidget(self.stitch_button)
        hbox.addWidget(self.delete_button)
        hbox.addWidget(self.help_button)
        layout.addItem(hbox, 4, 0)

        self.setLayout(layout)

    #TODO initialize actual parameter values
    def init_values(self):
        self.input_dir_entry.setText(os.getcwd())
        tmp = os.path.join("/data", "tmp-ezstitch-" + getpass.getuser())
        self.temp_dir_entry.setText(tmp)
        self.output_dir_entry.setText(os.getcwd() + '-stitched')
        self.crop_checkbox.setChecked(True)
        self.axis_bottom_entry.setText("245")
        self.axis_top_entry.setText("245")


    def input_button_pressed(self):
        logging.debug("Input button pressed")

    def set_input_entry(self):
        logging.debug("Input directory: " + str(self.input_dir_entry.text()))

    def temp_button_pressed(self):
        logging.debug("Temp button pressed")

    def set_temp_entry(self):
        logging.debug("Temp directory: " + str(self.temp_dir_entry.text()))

    def output_button_pressed(self):
        logging.debug("Output button pressed")

    def set_output_entry(self):
        logging.debug("Output directory: " + str(self.output_dir_entry.text()))

    def set_crop_projections_checkbox(self):
        logging.debug("Crop projections: " + str(self.crop_checkbox.isChecked()))

    def set_axis_bottom(self):
        logging.debug("Axis Bottom : " + str(self.axis_bottom_entry.text()))

    def set_axis_top(self):
        logging.debug("Axis Top: " + str(self.axis_top_entry.text()))

    def stitch_button_pressed(self):
        logging.debug("Stitch button pressed")

    def delete_button_pressed(self):
        logging.debug("Delete button pressed")

    def help_button_pressed(self):
        logging.debug("Help button pressed")

class tk_args():
    def __init__(self, e_input, e_output, e_tmpdir, e_ax1, e_ax2, e_ax, e_crop):

        self.args={}
        # directories
        self.args['input']=str(e_input)
        setattr(self,'input',self.args['input'])
        self.args['output']=str(e_output)
        setattr(self,'output',self.args['output'])
        self.args['tmpdir']=str(e_tmpdir)
        setattr(self,'tmpdir',self.args['tmpdir'])
        #hor stitch half acq mode
        self.args['ax1']=int(e_ax1)
        setattr(self,'ax1',self.args['ax1'])
        self.args['ax2']=int(e_ax2)
        setattr(self,'ax2',self.args['ax2'])
        self.args['ax']=int(e_ax)
        setattr(self,'ax',self.args['ax'])
        self.args['crop']=int(e_crop)
        setattr(self,'crop',self.args['crop'])