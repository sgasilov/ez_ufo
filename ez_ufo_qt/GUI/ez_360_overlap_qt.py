import sys
from PyQt5.QtWidgets import QGroupBox, QPushButton, QCheckBox, QLabel, QLineEdit, QGridLayout, QWidget, QApplication, QVBoxLayout, QHBoxLayout, QFileDialog, QMessageBox
import logging
import os
import getpass
from ez_ufo_qt.stitch_funcs import main_360_mp_depth2

class Overlap360Group(QGroupBox):
    def __init__(self):
        super().__init__()

        self.setTitle("Find 360 Overlap")
        self.setStyleSheet('QGroupBox {color: Orange;}')

        self.input_dir_button = QPushButton()
        self.input_dir_button.setText("Select input directory")

        self.input_dir_entry = QLineEdit()

        self.temp_dir_button = QPushButton()
        self.temp_dir_button.setText("Select temp directory")

        self.temp_dir_entry = QLineEdit()

        self.output_dir_button = QPushButton()
        self.output_dir_button.setText("Select output directory")

        self.output_dir_entry = QLineEdit()

        self.pixel_row_label = QLabel("Pixel row to be used for sinogram")
        self.pixel_row_entry = QLineEdit()

        self.min_label = QLabel("Lower limit of stitch/axis search range")
        self.min_entry = QLineEdit()

        self.max_label = QLabel("Upper limit of stitch/axis search range")
        self.max_entry = QLineEdit()

        self.step_label = QLabel("Value by which to increment through search range")
        self.step_entry = QLineEdit()

        self.axis_on_left = QCheckBox("Is the rotation axis on the left-hand side of the image?")

        self.find_overlap_button = QPushButton("Find Overlap")

        self.help_button = QPushButton("Help")

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
        layout.addWidget(self.find_overlap_button, 11, 0)
        layout.addWidget(self.help_button, 11, 1)

        self.setLayout(layout)

    def init_values(self):
        pass