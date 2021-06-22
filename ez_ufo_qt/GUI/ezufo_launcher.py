#!/usr/bin/env python3

import logging
import os
from PyQt5 import QtWidgets as qtw

from ez_ufo_qt.GUI.centre_of_rotation import CentreOfRotationGroup
from ez_ufo_qt.GUI.filters import FiltersGroup
from ez_ufo_qt.GUI.phase_retrieval import PhaseRetrievalGroup
from ez_ufo_qt.GUI.binning import BinningGroup
from ez_ufo_qt.GUI.config import ConfigGroup
from ez_ufo_qt.main import main_tk, clean_tmp_dirs
from ez_ufo_qt.GUI.yaml_in_out import Yaml_IO


class GUI(qtw.QWidget):
    """
    Creates main GUI
    """

    def __init__(self, *args, **kwargs):
        super(GUI, self).__init__(*args, **kwargs)
        self.setWindowTitle('EZ-UFO GUI')

        self.setStyleSheet("font: 10pt; font-family: Arial")

        # Setup logging for debugging
        logger = logging.getLogger()
        fhandler = logging.FileHandler(filename='mylog.log', mode='w')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fhandler.setFormatter(formatter)
        logger.addHandler(fhandler)
        logger.setLevel(logging.WARNING)

        # Dict which holds the value of parameters set by user in GUI interaction
        self.params = {}

        # Read in default parameter settings from yaml file
        settings_path = os.path.dirname(os.path.abspath(__file__)) + '/default_settings.yaml'
        self.yaml_io = Yaml_IO()
        self.yaml_data = self.yaml_io.read_yaml(settings_path)
        self.params = dict(self.yaml_data)

        # Create and setup classes for each section of GUI
        self.centre_of_rotation_group = CentreOfRotationGroup(self.params)
        self.filters_group = FiltersGroup(self.params)
        self.phase_retrieval_group = PhaseRetrievalGroup(self.params)
        self.binning_group = BinningGroup(self.params)
        self.config_group = ConfigGroup(self.params)

        self.set_layout()
        self.resize(0, 0) #window to minimum size

        self.config_group.signal_update_vals_from_params.connect(self.update_values_from_params)

        finish = qtw.QAction("Quit", self)
        finish.triggered.connect(self.closeEvent)

        self.show()

    def set_layout(self):
        main_layout = qtw.QGridLayout()

        main_layout.addWidget(self.centre_of_rotation_group, 0, 0)
        main_layout.addWidget(self.filters_group, 0, 1)
        main_layout.addWidget(self.phase_retrieval_group, 1, 0)
        main_layout.addWidget(self.binning_group, 1, 1)
        main_layout.addWidget(self.config_group, 2, 0, 2, 0)

        self.setLayout(main_layout)

    def update_values_from_params(self, params):
        print(params)
        self.centre_of_rotation_group.set_values_from_params(params)
        self.filters_group.set_values_from_params(params)
        self.phase_retrieval_group.set_values_from_params(params)
        self.binning_group.set_values_from_params(params)
        self.config_group.set_values_from_params(params)

    def closeEvent(self, event):
        logging.debug("QUIT")
        reply = qtw.QMessageBox.question(self, 'Quit', 'Are you sure you want to quit?',
        qtw.QMessageBox.Yes | qtw.QMessageBox.No, qtw.QMessageBox.No)
        if reply == qtw.QMessageBox.Yes:
            # remove all directories with projections
            clean_tmp_dirs(self.params['e_tmpdir'], self.config_group.get_fdt_names())
            # remove axis-search dir too
            tmp = os.path.join(self.params['e_tmpdir'], 'axis-search')
            event.accept()
        else:
            event.ignore()

