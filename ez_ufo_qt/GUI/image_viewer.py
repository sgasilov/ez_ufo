import logging
from PyQt5.QtWidgets import QGroupBox, QGridLayout, QPushButton, QFileDialog, QLabel, QWidget
from PyQt5.QtGui import QPixmap

class ImageViewerGroup(QGroupBox):
    """
    Viewing of tiff and multi-page tiff files
    """

    def __init__(self):
        super().__init__()

        self.directory_select = QPushButton()
        self.directory_select.setText("Open image from file")
        self.directory_select.clicked.connect(self.open_image_from_file)

        self.set_layout()

    def set_layout(self):
        layout = QGridLayout()

        layout.addWidget(self.directory_select, 0, 1)

        self.setLayout(layout)

    def open_image_from_file(self):
        logging.debug("Open image button pressed")
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(self, 'QFileDialog.getOpenFileName()', "", "All Files (*)", options=options)
        if filePath:
            logging.debug("Import image path: " + filePath)