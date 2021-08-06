import logging
import os

from PyQt5.QtWidgets import QGridLayout, QLabel, QRadioButton, QGroupBox, QLineEdit, QCheckBox, QPushButton, QHBoxLayout, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt

from ez_ufo_qt.main_nlm import main_tk

class NLMDNGroup(QGroupBox):
    """
    Non-local means de-noising settings
    """
    def __init__(self):
        super().__init__()

        self.e_indir = ""
        self.e_input_is_file = False
        self.e_outdir = ""
        self.e_bigtif = False
        self.e_r = 0
        self.e_dx = 0
        self.e_h = 0
        self.e_sig = 0
        self.e_w = 0
        self.e_fast = False
        self.e_autosig = False
        self.e_dryrun = False

        self.setTitle("Non-local-means Denoising")
        self.setStyleSheet('QGroupBox {color: royalblue;}')

        self.input_dir_button = QPushButton("Select input directory")
        self.input_dir_button.clicked.connect(self.set_indir_button)

        self.select_img_button = QPushButton("Select one image")
        self.select_img_button.clicked.connect(self.select_image)

        self.input_dir_entry = QLineEdit()
        self.input_dir_entry.textChanged.connect(self.set_indir_entry)

        self.output_dir_button = QPushButton("Select output directory or filename pattern")
        self.output_dir_button.clicked.connect(self.set_outdir_button)

        self.save_biftiff_checkbox = QCheckBox("Save in bigtiff container")
        self.save_biftiff_checkbox.clicked.connect(self.set_save_bigtiff)

        self.output_dir_entry = QLineEdit()
        self.output_dir_entry.textChanged.connect(self.set_outdir_entry)

        self.similarity_radius_label = QLabel("Radius for similarity search")
        self.similarity_radius_entry = QLineEdit()
        self.similarity_radius_entry.textChanged.connect(self.set_rad_sim_entry)

        self.patch_radius_label = QLabel("Radius of patches")
        self.patch_radius_entry = QLineEdit()
        self.patch_radius_entry.textChanged.connect(self.set_rad_patch_entry)

        self.smoothing_label = QLabel("Smoothing control parameter")
        self.smoothing_entry = QLineEdit()
        self.smoothing_entry.textChanged.connect(self.set_smoothing_entry)

        self.noise_std_label = QLabel("Noise standard deviation")
        self.noise_std_entry = QLineEdit()
        self.noise_std_entry.textChanged.connect(self.set_noise_entry)

        self.window_label = QLabel("Window (optional)")
        self.window_entry = QLineEdit()
        self.window_entry.textChanged.connect(self.set_window_entry)

        self.fast_checkbox = QCheckBox("Fast")
        self.fast_checkbox.clicked.connect(self.set_fast_checkbox)

        self.sigma_checkbox = QCheckBox("Estimate sigma")
        self.sigma_checkbox.clicked.connect(self.set_sigma_checkbox)

        self.help_button = QPushButton("Help")
        self.help_button.clicked.connect(self.help_button_pressed)

        self.delete_button = QPushButton("Delete reco dir")
        self.delete_button.clicked.connect(self.delete_button_pressed)

        self.dry_button = QPushButton("Dry run")
        self.dry_button.clicked.connect(self.dry_button_pressed)

        self.apply_button = QPushButton("Apply filter")
        self.apply_button.clicked.connect(self.apply_button_pressed)

        self.set_layout()

    def set_layout(self):
        layout = QGridLayout()

        layout.addWidget(self.input_dir_button, 0, 0, 1, 2)
        layout.addWidget(self.select_img_button, 0, 2, 1, 2)
        layout.addWidget(self.input_dir_entry, 1, 0, 1, 4)
        layout.addWidget(self.output_dir_button, 2, 0, 1, 2)
        layout.addWidget(self.save_biftiff_checkbox, 2, 2, 1, 2, Qt.AlignCenter)
        layout.addWidget(self.output_dir_entry, 3, 0, 1, 4)
        layout.addWidget(self.similarity_radius_label, 4, 0, 1, 2)
        layout.addWidget(self.similarity_radius_entry, 4, 2, 1, 2)
        layout.addWidget(self.patch_radius_label, 5, 0, 1, 2)
        layout.addWidget(self.patch_radius_entry, 5, 2, 1, 2)
        layout.addWidget(self.smoothing_label, 6, 0, 1, 2)
        layout.addWidget(self.smoothing_entry, 6, 2, 1, 2)
        layout.addWidget(self.noise_std_label, 7, 0, 1, 2)
        layout.addWidget(self.noise_std_entry, 7, 2, 1, 2)
        layout.addWidget(self.window_label, 8, 0, 1, 2)
        layout.addWidget(self.window_entry, 8, 2, 1, 2)
        layout.addWidget(self.fast_checkbox, 9, 0, 1, 2, Qt.AlignCenter)
        layout.addWidget(self.sigma_checkbox, 9, 2, 1, 2, Qt.AlignCenter)

        layout.addWidget(self.help_button, 10, 0, 1, 1)
        layout.addWidget(self.delete_button, 10, 1)
        layout.addWidget(self.dry_button, 10, 2)
        layout.addWidget(self.apply_button, 10, 3)


        self.setLayout(layout)

    def init_values(self):
        self.input_dir_entry.setText(os.getcwd())
        self.output_dir_entry.setText(os.getcwd() + '-nlmfilt')
        self.e_bigtif = False
        self.similarity_radius_entry.setText("10")
        self.patch_radius_entry.setText("3")
        self.smoothing_entry.setText("0.0")
        self.noise_std_entry.setText("0.0")
        self.window_entry.setText("0.0")
        self.fast_checkbox.setChecked(True)
        self.e_fast = True
        self.sigma_checkbox.setChecked(False)
        self.e_sig = False
        self.e_dryrun = False

    def set_values_from_params(self):
        pass

    def set_indir_button(self):
        """
        Saves directory specified by user in file-dialog for input tomographic data
        """
        logging.debug("Select input directory pressed")
        dir_explore = QFileDialog(self)
        directory = dir_explore.getExistingDirectory()
        self.input_dir_entry.setText(directory)
        self.output_dir_entry.setText(directory + "-nlmfilt")
        self.e_indir = directory
        self.e_outdir = directory + "-nlmfilt"
        self.e_input_is_file = False

    def set_indir_entry(self):
        logging.debug("Indir entry: " + str(self.input_dir_entry.text()))
        self.e_indir = str(self.input_dir_entry.text())

    def select_image(self):
        logging.debug("Select one image button pressed")
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open .tif Image File', "", "Tiff Files (*.tif *.tiff)",
                                                  options=options)
        if file_path:
            img_name, img_ext = os.path.splitext(file_path)
            tmp = img_name + '-nlmfilt-%05i'+ img_ext
            self.input_dir_entry.setText(file_path)
            self.output_dir_entry.setText(tmp)
            self.e_indir = file_path
            self.e_outdir = tmp
            self.e_input_is_file = True

    def set_outdir_button(self):
        logging.debug("Select output directory pressed")
        dir_explore = QFileDialog(self)
        directory = dir_explore.getExistingDirectory()
        self.output_dir_entry.setText(directory)

    def set_save_bigtiff(self):
        logging.debug("Save bigtiff checkbox: " + str(self.save_biftiff_checkbox.isChecked()))
        self.e_bigtif = bool(self.save_biftiff_checkbox.isChecked())

    def set_outdir_entry(self):
        logging.debug("Outdir entry: " + str(self.output_dir_entry.text()))
        self.e_outdir = str(self.output_dir_entry.text())

    def set_rad_sim_entry(self):
        logging.debug("Radius for similarity: " + str(self.similarity_radius_entry.text()))
        self.e_r = int(self.similarity_radius_entry.text())

    def set_rad_patch_entry(self):
        logging.debug("Radius of patches: " + str(self.patch_radius_entry.text()))
        self.e_dx = int(self.patch_radius_entry.text())

    def set_smoothing_entry(self):
        logging.debug("Smoothing control: " + str(self.smoothing_entry.text()))
        self.e_h = float(self.smoothing_entry.text())

    def set_noise_entry(self):
        logging.debug("Noise std: " + str(self.noise_std_entry.text()))
        self.e_sig = float(self.noise_std_entry.text())

    def set_window_entry(self):
        logging.debug("Window: " + str(self.window_entry.text()))
        self.e_w = float(self.window_entry.text())

    def set_fast_checkbox(self):
        logging.debug("Fast: " + str(self.fast_checkbox.isChecked()))
        self.e_fast = bool(self.fast_checkbox.isChecked())

    def set_sigma_checkbox(self):
        logging.debug("Estimate sigma: " + str(self.sigma_checkbox.isChecked()))
        self.e_autosig = bool(self.sigma_checkbox.isChecked())

    def help_button_pressed(self):
        logging.debug("Help Button Pressed")
        h = ""
        h += "Note4: set to \"flats\" if \"flats2\" exist but you need to ignore them; \n"
        h += "SerG, BMIT CLS, Dec. 2020."
        QMessageBox.information(self, "Help", h)

    def delete_button_pressed(self):
        logging.debug("Delete Reco Button Pressed")
        """
        Deletes the directory that contains reconstructed data
        """
        logging.debug("DELETE")
        msg = "Delete directory with reconstructed data?"
        dialog = QMessageBox.warning(self, "Warning: data can be lost", msg, QMessageBox.Yes | QMessageBox.No)

        if dialog == QMessageBox.Yes:
            if os.path.exists(str(self.e_outdir)):
                logging.debug("YES")
                if self.e_outdir == self.e_indir:
                    logging.debug("Cannot delete: output directory is the same as input")
                else:
                    os.system( 'rm -rf {}'.format(self.e_outdir))
                    logging.debug("Directory with reconstructed data was removed")
            else:
                logging.debug("Directory does not exist")
        else:
            logging.debug("NO")

    def dry_button_pressed(self):
        logging.debug("Dry Run Button Pressed")
        self.e_dryrun = True
        self.apply_button_pressed()
        self.e_dryrun = False

    def apply_button_pressed(self):
        logging.debug("Apply Filter Button Pressed")
        args = tk_args(self.e_indir, self.e_input_is_file, \
                       self.e_outdir, self.e_bigtif, \
                       self.e_r, self.e_dx, self.e_h, self.e_sig, \
                       self.e_w, self.e_fast, self.e_autosig, \
                       self.e_dryrun)
        logging.debug(args.args)
        if os.path.exists(args.outdir) and not self.e_dryrun:
            titletext = "Warning: files can be overwritten"
            text1 = "Output directory exists. Files can be overwritten. Proceed?"
            dialog = QMessageBox.warning(self, titletext, text1, QMessageBox.Yes | QMessageBox.No)
            if dialog == QMessageBox.Yes:
                main_tk(args)
                QMessageBox.information(self, "Finished", "Finished")
        else:
            main_tk(args)
            QMessageBox.information(self, "Finished", "Finished")

class tk_args():
    def __init__(self, e_indir, e_input_is_file,
                 e_outdir, e_bigtif,
                 e_r, e_dx, e_h, e_sig,
                 e_w, e_fast, e_autosig,
                  e_dryrun):
        self.args = {}
        # PATHS
        self.args['indir'] = str(e_indir)
        setattr(self, 'indir', self.args['indir'])
        self.args['input_is_file'] = e_input_is_file
        setattr(self, 'input_is_file', self.args['input_is_file'])
        self.args['outdir'] = str(e_outdir)
        setattr(self, 'outdir', self.args['outdir'])
        # ALG PARAMS - MAIN
        self.args['search_r'] = int(e_r)
        setattr(self, 'search_r', self.args['search_r'])
        self.args['patch_r'] = int(e_dx)
        setattr(self, 'patch_r', self.args['patch_r'])
        self.args['h'] = float(e_h)
        setattr(self, 'h', self.args['h'])
        self.args['sig'] = float(e_sig)
        setattr(self, 'sig', self.args['sig'])
        # ALG PARAMS - optional
        self.args['w'] = float(e_w)
        setattr(self, 'w', self.args['w'])
        self.args['fast'] = bool(e_fast)
        setattr(self, 'fast', self.args['fast'])
        self.args['autosig'] = bool(e_autosig)
        setattr(self, 'autosig', self.args['autosig'])
        # Misc
        # self.args['inplace'] = bool(e_inplace.get())
        # setattr(self, 'inplace', self.args['inplace'])
        self.args['bigtif'] = bool(e_bigtif)
        setattr(self, 'bigtif', self.args['bigtif'])
        self.args['dryrun']=bool(e_dryrun)
        setattr(self,'dryrun',self.args['dryrun'])