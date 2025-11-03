from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QVBoxLayout,
    QFileDialog, QMessageBox, QHBoxLayout
)
import os
from modules import certRequest

class WidgetDangKyChungChi(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Yêu cầu cấp chứng chỉ")

        self.label_name = QLabel("Tên người dùng (CN):")
        self.input_name = QLineEdit()

        self.label_org = QLabel("Tổ chức:")
        self.input_org = QLineEdit()

        self.label_country = QLabel("Quốc gia (VN, US...):")
        self.input_country = QLineEdit()

        self.label_pubkey = QLabel("Chọn file khóa công khai:")
        self.input_pubkey = QLineEdit()
        self.btn_chon_pubkey = QPushButton("Chọn khóa...")

        self.btn_gui_yeu_cau = QPushButton("Gửi yêu cầu đến CA")

        layout_key = QHBoxLayout()
        layout_key.addWidget(self.input_pubkey)
        layout_key.addWidget(self.btn_chon_pubkey)

        layout = QVBoxLayout()
        layout.addWidget(self.label_name)
        layout.addWidget(self.input_name)
        layout.addWidget(self.label_org)
        layout.addWidget(self.input_org)
        layout.addWidget(self.label_country)
        layout.addWidget(self.input_country)
        layout.addWidget(self.label_pubkey)
        layout.addLayout(layout_key)
        layout.addWidget(self.btn_gui_yeu_cau)

        self.setLayout(layout)

        self.btn_chon_pubkey.clicked.connect(self.chon_pubkey)
        self.btn_gui_yeu_cau.clicked.connect(self.gui_yeu_cau)

    def chon_pubkey(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Chọn khóa công khai", "data/keys", "PEM Files (*.pem)"
        )
        if file_path:
            self.input_pubkey.setText(file_path)

    def gui_yeu_cau(self):
        cn = self.input_name.text().strip()
        org = self.input_org.text().strip()
        country = self.input_country.text().strip()
        pubkey_path = self.input_pubkey.text().strip()

        if not all([cn, org, country, pubkey_path]):
            QMessageBox.warning(self, "Thiếu thông tin", "Điền đầy đủ thông tin trước khi gửi.")
            return

        result = certRequest.gui_yeu_cau(pubkey_path, cn, org, country)

        if result == "OK":
            QMessageBox.information(self, "Thành công", "✅ Yêu cầu chứng chỉ đã gửi tới CA.")
        else:
            QMessageBox.critical(self, "Lỗi", f"Gửi yêu cầu thất bại: {result}")
