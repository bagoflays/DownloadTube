from PyQt5.QtWidgets import QApplication, QFileDialog, QVBoxLayout, QWidget, QPushButton, QSpacerItem, QSizePolicy, QLabel, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt
import sys
from pytube import YouTube

class DirectorySelectionWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Create a spacer item to push the label and input field to the top
        spacer_top = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacer_top)

        # Create the button
        button = QPushButton("Select Directory")
        button.setFixedHeight(60)  # Set the button height to 60 pixels
        layout.addWidget(button, alignment=Qt.AlignCenter)

        # Create a spacer item to push the button and label to the middle
        spacer_middle = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacer_middle)

        # Create the label and input field for "File name"
        label_file = QLabel("File name:")
        layout.addWidget(label_file, alignment=Qt.AlignCenter)

        self.input_file = QLineEdit()
        self.input_file.setFixedHeight(30)  # Set the input field height to 30 pixels
        layout.addWidget(self.input_file, alignment=Qt.AlignCenter)

        # Create a spacer item to push the "File name" label and input field to the middle
        spacer_middle2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacer_middle2)

        # Create the label and input field for "Youtube Video"
        label_video = QLabel("Youtube Video:")
        layout.addWidget(label_video, alignment=Qt.AlignCenter)

        self.input_video = QLineEdit()
        self.input_video.setFixedHeight(30)  # Set the input field height to 30 pixels
        layout.addWidget(self.input_video, alignment=Qt.AlignCenter)

        # Create a spacer item to push the "Youtube Video" label and input field to the bottom
        spacer_bottom = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacer_bottom)

        # Create the "Export Video" button
        button_export = QPushButton("Export Video")
        button_export.setFixedHeight(60)  # Set the button height to 60 pixels
        layout.addWidget(button_export, alignment=Qt.AlignCenter)

        self.setLayout(layout)

        # Set window properties
        self.setWindowTitle("DownloadTube: Youtube Video Downloader")
        self.setFixedSize(1500, 720)
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)

        # Position the window at the middle of the screen
        screen_geometry = QApplication.desktop().availableGeometry()
        x = screen_geometry.width() // 2 - self.width() // 2
        y = screen_geometry.height() // 2 - self.height() // 2
        self.move(x, y)

        # Connect the button's clicked signal to the selectDirectory function
        button.clicked.connect(self.selectDirectory)

        # Connect the "Export Video" button's clicked signal to the exportVideo function
        button_export.clicked.connect(self.exportVideo)

        # Initialize the directory, file, and video input variables
        self.selected_directory = ""
        self.input_file_text = ""
        self.input_video_text = ""

    def selectDirectory(self):
        selected_directory = QFileDialog.getExistingDirectory(None, "Select Directory")
        print("Selected Directory:", selected_directory)
        # Save the selected directory as text in a variable
        self.selected_directory = selected_directory

        # Save the input field text for "File name" as a variable
        self.input_file_text = self.input_file.text()
        print("Input File Text:", self.input_file_text)

        # Save the input field text for "Youtube Video" as a variable
        self.input_video_text = self.input_video.text()
        print("Input Video Text:", self.input_video_text)

    def exportVideo(self):
        if not self.selected_directory:
            QMessageBox.critical(self, "Error", "No directory selected.")
            return

        self.input_file_text = self.input_file.text()  # Update the file name variable

        if not self.input_file_text:
            QMessageBox.critical(self, "Error", "No file name specified.")
            return

        self.input_video_text = self.input_video.text()  # Update the video URL variable

        if not self.input_video_text:
            QMessageBox.critical(self, "Error", "No YouTube video URL specified.")
            return

        try:
            yt = YouTube(self.input_video_text)
            stream = yt.streams.filter(file_extension='mp4').first()  # Select the first stream with MP4 format
            if stream is not None:
                file_path = self.selected_directory + '/' + self.input_file_text + '.mp4'
                stream.download(output_path=self.selected_directory, filename=self.input_file_text + ".mp4")
                QMessageBox.information(self, "Success", "Video exported successfully as:\n" + file_path)
            else:
                QMessageBox.critical(self, "Error", "No suitable video stream found.")
        except Exception as e:
            QMessageBox.critical(self, "Error", "An error occurred:\n" + str(e))

app = QApplication(sys.argv)
widget = DirectorySelectionWidget()
widget.show()
sys.exit(app.exec_())
