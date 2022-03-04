import yaml
import logging
import glob
import os

from PyQt5.QtWidgets import QGroupBox, QLabel, QGridLayout, QPushButton, QFileDialog, QLineEdit
# Auto Stitch
from ez_ufo_qt.GUI.Main.config import ConfigGroup
from ez_ufo_qt.GUI.StitchTools.auto_horizontal_stitch_funcs import AutoHorizontalStitchFunctions
from ez_ufo_qt.GUI.StitchTools.auto_vertical_stitch_funcs import AutoVerticalStitchFunctions
# Helpers
from ez_ufo_qt.Helpers.mview_main import main_prep
from ez_ufo_qt.Helpers.find_360_overlap import find_overlap
from ez_ufo_qt.Helpers.stitch_funcs import main_360_mp_depth2
from ez_ufo_qt.Helpers.stitch_funcs import main_sti_mp, main_conc_mp, main_360_mp_depth1
# Params
import ez_ufo_qt.GUI.params_io as params_io


class BatchProcessGroup(QGroupBox):
    def __init__(self):
        super().__init__()

        self.parameters = {}
        self.config_group = None
        self.auto_horizontal_stitch_funcs = None
        self.auto_vertical_stitch_funcs = None

        self.info_label = QLabel()
        self.set_info_label()

        self.input_dir_button = QPushButton("Select input directory")
        self.input_dir_button.setFixedWidth(500)
        self.input_dir_button.clicked.connect(self.input_dir_button_pressed)

        self.input_dir_entry = QLineEdit("...Enter the path to the input directory")
        self.input_dir_entry.setFixedWidth(450)
        self.input_dir_entry.textChanged.connect(self.set_input_entry)

        self.batch_proc_button = QPushButton("Begin Batch Process")
        self.batch_proc_button.clicked.connect(self.batch_proc_button_pressed)
        self.batch_proc_button.setStyleSheet("background-color:orangered; font-size:26px")
        self.batch_proc_button.setFixedHeight(100)

        self.set_layout()

    def set_layout(self):
        self.setMaximumSize(1000, 400)

        layout = QGridLayout()

        layout.addWidget(self.input_dir_button, 0, 0)
        layout.addWidget(self.input_dir_entry, 0, 1)

        layout.addWidget(self.info_label, 1, 0)

        layout.addWidget(self.batch_proc_button, 2, 0, 1, 2)
        self.setLayout(layout)

        self.show()

    def set_info_label(self):
        info_str = "EZ Batch Process allows for batch reconstruction and processing of images.\n\n"
        info_str += "The program reads a list of .yaml parameter files from the input directory and executes\n" \
                    "them sequentially in alpha-numeric order.\n"
        info_str += "It is the user's responsibility to name files so that they are executed in the desired order.\n"
        info_str += "It is suggested to prepend descriptive filenames with numbers to indicate the order.\n" \
                    "For example: \n\n"
        info_str += "00_horizontal_stitch_params.yaml\n"
        info_str += "01_ezufo_params.yaml\n"
        info_str += "02_vertical_stitch_params.yaml\n"
        self.info_label.setText(info_str)

    def input_dir_button_pressed(self):
        logging.debug("Input Button Pressed")
        dir_explore = QFileDialog(self)
        input_dir = dir_explore.getExistingDirectory()
        self.input_dir_entry.setText(input_dir)
        self.parameters['input_dir'] = input_dir

    def set_input_entry(self):
        logging.debug("Input Entry: " + str(self.input_dir_entry.text()))
        self.parameters['input_dir'] = str(self.input_dir_entry.text())

    def batch_proc_button_pressed(self):
        logging.debug("Batch Process Button Pressed")
        try:
            param_files_list = sorted(glob.glob(os.path.join(self.parameters['input_dir'], "*.yaml")))
            if len(param_files_list) == 0:
                print("=> Error: Did not find any .yaml files in the input directory. Please try again.")
            else:
                print("*************************************************************************")
                print("************************** Begin Batch Process **************************")
                print("*************************************************************************\n")
                print("=> Found the following .yaml files:")
                print(param_files_list)

                for file in param_files_list:
                    print("\n************************* Working on: *************************")
                    print("-->  " + file)
                    # Open .yaml file and store the parameters
                    try:
                        file_in = open(file, 'r')
                        params = yaml.load(file_in, Loader=yaml.FullLoader)
                    except FileNotFoundError:
                        print("Something went wrong")

                    params_type = params['parameters_type']
                    print("       type: " + params_type)

                    if params_type == "auto_horizontal_stitch":
                        try:
                            print("\n**********************************************")
                            print("********** Auto Horizontal Stitch ************")
                            print("**********************************************\n")
                            # Call functions to begin auto horizontal stitch and pass params
                            self.auto_horizontal_stitch_funcs = AutoHorizontalStitchFunctions(params)
                            self.auto_horizontal_stitch_funcs.run_horizontal_auto_stitch()
                            params_io.save_parameters(params, params['output_dir'])
                        except Exception as e:
                            print(e)
                    elif params_type == "ez_ufo_reco":
                        try:
                            print("\n**********************************************")
                            print("************** Reconstruction ****************")
                            print("**********************************************\n")
                            # Call functions to begin ezufo reco and pass params
                            self.config_group = ConfigGroup()
                            self.config_group.run_reconstruction(params, batch_run=True)
                            params_io.save_parameters(params, params['main_config_output_dir'])
                        except Exception as e:
                            print(e)
                    elif params_type == "auto_vertical_stitch":
                        try:
                            print("\n********************************************")
                            print("********** Auto Vertical Stitch ************")
                            print("********************************************\n")
                            # Call functions to begin auto horizontal stitch and pass params
                            self.auto_vertical_stitch_funcs = AutoVerticalStitchFunctions(params)
                            self.auto_vertical_stitch_funcs.run_vertical_auto_stitch()
                            params_io.save_parameters(params, params['output_dir'])
                        except Exception as e:
                            print(e)
                    elif params_type == "ez_mview":
                        try:
                            print("\n*************************************")
                            print("********** EZ Multi-View ************")
                            print("*************************************\n")
                            main_prep(params)
                            params_io.save_parameters(params, params['ezmview_input_dir'])
                        except Exception as e:
                            print(e)
                    elif params_type == "360_overlap":
                        try:
                            print("\n***********************************************")
                            print("**************** 360 Overlap ******************")
                            print("***********************************************\n")
                            find_overlap(params)
                            params_io.save_parameters(params, params['360overlap_output_dir'])
                        except Exception as e:
                            print(e)
                    elif params_type == "360_multi_stitch":
                        try:
                            print("\n****************************************")
                            print("********** 360 Multi Stitch ************")
                            print("****************************************\n")
                            if os.path.exists(params['360multi_temp_dir']):
                                os.system('rm -r {}'.format(params['360multi_temp_dir']))
                            if os.path.exists(params['360multi_output_dir']):
                                raise ValueError('Output directory exists')
                            print("======= Begin 360 Multi-Stitch =======")
                            main_360_mp_depth2(params)
                            params_io.save_parameters(params, params['360multi_output_dir'])
                            print("==== Waiting for Next Task ====")
                        except Exception as e:
                            print(e)
                    elif params_type == "ez_stitch":
                        try:
                            print("\n*********************************************")
                            print("**************** EZ Stitch ******************")
                            print("*********************************************\n")
                            if os.path.exists(params['ezstitch_temp_dir']):
                                os.system('rm -r {}'.format(params['ezstitch_temp_dir']))

                            if os.path.exists(params['ezstitch_output_dir']):
                                raise ValueError('Output directory exists')

                            print("======= Begin Stitching =======")
                            # Interpolate overlapping regions and equalize intensity
                            if params['ezstitch_stitch_type'] == 0:
                                main_sti_mp(params)
                            # Concatenate only
                            elif params['ezstitch_stitch_type'] == 1:
                                main_conc_mp(params)
                            # Half acquisition mode
                            elif params['ezstitch_stitch_type'] == 2:
                                main_360_mp_depth1(params)
                            params_io.save_parameters(params, params['ezstitch_output_dir'])
                            print("==== Waiting for Next Task ====")
                        except Exception as e:
                            print(e)
                    else:
                        print("Invalid params type: " + str(params_type))

                print("\n*****************************************************************************")
                print("************************** Completed Batch Process **************************")
                print("*****************************************************************************\n")
        except KeyError as k:
            print("Key Error: " + k)
