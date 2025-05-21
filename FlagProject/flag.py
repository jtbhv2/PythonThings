from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
from PySide6.QtGui import QPixmap, QImage, Qt
from flagpy import get_country_list, get_flag_img
import numpy as np
#np.random.seed(1)
class RandomCountryFlagApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Guess Flag")
        self.setGeometry(100, 100, 400, 400)

        layout = QVBoxLayout()

        # Label to display country flag
        self.flag_label = QLabel()
        layout.addWidget(self.flag_label)

        # Label to display country name
        self.name_label = QLabel()
        self.name_label.setAlignment(Qt.AlignCenter)
        self.name_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(self.name_label)

        # Button to display country name and flag
        self.show_button = QPushButton("Show Name")
        self.show_button.clicked.connect(self.display_country_info)
        layout.addWidget(self.show_button)

        # Button to show next random flag and guess name
        self.next_button = QPushButton("Next Flag")
        self.next_button.clicked.connect(self.display_random_flag)
        layout.addWidget(self.next_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.checked_in = []
        self.display_random_flag()

    def display_random_flag(self):
            countries = get_country_list()
            while True:
                random_index = np.random.randint(0, len(countries))
                if (random_index not in self.checked_in):
                    self.checked_in.append(random_index)
                    break
                if len(self.checked_in) == len(countries):
                    
                    break
                    
            
            
            self.current_country = countries[random_index]
            flag_image = get_flag_img(self.current_country)
            qt_image = QImage(flag_image.tobytes(), flag_image.width, flag_image.height, flag_image.width * 3, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_image)
            self.flag_label.setPixmap(pixmap)
            self.name_label.clear()

    def display_country_info(self):
        self.name_label.setText(self.current_country)

if __name__ == "__main__":
    app = QApplication([])
    window = RandomCountryFlagApp()
    window.show()
    app.exec()


