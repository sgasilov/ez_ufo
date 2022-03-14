import yaml
import logging
import glob
import os

from PyQt5.QtWidgets import QGroupBox, QLabel, QGridLayout, QPushButton, QFileDialog, QLineEdit, QMessageBox
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
        self.file_list_group = None
        self.meta_batch_input_list = []

        self.params_file_list = []

        # ---- Simple Batch ---- #
        self.help_button = QPushButton("Help")
        self.help_button.clicked.connect(self.help_button_pressed)

        self.input_dir_button = QPushButton("Select input directory")
        self.input_dir_button.clicked.connect(self.input_dir_button_pressed)

        self.input_dir_entry = QLineEdit("...Enter the path to the input directory")
        self.input_dir_entry.setFixedWidth(500)
        self.input_dir_entry.textChanged.connect(self.set_input_entry)

        self.file_list_label = QLabel()
        self.file_list_content_label = QLabel()

        self.batch_proc_button = QPushButton("Begin Batch Process")
        self.batch_proc_button.clicked.connect(self.batch_proc_button_pressed)
        self.batch_proc_button.setStyleSheet("background-color:orangered; font-size:26px")
        self.batch_proc_button.setFixedHeight(50)

        # ---- Meta Batch ---- #
        self.meta_help_button = QPushButton("Help")
        self.meta_help_button.clicked.connect(self.meta_help_button_pressed)

        self.meta_add_input_dir_button = QPushButton("Add input directory")
        self.meta_add_input_dir_button.clicked.connect(self.meta_add_input_dir_button_pressed)

        self.meta_remove_input_dir_button = QPushButton("Remove input directory")
        self.meta_remove_input_dir_button.clicked.connect(self.meta_remove_input_dir_button_pressed)

        self.meta_directory_list_label = QLabel()
        self.meta_directory_list_content_label = QLabel()

        self.meta_file_list_label = QLabel("Hello")
        self.meta_file_list_content_label = QLabel()

        self.meta_batch_proc_button = QPushButton("Begin Batch Process")
        self.meta_batch_proc_button.clicked.connect(self.meta_batch_proc_button_pressed)
        self.meta_batch_proc_button.setStyleSheet("background-color:orangered; font-size:26px")
        self.meta_batch_proc_button.setFixedHeight(50)

        self.set_layout()

    def set_layout(self):
        self.setMaximumSize(1000, 800)

        layout = QGridLayout()

        # ---- Simple Batch ---- #
        '''
        input_group = QGroupBox()
        input_group_layout = QGridLayout()
        input_group_layout.addWidget(self.help_button, 0, 0)
        input_group_layout.addWidget(self.input_dir_button, 0, 1)
        input_group_layout.addWidget(self.input_dir_entry, 0, 2)
        input_group.setLayout(input_group_layout)

        self.file_list_group = QGroupBox()
        file_list_layout = QGridLayout()
        file_list_layout.addWidget(self.file_list_label, 2, 0)
        file_list_layout.addWidget(self.file_list_content_label, 2, 1)
        self.file_list_group.setLayout(file_list_layout)
        self.file_list_group.setHidden(True)

        batch_group = QGroupBox()
        batch_group_layout = QGridLayout()
        batch_group_layout.addWidget(input_group, 1, 0, 1, 2)
        batch_group_layout.addWidget(self.file_list_group, 2, 0, 1, 2)
        batch_group_layout.addWidget(self.batch_proc_button, 3, 0, 1, 2)
        batch_group.setLayout(batch_group_layout)
        batch_group.setStyleSheet('background: #eee')
        '''
        # ---- Meta Batch ---- #
        meta_input_group = QGroupBox()
        meta_input_group_layout = QGridLayout()
        meta_input_group_layout.addWidget(self.meta_help_button, 0, 0)
        meta_input_group_layout.addWidget(self.meta_add_input_dir_button, 0, 1)
        meta_input_group_layout.addWidget(self.meta_remove_input_dir_button, 0, 2)
        meta_input_group.setLayout(meta_input_group_layout)

        self.meta_file_list_group = QGroupBox()
        meta_file_list_layout = QGridLayout()
        meta_file_list_layout.addWidget(self.meta_file_list_label, 2, 0)
        meta_file_list_layout.addWidget(self.meta_file_list_content_label, 2, 1)
        self.meta_file_list_group.setLayout(meta_file_list_layout)
        self.meta_file_list_group.setHidden(True)

        meta_batch_group = QGroupBox()
        meta_batch_group_layout = QGridLayout()
        meta_batch_group_layout.addWidget(meta_input_group, 0, 0, 1, 2)
        meta_batch_group_layout.addWidget(self.meta_file_list_group, 2, 0, 1, 2)
        meta_batch_group_layout.addWidget(self.meta_batch_proc_button, 3, 0, 1, 2)
        meta_batch_group.setLayout(meta_batch_group_layout)
        meta_batch_group.setStyleSheet('background: #eee')

        #layout.addWidget(batch_group)
        layout.addWidget(meta_batch_group)
        self.setLayout(layout)

        self.show()

    # ---- Simple Batch ---- #
    def input_dir_button_pressed(self):
        logging.debug("Input Button Pressed")
        dir_explore = QFileDialog(self)
        input_dir = dir_explore.getExistingDirectory()
        self.input_dir_entry.setText(input_dir)
        self.parameters['input_dir'] = input_dir
        self.param_files_list = sorted(glob.glob(os.path.join(self.parameters['input_dir'], "*.yaml")))
        self.set_file_list_content_label(self.param_files_list)

    def set_input_entry(self):
        logging.debug("Input Entry: " + str(self.input_dir_entry.text()))
        self.parameters['input_dir'] = str(self.input_dir_entry.text())

    def set_file_list_content_label(self, param_files_list):
        str_buffer = ''
        for params_file_path in param_files_list:
            str_buffer += f' -> {params_file_path}\n'
        self.file_list_label.setText("Found the following parameters files: ")
        self.file_list_content_label.setText(str_buffer)
        self.file_list_group.setHidden(False)
        print("Found the following parameters files: ")
        print(str_buffer)

    def help_button_pressed(self):
        logging.debug("HELP")
        info_str = "EZ Batch Process allows for batch reconstruction and processing of images.\n\n"
        info_str += "The program reads a list of .yaml parameter files from the input directory and executes\n" \
                    "them sequentially in alpha-numeric order.\n"
        info_str += "It is the user's responsibility to name files so that they are executed in the desired order.\n"
        info_str += "It is suggested to prepend descriptive filenames with numbers to indicate the order.\n" \
                    "For example: \n\n"
        info_str += "00_horizontal_stitch_params.yaml\n"
        info_str += "01_ezufo_params.yaml\n"
        info_str += "02_vertical_stitch_params.yaml\n"
        QMessageBox.information(self, "Help", info_str)

    def batch_proc_button_pressed(self):
        self.run_batch_process()

    def run_batch_process(self):
        logging.debug("Batch Process Button Pressed")
        try:
            if len(self.param_files_list) == 0:
                print("=> Error: Did not find any .yaml files in the input directory. Please try again.")
            else:
                print("*************************************************************************")
                print("************************** Begin Batch Process **************************")
                print("*************************************************************************\n")
                print("=> Found the following .yaml files:")
                print(self.param_files_list)

                for file in self.param_files_list:
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

    # ---- Meta Batch ---- #
    def meta_help_button_pressed(self):
        logging.debug("HELP")
        info_str = "EZ Batch Process allows for batch reconstruction and processing of images.\n\n"
        info_str += "The user can select multiple input directories containing .yaml files." \
                    " These directories will be processed in the order that they are added. \n\n"
        info_str += "From each input directory, the program reads a list of .yaml parameter files and executes " \
                    "them sequentially in alpha-numeric order.\n\n"
        info_str += "It is the user's responsibility to name files so that they are executed in the desired order.\n\n"
        info_str += "It is suggested to prepend descriptive filenames with numbers to indicate the order.\n\n" \
                    "For example: \n\n"
        info_str += "00_horizontal_stitch_params.yaml\n"
        info_str += "01_ezufo_params.yaml\n"
        info_str += "02_vertical_stitch_params.yaml\n\n\n"
        info_str += "Once all directories have been added, simply click the big red button to begin processing :)"

        QMessageBox.information(self, "Help", info_str)

    def meta_add_input_dir_button_pressed(self):
        logging.debug("Input Button Pressed")
        dir_explore = QFileDialog(self)
        input_dir = dir_explore.getExistingDirectory()
        self.meta_batch_input_list.append(input_dir)
        self.set_meta_directory_list_content_label(self.meta_batch_input_list)

    def meta_remove_input_dir_button_pressed(self):
        if not len(self.meta_batch_input_list) == 0:
            self.meta_batch_input_list.pop()
        self.set_meta_directory_list_content_label(self.meta_batch_input_list)

    def set_meta_directory_list_content_label(self, directory_list):
        format_string = ""
        for index, dir_name in enumerate(directory_list):
            format_string += "{} : {}\n".format(index, directory_list[index])
        self.meta_file_list_label.setText("Found the following directories: ")
        self.meta_file_list_content_label.setText(format_string)
        self.meta_file_list_group.setHidden(False)
        print("Found the following directories: ")
        print(format_string)

    def meta_batch_proc_button_pressed(self):
        print("***********************************************************************************************")
        print("************************************* Begin Meta Batch Process ********************************")
        print("***********************************************************************************************\n")
        self.verify_input_directories()
        for dir_path in self.meta_batch_input_list:
            print("Working on: {}".format(dir_path))
            self.param_files_list = sorted(glob.glob(os.path.join(dir_path, "*.yaml")))
            self.run_batch_process()

        print("***********************************************************************************************")
        print("*********************************** Completed Meta Batch Process ******************************")
        print("***********************************************************************************************\n")

    def verify_input_directories(self):
        """
        Checks that each directory in the meta batch input list contains .yaml files
        If the directory does not contain .yaml files then it is removed from the list
        """
        for index, dir_path in enumerate(self.meta_batch_input_list):
            yaml_list = glob.glob(os.path.join(dir_path, '*.yaml'))
            if len(yaml_list) != 0:
                print("{} : {} contains : ".format(index, dir_path))
                for file in yaml_list:
                    print("{}\n".format(file))
            else:
                print("{} : {} does not contain any .yaml files\n".format(index, dir_path))
                self.meta_batch_input_list.pop(index)
