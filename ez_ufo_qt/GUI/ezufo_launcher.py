#!/usr/bin/env python3

import logging
import os
from PyQt5 import QtWidgets as qtw

from ez_ufo_qt.GUI.centre_of_rotation import CentreOfRotationGroup
from ez_ufo_qt.GUI.filters import FiltersGroup
from ez_ufo_qt.GUI.ffc import FFCGroup
from ez_ufo_qt.GUI.phase_retrieval import PhaseRetrievalGroup
from ez_ufo_qt.GUI.binning import BinningGroup
from ez_ufo_qt.GUI.config import ConfigGroup
from ez_ufo_qt.main import main_tk, clean_tmp_dirs
from ez_ufo_qt.GUI.yaml_in_out import Yaml_IO
from ez_ufo_qt.GUI.image_viewer import ImageViewerGroup

import ez_ufo_qt.GUI.params as parameters

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
        logger.setLevel(logging.DEBUG)

        # Read in default parameter settings from yaml file
        settings_path = os.path.dirname(os.path.abspath(__file__)) + '/default_settings.yaml'
        self.yaml_io = Yaml_IO()
        self.yaml_data = self.yaml_io.read_yaml(settings_path)
        parameters.params = dict(self.yaml_data)

        # Create and setup classes for each section of GUI
        self.centre_of_rotation_group = CentreOfRotationGroup()
        self.centre_of_rotation_group.init_values()

        self.filters_group = FiltersGroup()
        self.filters_group.init_values()

        self.ffc_group = FFCGroup()
        self.ffc_group.init_values()

        self.phase_retrieval_group = PhaseRetrievalGroup()
        self.phase_retrieval_group.init_values()

        self.binning_group = BinningGroup()
        self.binning_group.init_values()

        self.config_group = ConfigGroup()
        self.config_group.init_values()

        self.image_group = ImageViewerGroup()

        #######################################################

        self.set_layout()
        self.resize(0, 0) #window to minimum size

        # When new settings are imported signal is sent and this catches it to update params for each GUI object
        self.config_group.signal_update_vals_from_params.connect(self.update_values_from_params)

        # When RECO is done send signal from config
        self.config_group.signal_reco_done.connect(self.switch_to_image_tab)

        finish = qtw.QAction("Quit", self)
        finish.triggered.connect(self.closeEvent)

        self.show()

    def set_layout(self):
        layout = qtw.QVBoxLayout(self)
        # Initialize tab screen
        self.tabs = qtw.QTabWidget()
        self.tab1 = qtw.QWidget()
        self.tab2 = qtw.QWidget()
        self.tab3 = qtw.QWidget()

        pr_ffc_box = qtw.QVBoxLayout()
        pr_ffc_box.addWidget(self.ffc_group)
        pr_ffc_box.addWidget(self.phase_retrieval_group)

        main_layout = qtw.QGridLayout()
        main_layout.addWidget(self.centre_of_rotation_group, 0, 0)
        main_layout.addWidget(self.filters_group, 0, 1)
        main_layout.addItem(pr_ffc_box, 1, 0)
        #main_layout.addWidget(self.phase_retrieval_group, 1, 0)
        main_layout.addWidget(self.binning_group, 1, 1)
        main_layout.addWidget(self.config_group, 2, 0, 2, 0)

        image_layout = qtw.QGridLayout()
        image_layout.addWidget(self.image_group, 0, 0)

        # Add tabs
        self.tabs.addTab(self.tab1, "Main")
        self.tabs.addTab(self.tab2, "Image Viewer")
        self.tabs.addTab(self.tab3, "Advanced")

        # Create main tab
        self.tab1.layout = main_layout
        self.tab1.setLayout(self.tab1.layout)

        # Create image tab
        self.tab2.layout = image_layout
        self.tab2.setLayout(self.tab2.layout)

        # Add tabs to widget
        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def update_values_from_params(self):
        logging.debug("Update Values from Params")
        logging.debug(parameters.params)
        self.centre_of_rotation_group.set_values_from_params()
        self.filters_group.set_values_from_params()
        self.phase_retrieval_group.set_values_from_params()
        self.binning_group.set_values_from_params()
        self.config_group.set_values_from_params()

    def switch_to_image_tab(self):
        if parameters.params['e_openIV'] is True:
            logging.debug("Switch to Image Tab")
            self.tabs.setCurrentWidget(self.tab2)
            self.image_group.open_stack_from_path(str(parameters.params['e_outdir'] + '/sli'))

    def closeEvent(self, event):
        logging.debug("QUIT")
        reply = qtw.QMessageBox.question(self, 'Quit', 'Are you sure you want to quit?',
        qtw.QMessageBox.Yes | qtw.QMessageBox.No, qtw.QMessageBox.No)
        if reply == qtw.QMessageBox.Yes:
            # remove all directories with projections
            clean_tmp_dirs(parameters.params['e_tmpdir'], self.config_group.get_fdt_names())
            # remove axis-search dir too
            tmp = os.path.join(parameters.params['e_tmpdir'], 'axis-search')
            event.accept()
        else:
            event.ignore()

