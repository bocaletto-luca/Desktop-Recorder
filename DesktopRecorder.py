# Software Name: Desktop Recorder
# Author: Bocaletto Luca
# Language: Italian
import sys
import sys
import cv2
import pyautogui
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QRadioButton, QLabel
from PyQt5.QtCore import QTimer
from plyer import notification
from PyQt5.QtGui import QImage, QPixmap

# Definition of the main class
class DesktopRecorder(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

        self.is_recording = False
        self.video_writer = None
        self.selected_quality = None

    # Initialize the user interface
    def initUI(self):
        self.setWindowTitle("Desktop Recorder")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        # Button to start/stop recording
        self.record_btn = QPushButton("Start Recording")
        self.record_btn.clicked.connect(self.toggle_recording)
        self.layout.addWidget(self.record_btn)

        # Video quality options
        self.low_quality_radio = QRadioButton("480p")
        self.medium_quality_radio = QRadioButton("720p")
        self.high_quality_radio = QRadioButton("1080p")
        self.quality_group = []  # Group to manage quality options

        self.low_quality_radio.setChecked(True)  # Default option
        self.layout.addWidget(self.low_quality_radio)
        self.layout.addWidget(self.medium_quality_radio)
        self.layout.addWidget(self.high_quality_radio)

        # Configure the main window with the layout
        self.central_widget.setLayout(self.layout)

        # Timer to capture frames
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(20)  # Update frame every 20 ms

        # Label to display the video thumbnail
        self.thumbnail_label = QLabel(self)
        self.thumbnail_label.setFixedSize(300, 420)
        self.layout.addWidget(self.thumbnail_label)

    # Function to start/stop recording
    def toggle_recording(self):
        if not self.is_recording:
            for radio in self.quality_group:
                if radio.isChecked():
                    self.selected_quality = radio.text()
                    break

            # Video writer configuration
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            screen_width, screen_height = pyautogui.size()
            output_filename = f"desktop_recording_{self.selected_quality}.avi"

            self.video_writer = cv2.VideoWriter(output_filename, fourcc, 20.0, (screen_width, screen_height))
            self.record_btn.setText("Stop Recording")
            self.is_recording = True

            # Notify the start of recording
            notification.notify(
                title="Desktop Recorder",
                message="Recording has started.",
            )
        else:
            # Stop recording and release the writer
            self.video_writer.release()
            self.record_btn.setText("Start Recording")
            self.is_recording = False

            # Notify the end of recording
            notification.notify(
                title="Desktop Recorder",
                message="Recording has been stopped.",
            )

    # Function to capture and update the frame
    def update_frame(self):
        if self.is_recording:
            screenshot = pyautogui.screenshot()
            frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            self.video_writer.write(frame)

            small_frame = cv2.resize(frame, (300, 420))
            frame_rgb = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame_rgb.shape
            bytes_per_line = ch * w
            q_image = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
            self.thumbnail_label.setPixmap(QPixmap.fromImage(q_image))

# Main function
def main():
    app = QApplication(sys.argv)
    window = DesktopRecorder()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
