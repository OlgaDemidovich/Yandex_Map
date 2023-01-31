import os
import sys
import random

import requests
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel

SCREEN_SIZE = [1000, 750]


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.coords = random.randrange(-180000000, 180000000), random.randrange(-90000000, 90000000)
        self.coords = (71431220, 51156987)
        self.param_z = 1
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Yandex Maps')
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(1000, 750)
        self.getImage()

    def getImage(self):

        map_request = f"http://static-maps.yandex.ru/1.x/?ll={self.coords[0] / 1000000},{self.coords[1] / 1000000}" \
                      f"&l=map&z={self.param_z}"
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        # Запишем полученное изображение в файл.
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

        self.update()
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)
        print('a')

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_PageUp:
            self.param_z -= 1
            if self.param_z < 1:
                self.param_z = 1
            self.getImage()
        if event.key() == QtCore.Qt.Key_PageDown:
            self.param_z += 1
            if self.param_z > 17:
                self.param_z = 17
            self.getImage()

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec())
