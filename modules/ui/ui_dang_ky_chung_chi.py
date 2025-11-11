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

        self.label_priv = QLabel("Chọn file khóa bí mật (private key):")
        self.input_priv = QLineEdit()
        self.btn_chon_priv = QPushButton("Chọn private key...")

        self.btn_gui_yeu_cau = QPushButton("Gửi yêu cầu đến CA")

        layout_key = QHBoxLayout()
        layout_key.addWidget(self.input_priv)
        layout_key.addWidget(self.btn_chon_priv)

        layout = QVBoxLayout()
        layout.addWidget(self.label_name)
        layout.addWidget(self.input_name)
        layout.addWidget(self.label_org)
        layout.addWidget(self.input_org)
        layout.addWidget(self.label_country)
        layout.addWidget(self.input_country)
        layout.addWidget(self.label_priv)
        layout.addLayout(layout_key)
        layout.addWidget(self.btn_gui_yeu_cau)

        self.setLayout(layout)

        self.btn_chon_priv.clicked.connect(self.chon_priv)
        self.btn_gui_yeu_cau.clicked.connect(self.gui_yeu_cau)

    def chon_priv(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Chọn khóa bí mật (PEM)", "data/keys", "PEM Files (*.pem)"
        )
        if file_path:
            self.input_priv.setText(file_path)

    def gui_yeu_cau(self):
        cn = self.input_name.text().strip()
        org = self.input_org.text().strip()
        country = self.input_country.text().strip()
        priv_path = self.input_priv.text().strip()

        if not all([cn, org, country, priv_path]):
            QMessageBox.warning(self, "Thiếu thông tin", "Điền đầy đủ thông tin trước khi gửi.")
            return

        result = certRequest.gui_yeu_cau(priv_path, cn, org, country)

        if result == "OK":
            QMessageBox.information(self, "Thành công", "Yêu cầu chứng chỉ đã gửi tới CA.")
        else:
            QMessageBox.critical(self, "Lỗi", f"Gửi yêu cầu thất bại: {result}")
