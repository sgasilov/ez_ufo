import os
import numpy as np
import logging
import pyqtgraph as pg
from tifffile import imread, imwrite
from PyQt5.QtWidgets import QGroupBox, QGridLayout, QPushButton, QFileDialog, QLabel, QWidget


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
            img_arr = read_image(filePath)
            pg.image(img_arr)


class InvalidDataSetError(Exception):
    """
    Error to be raised on attempt to read data from empty or non-existing data set
    """
    pass

def validate_files_path(files_path: str, supported_file_types: list) -> bool:
    """
    Validates specified path
    :param supported_file_types: List of supported extensions
    :param files_path: Path to validate
    :return: True if path exists and contains at least one file of supported type, else False
    """
    try:
        valid_files_list = get_valid_files_list(files_path=files_path,
                                                supported_file_types=supported_file_types)
    except InvalidDataSetError:
        return False
    return len(valid_files_list) > 0


def get_valid_files_list(files_path: str, supported_file_types: list) -> list:
    """
    Get the list of files of supported type in directory
    :param supported_file_types: List of supported extensions
    :param files_path: Path to directory with files
    :return: List of full paths to files
    """
    # Check if directory exists
    if not os.path.exists(files_path):
        raise InvalidDataSetError(f"No such directory: {files_path}")

    files_list = os.listdir(files_path)
    valid_files_list = [
        os.path.join(files_path, file_name)
        for file_name in files_list
        if os.path.splitext(file_name)[1] in supported_file_types
    ]
    return valid_files_list


def read_image(image_file_path: str, data_type=np.float32) -> np.ndarray:
    """
    Reads image file to numpy.ndarray of specified type
    :param data_type: Data type to store the image
    :param image_file_path: Full path to image to read
    :return:
    """
    return imread(image_file_path).astype(dtype=data_type)


def write_image(image: np.ndarray, target_directory: str, target_name: str, data_type=np.float32):
    """
    Writes image data to file
    :param image: Image data
    :param target_directory: Path to directory to write image
    :param target_name: Target image file name
    :param data_type: Data type to write the image
    :return:
    """
    os.makedirs(target_directory, exist_ok=True)
    data_file_path = os.path.join(target_directory, target_name)
    imwrite(data_file_path, data=image.astype(dtype=data_type))


def read_all_images(image_files_path: str, supported_image_types: list,  data_type=np.float32) -> np.ndarray:
    """
    Reads all images of the supported type from specified directory
    :param supported_image_types: List of supported extensions
    :param image_files_path: Path to directory with images
    :param data_type: Data type to store the images
    :return: 3-dimensional numpy.ndarray of specified type, first index being image index
    """
    valid_files_list = get_valid_files_list(files_path=image_files_path,
                                            supported_file_types=supported_image_types)
    if len(valid_files_list) == 0:
        raise InvalidDataSetError(f"Directory {image_files_path} "
                                  f"does not contain files of supported types {supported_image_types}")
    data_array = imread(valid_files_list).astype(dtype=data_type)
    return np.array(data_array)