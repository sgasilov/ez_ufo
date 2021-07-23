import logging
import os
import argparse
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
from ez_ufo_qt.GUI.ez_360_multi_stitch_qt import MultiStitch360Group
from ez_ufo_qt.GUI.ezmview_qt import EZMView
from ez_ufo_qt.GUI.eznlmdn_qt import EZnlmdnGroup
from ez_ufo_qt.GUI.ezstitch_qt import EZStitchGroup

import ez_ufo_qt.GUI.params as parameters

class GUI(qtw.QWidget):
    """
    Creates main GUI
    """

    def __init__(self, *args, **kwargs):
        super(GUI, self).__init__(*args, **kwargs)
        self.setWindowTitle('EZ-UFO GUI')

        self.setStyleSheet("font: 10pt; font-family: Arial")

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

        self.multi_stitch_360_group = MultiStitch360Group()

        self.ezmview_group = EZMView()

        self.eznlmdn_group = EZnlmdnGroup()

        self.ezstitch_group = EZStitchGroup()

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
        self.tab4 = qtw.QWidget()

        pr_ffc_box = qtw.QVBoxLayout()
        pr_ffc_box.addWidget(self.ffc_group)
        pr_ffc_box.addWidget(self.phase_retrieval_group)

        main_layout = qtw.QGridLayout()
        main_layout.addWidget(self.centre_of_rotation_group, 0, 0)
        main_layout.addWidget(self.filters_group, 0, 1)
        main_layout.addItem(pr_ffc_box, 1, 0)
        main_layout.addWidget(self.binning_group, 1, 1)
        main_layout.addWidget(self.config_group, 2, 0, 2, 0)

        image_layout = qtw.QGridLayout()
        image_layout.addWidget(self.image_group, 0, 0)

        ez_helpers_layout = qtw.QGridLayout()
        ez_helpers_layout.addWidget(self.multi_stitch_360_group, 0, 0)
        ez_helpers_layout.addWidget(self.ezmview_group, 0, 1)
        ez_helpers_layout.addWidget(self.eznlmdn_group, 1, 0)
        ez_helpers_layout.addWidget(self.ezstitch_group, 1, 1)

        # Add tabs
        self.tabs.addTab(self.tab1, "Main")
        self.tabs.addTab(self.tab2, "Image Viewer")
        self.tabs.addTab(self.tab3, "Advanced")
        self.tabs.addTab(self.tab4, "EZ Helpers")

        # Create main tab
        self.tab1.layout = main_layout
        self.tab1.setLayout(self.tab1.layout)

        # Create image tab
        self.tab2.layout = image_layout
        self.tab2.setLayout(self.tab2.layout)

        self.tab4.layout = ez_helpers_layout
        self.tab4.setLayout(self.tab4.layout)

        # Add tabs to widget
        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def update_values_from_params(self):
        logging.debug("Update Values from Params")
        logging.debug(parameters.params)
        self.centre_of_rotation_group.set_values_from_params()
        self.filters_group.set_values_from_params()
        self.ffc_group.set_values_from_params()
        self.phase_retrieval_group.set_values_from_params()
        self.binning_group.set_values_from_params()
        self.config_group.set_values_from_params()

    def switch_to_image_tab(self):
        if parameters.params['e_openIV'] is True:
            logging.debug("Switch to Image Tab")
            self.tabs.setCurrentWidget(self.tab2)
            if os.path.isdir(str(parameters.params['e_outdir'] + '/sli')):
                files = os.listdir(str(parameters.params['e_outdir'] + '/sli'))
                ##CHECK IF ONLY SINGLE IMAGE THEN USE OPEN IMAGE -- OTHERWISE OPEN STACK
                if len(files) == 1:
                    print("Only one file in {}: Opening single image {}".format(parameters.params['e_outdir'] + '/sli', files[0]))
                    filePath = str(parameters.params['e_outdir'] + '/sli/' + str(files[0]))
                    self.image_group.open_image_from_filepath(filePath)
                else:
                    print("Multiple files in {}: Opening stack of images".format(str(parameters.params['e_outdir'] + '/sli')))
                    self.image_group.open_stack_from_path(str(parameters.params['e_outdir'] + '/sli'))
            else:
                print("No output directory found")

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

