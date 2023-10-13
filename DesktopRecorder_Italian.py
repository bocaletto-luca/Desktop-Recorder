# Software Name: Desktop Recorder
# Author: Bocaletto Luca
# Site Web: https://www.elektronoide.it
# Language: Italian
import sys
import cv2
import pyautogui
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QRadioButton, QLabel
from PyQt5.QtCore import QTimer
from plyer import notification
from PyQt5.QtGui import QImage, QPixmap

# Definizione della classe principale
class DesktopRecorder(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

        self.is_recording = False
        self.video_writer = None
        self.selected_quality = None

    # Inizializzazione dell'interfaccia utente
    def initUI(self):
        self.setWindowTitle("Desktop Recorder")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
		
		title_label = QLabel("Screen Recorder", self)  # Aggiungi un titolo
        title_label.setAlignment(Qt.AlignCenter)  # Imposta l'allineamento al centro
        self.layout.addWidget(title_label)
        
        # Bottone per iniziare/arrestare la registrazione
        self.record_btn = QPushButton("Inizia a Registrare")
        self.record_btn.clicked.connect(self.toggle_recording)
        self.layout.addWidget(self.record_btn)

        # Opzioni di qualità video
        self.low_quality_radio = QRadioButton("480p")
        self.medium_quality_radio = QRadioButton("720p")
        self.high_quality_radio = QRadioButton("1080p")
        self.quality_group = []  # Gruppo per gestire le opzioni di qualità

        self.low_quality_radio.setChecked(True)  # Opzione predefinita
        self.layout.addWidget(self.low_quality_radio)
        self.layout.addWidget(self.medium_quality_radio)
        self.layout.addWidget(self.high_quality_radio) 

        # Configura la finestra principale con il layout
        self.central_widget.setLayout(self.layout)

        # Timer per catturare il frame
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(20)  # Aggiorna il frame ogni 20 ms

        # Label per visualizzare la miniatura del video
        self.thumbnail_label = QLabel(self)
        self.thumbnail_label.setFixedSize(300, 420)
        self.layout.addWidget(self.thumbnail_label)

    # Funzione per iniziare/arrestare la registrazione
    def toggle_recording(self):
        if not self.is_recording:
            for radio in self.quality_group:
                if radio.isChecked():
                    self.selected_quality = radio.text()
                    break

            # Configurazione del video writer
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            screen_width, screen_height = pyautogui.size()
            output_filename = f"desktop_recording_{self.selected_quality}.avi"

            self.video_writer = cv2.VideoWriter(output_filename, fourcc, 20.0, (screen_width, screen_height))
            self.record_btn.setText("Arresta la Registrazione")
            self.is_recording = True

            # Notifica l'inizio della registrazione
            notification.notify(
                title="Desktop Recorder",
                message="La registrazione è iniziata.",
            )
        else:
            # Arresta la registrazione e rilascia il writer
            self.video_writer.release()
            self.record_btn.setText("Inizia a Registrare")
            self.is_recording = False

            # Notifica la fine della registrazione
            notification.notify(
                title="Desktop Recorder",
                message="La registrazione è stata interrotta.",
            )

    # Funzione per catturare e aggiornare il frame
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

# Funzione principale
def main():
    app = QApplication(sys.argv)
    window = DesktopRecorder()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
