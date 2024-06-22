import sys

from PyQt5.QtCore import Qt, pyqtSignal, QTimer, QPoint
from PyQt5.QtGui import QPixmap, QMouseEvent
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QFileDialog, \
    QLineEdit

from cipher.alg import encrypt_image, decrypt_image


class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super(ClickableLabel, self).__init__(parent)

    def mousePressEvent(self, event):
        self.clicked.emit()


class ClickableLabelCopy(QLabel):
    def __init__(self, text='', parent=None):
        super().__init__(text, parent)
        self.setText(text)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            QApplication.clipboard().setText(self.text())
            self.parent().show_copy_message(self.mapToGlobal(event.pos()))
            # print("Text copied to clipboard:", self.text())
        super().mousePressEvent(event)


def encrypt(image_path: str, message: str) -> (bytes, bytes):
    encrypted_data, key = encrypt_image(
        image_path,
        message,
    )
    return encrypted_data, key.hex()


def decrypt(image_path: str, key: str) -> str:
    # Заглушка для функции дешифрования
    key = bytes.fromhex(key)
    decrypted_message = decrypt_image(
        image_path,
        key
    )
    return decrypted_message


class ImageCipherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Шифрование и Дешифрование Изображений')
        self.setGeometry(300, 300, 800, 600)

        button_style = "QPushButton { background-color: #007BFF; font-size: 14px; color: white; font-weight: bold; padding: 10px; }"
        label_style = "QLabel { background-color: #F0F0F0; font-size: 14px; padding: 10px; border: 1px solid #DDD; }"
        default_label_style = "QLabel { background-color: #F0F0F0; font-size: 14px; padding: 4px;}"
        big_bold_label_style = "QLabel { background-color: #F0F0F0; font-size: 18px; padding: 10px; font: bold;}"

        # Макеты
        message_layout = QHBoxLayout()
        params_encrypt_layout_1 = QHBoxLayout()

        original_layout = QVBoxLayout()
        display_result_layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        # Добавление всех макетов (Виджетов)
        label_message = QLabel('Сообщение:')
        self.message = QLineEdit()
        self.message.setPlaceholderText("Введите сообщения для шифрования")
        message_layout.addWidget(label_message)
        message_layout.addWidget(self.message)

        key_label = QLabel("Ключ:")
        self.key = QLineEdit()
        self.key.setPlaceholderText("Введите ключ")
        params_encrypt_layout_1.addWidget(key_label)
        params_encrypt_layout_1.addWidget(self.key)

        # Image and path labels
        self.encryption_label = QLabel('Выбранная картинка')
        self.encryption_label.setAlignment(Qt.AlignCenter)
        self.encryption_label.setStyleSheet("QLabel { margin-top: 2px; margin-bottom: 2px; }")
        self.encryption_label.setMaximumHeight(20)
        self.original_image_label = ClickableLabel('Кликните для загрузки изображения')
        self.original_image_label.setAlignment(Qt.AlignCenter)
        self.original_path_label = QLabel('Путь не выбран')
        self.original_path_label.setVisible(False)

        # Вывод данных после шифрования
        self.encrypted_image_data = b""
        self.label_for_key_to_encrypted_image = QLabel("Полученный ключ: ")
        self.label_for_key_to_encrypted_image.setVisible(False)
        self.key_to_encrypted_image = ClickableLabelCopy()
        self.key_to_encrypted_image.setVisible(False)
        ttt = QHBoxLayout()
        ttt.addWidget(self.label_for_key_to_encrypted_image)
        ttt.addWidget(self.key_to_encrypted_image)
        display_result_layout.addLayout(ttt)

        # Вывод данных после Дешифрования
        self.label_for_decrypted_message = QLabel("Полученное сообщение: ")
        self.label_for_decrypted_message.setVisible(False)
        self.decrypted_message = ClickableLabelCopy()
        self.decrypted_message.setVisible(False)
        ttt = QHBoxLayout()
        ttt.addWidget(self.label_for_decrypted_message)
        ttt.addWidget(self.decrypted_message)
        display_result_layout.addLayout(ttt)

        self.copy_message = QLabel('Текст скопирован!', self)
        self.copy_message.setStyleSheet("background-color: gray; color: white; padding: 10px;")
        self.copy_message.setAlignment(Qt.AlignCenter)
        self.copy_message.setVisible(False)
        self.copy_message.setWindowFlags(Qt.ToolTip)

        # Кнопки
        self.load_button = QPushButton('Загрузить изображение')
        self.encrypt_button = QPushButton('Шифровать')
        self.decrypt_button = QPushButton('Дешифровать')
        self.save_button = QPushButton('Сохранить')

        # Стили
        self.load_button.setStyleSheet(button_style)
        self.encrypt_button.setStyleSheet(button_style)
        self.decrypt_button.setStyleSheet(button_style)
        self.save_button.setStyleSheet(button_style)
        self.original_image_label.setStyleSheet(label_style)
        self.message.setStyleSheet(default_label_style)
        label_message.setStyleSheet(default_label_style)
        key_label.setStyleSheet(default_label_style)
        # self.label_q_const.setStyleSheet(default_label_style)
        # self.label_n_iterations.setStyleSheet(default_label_style)
        self.label_for_key_to_encrypted_image.setStyleSheet(big_bold_label_style)
        self.label_for_decrypted_message.setStyleSheet(big_bold_label_style)
        self.key_to_encrypted_image.setStyleSheet(big_bold_label_style)
        self.decrypted_message.setStyleSheet(big_bold_label_style)

        # Добавление элементов в оригинальный вертикальный макет
        original_layout.addWidget(self.encryption_label)
        original_layout.addWidget(self.original_image_label)
        original_layout.addWidget(self.original_path_label)

        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.encrypt_button)
        button_layout.addWidget(self.decrypt_button)
        button_layout.addWidget(self.save_button)

        # Добавление всех макетов в главный виджет
        final_layout = QVBoxLayout()
        final_layout.addLayout(message_layout)
        final_layout.addLayout(params_encrypt_layout_1)
        final_layout.addStretch(1)
        final_layout.addLayout(original_layout)
        final_layout.addStretch(1)
        final_layout.addLayout(display_result_layout)
        final_layout.addLayout(button_layout)
        self.setLayout(final_layout)

        # Connections
        self.load_button.clicked.connect(self.load_image)
        self.encrypt_button.clicked.connect(self.encrypt_image)
        self.decrypt_button.clicked.connect(self.decrypt_image)
        self.save_button.clicked.connect(self.save_image)
        self.original_image_label.clicked.connect(self.load_image)

    def show_copy_message(self, position: QPoint):
        self.copy_message.move(position)
        self.copy_message.setVisible(True)
        self.copy_message.raise_()  # Поднимаем виджет на передний план
        QTimer.singleShot(2000, self.hide_copy_message)  # Hide after 2 seconds

    def hide_copy_message(self):
        self.copy_message.setVisible(False)

    def load_image(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Выберите изображение', '', 'Image files (*.jpg *.png)')
        if filename:
            self.original_pixmap = QPixmap(filename)
            self.original_image_label.setPixmap(self.original_pixmap.scaled(400, 400, Qt.KeepAspectRatio))
            self.original_path_label.setText(filename)
            self.original_path_label.setVisible(True)
            self.current_image = filename

    def encrypt_image(self):
        if hasattr(self, 'current_image'):
            encrypted_data, key = encrypt(
                self.current_image,
                self.message.text().strip()
            )
            self.encrypted_image_data = encrypted_data
            # Отобразим ключ
            self.key_to_encrypted_image.setText(f"{key}")
            self.label_for_key_to_encrypted_image.setVisible(True)
            self.key_to_encrypted_image.setVisible(True)
            self.save_image()

    def decrypt_image(self):
        if hasattr(self, 'current_image'):
            decrypted_message = decrypt(
                self.current_image,
                self.key.text().strip()
            )
            self.decrypted_message.setText(f"{decrypted_message}")
            self.label_for_decrypted_message.setVisible(True)
            self.decrypted_message.setVisible(True)

    def save_image(self):
        filename, _ = QFileDialog.getSaveFileName(self, 'Сохранить изображение', '', 'Image files (*.jpg *.png)')
        if filename:
            with open(filename, 'wb') as f:
                f.write(self.encrypted_image_data)
