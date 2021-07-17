import sys
from PyQt5.QtWidgets import QGroupBox, QPushButton, QLineEdit, QCheckBox, QLabel, QGridLayout, QVBoxLayout, QApplication, QHBoxLayout

class EZnlmdnGroup(QGroupBox):

    def __init__(self):
        super().__init__()

        self.setTitle("EZ-nlmdn")
        self.setStyleSheet('QGroupBox {color: blue;}')

        self.input_dir_button = QPushButton()
        self.input_dir_button.setText("Select input directory")

        self.select_image_button = QPushButton()
        self.select_image_button.setText("Select one image")

        self.select_input_entry = QLineEdit()

        self.select_output_button = QPushButton()
        self.select_output_button.setText("Select output directory or filename pattern")

        self.bigtiff_checkbox = QCheckBox()
        self.bigtiff_checkbox.setText("Save in bigtiff container")

        self.select_output_entry = QLineEdit()

        self.radius_similarity_label = QLabel()
        self.radius_similarity_label.setText("Radius for similarity search")
        self.radius_similarity_entry = QLineEdit()

        self.radius_patches_label = QLabel()
        self.radius_patches_label.setText("Radius of patches")
        self.radius_patches_entry = QLineEdit()

        self.smoothing_control_label = QLabel()
        self.smoothing_control_label.setText("Smoothing control parameter")
        self.smoothing_control_entry = QLineEdit()

        self.noise_sd_label = QLabel()
        self.noise_sd_label.setText("Noise standard deviation")
        self.noise_sd_entry = QLineEdit()

        self.window_label = QLabel()
        self.window_label.setText("Window (optional)")
        self.window_entry = QLineEdit()

        self.fast_checkbox = QCheckBox()
        self.fast_checkbox.setText("Fast")

        self.estimate_sigma_checkbox = QCheckBox()
        self.estimate_sigma_checkbox.setText("Estimate sigma")

        self.quit_button = QPushButton()
        self.quit_button.setText("Quit")
        self.quit_button.setStyleSheet("background-color:lightgrey;color:black; font: 14pt; font-weight: bold;")

        self.help_button = QPushButton()
        self.help_button.setText("Help")
        self.help_button.setStyleSheet("background-color:lightgrey;color:black; font: 14pt; font-weight: bold;")

        self.delete_button = QPushButton()
        self.delete_button.setText("Delete reco dir")
        self.delete_button.setStyleSheet("background-color:lightgrey;color:black; font: 14pt; font-weight: bold;")

        self.dry_run_button = QPushButton()
        self.dry_run_button.setText("Dry run")
        self.dry_run_button.setStyleSheet("background-color:lightgrey;color:black; font: 14pt; font-weight: bold;")

        self.apply_filter_button = QPushButton()
        self.apply_filter_button.setText("Apply filter")
        self.apply_filter_button.setStyleSheet("background-color:lightgrey;color:royalblue; font: 14pt; font-weight: bold;")

        self.set_layout()


    def set_layout(self):
        layout = QGridLayout()

        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.input_dir_button)
        hbox1.addWidget(self.select_image_button)

        layout.addItem(hbox1, 0, 0)
        layout.addWidget(self.select_input_entry, 1, 0)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.select_output_button)
        hbox2.addWidget(self.bigtiff_checkbox)

        layout.addItem(hbox2, 2, 0)
        layout.addWidget(self.select_output_entry, 3, 0)

        grid = QGridLayout()
        grid.addWidget(self.radius_similarity_label, 0, 0)
        grid.addWidget(self.radius_similarity_entry, 0, 1)
        grid.addWidget(self.radius_patches_label, 1, 0)
        grid.addWidget(self.radius_patches_entry, 1, 1)
        grid.addWidget(self.smoothing_control_label, 2, 0)
        grid.addWidget(self.smoothing_control_entry, 2, 1)
        grid.addWidget(self.noise_sd_label, 3, 0)
        grid.addWidget(self.noise_sd_entry, 3, 1)
        grid.addWidget(self.window_label, 4, 0)
        grid.addWidget(self.window_entry, 4, 1)
        grid.addWidget(self.fast_checkbox, 5, 0)
        grid.addWidget(self.estimate_sigma_checkbox, 5, 1)
        layout.addItem(grid, 4, 0)

        hbox3 = QHBoxLayout()
        hbox3.addWidget(self.quit_button)
        hbox3.addWidget(self.help_button)
        hbox3.addWidget(self.delete_button)
        hbox3.addWidget(self.dry_run_button)
        hbox3.addWidget(self.apply_filter_button)
        layout.addItem(hbox3, 5, 0)

        self.setLayout(layout)

'''
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = EZnlmdnGroup()
    sys.exit(app.exec_())
'''