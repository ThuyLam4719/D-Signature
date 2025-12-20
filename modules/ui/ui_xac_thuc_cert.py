# modules/ui/ui_xac_thuc_cert.py

from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTextEdit, QFileDialog
)
from PySide6.QtCore import Qt

from modules.verifyCertByPub import verify_certificate 
import os

class WidgetXacThucCert(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Xác thực Chứng chỉ")
        # Khai báo biến đường dẫn (chủ yếu dùng cho tham chiếu ban đầu)
        self.cert_path = ""
        self.ca_pub_path = ""
        self.output_pub_path = ""
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 30, 40, 30)  # left, top, right, bottom
        main_layout.setSpacing(12)

        # --- 1. Tiêu đề ---
        title = QLabel("Xác Thực Chứng Chỉ Số")
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 10px; color: #00b8d4;")
        main_layout.addWidget(title)
        
        # ------------------- 2. Vùng Chọn File Chứng Chỉ -------------------
        cert_group_layout, self.cert_path_input = self._create_file_selection_group(
            "Đường dẫn Chứng chỉ:", 
            self._select_cert_file,
            is_input=True
        )
        main_layout.addLayout(cert_group_layout)

        # ------------------- 3. Vùng Chọn Public Key của CA -------------------
        ca_pub_group_layout, self.ca_pub_path_input = self._create_file_selection_group(
            "Public Key của CA:", 
            self._select_ca_pub_file,
            is_input=True
        )
        main_layout.addLayout(ca_pub_group_layout)
        
        # ------------------- 4. Vùng Chọn Nơi Lưu Public Key -------------------
        output_pub_group_layout, self.output_pub_path_input = self._create_file_selection_group(
            "Lưu Public Key trích xuất:",
            self._select_output_pub_file,
            is_input=False
        )
        main_layout.addLayout(output_pub_group_layout)

        # ------------------- 5. Nút Thực hiện và Kết quả -------------------
        self.verify_button = QPushButton("Xác Thực Chứng Chỉ")
        self.verify_button.setMinimumHeight(40)
        self.verify_button.clicked.connect(self._verify_cert)
        main_layout.addWidget(self.verify_button)

        # Vùng Kết quả
        result_label = QLabel("Kết quả và Thông tin Chứng chỉ:")
        result_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        main_layout.addWidget(result_label)
        
        self.result_output = QTextEdit()
        self.result_output.setReadOnly(True)
        self.result_output.setMinimumHeight(300)
        self.result_output.setStyleSheet("font-size: 14px;")
        main_layout.addWidget(self.result_output, 1)
        
        main_layout.addStretch()


    # --- Hàm Helper TỔNG HỢP để tạo Layout chọn file ---
    def _create_file_selection_group(self, label_text, button_slot, is_input=True):
        """Tạo một nhóm widget (label, input, button) để chọn file."""
        h_layout = QHBoxLayout()
        label = QLabel(label_text)
        label.setFixedWidth(200)

        input_field = QLineEdit()
        
        browse_button = QPushButton("Chọn" if is_input else "Lưu")
        browse_button.setFixedWidth(100)
        browse_button.setMinimumHeight(36)
        browse_button.clicked.connect(button_slot)

        h_layout.addWidget(label)
        h_layout.addWidget(input_field)
        h_layout.addWidget(browse_button)
        return h_layout, input_field

    # --- Slots Xử lý Chọn File Đầu vào ---
    def _select_cert_file(self):
        """Chọn file chứng chỉ."""
        file_name, _ = QFileDialog.getOpenFileName(self, "Chọn Chứng chỉ X.509", "", "Certificate Files (*.pem *.crt);;All Files (*)")
        if file_name:
            self.cert_path = file_name
            self.cert_path_input.setText(file_name)
            
            # Đề xuất tên file đầu ra Public Key theo tên chứng chỉ
            base_name = os.path.splitext(file_name)[0]
            default_output = f"{base_name}_pub.pem"
            self.output_pub_path_input.setText(default_output)

    def _select_ca_pub_file(self):
        """Chọn Public Key của CA."""
        file_name, _ = QFileDialog.getOpenFileName(self, "Chọn Public Key của CA", "", "Public Key Files (*.pem);;All Files (*)")
        if file_name:
            self.ca_pub_path = file_name
            self.ca_pub_path_input.setText(file_name)

    # --- Slots Xử lý Chọn File Đầu ra ---
    def _select_output_pub_file(self):
        """Chọn nơi lưu và tên file Public Key trích xuất."""
        # Lấy tên file mặc định từ input (nếu có)
        default_file_name = self.output_pub_path_input.text() if self.output_pub_path_input.text() else "certificate_pub.pem"
        
        file_name, _ = QFileDialog.getSaveFileName(self, "Lưu Public Key Trích Xuất", default_file_name, "PEM Public Key (*.pem);;All Files (*)")
        if file_name:
            self.output_pub_path_input.setText(file_name)


    # --- Hàm Xử lý Xác thực ---
    def _verify_cert(self):
        """Thực hiện xác thực chứng chỉ."""
        self.result_output.clear()
        
        cert_path = self.cert_path_input.text()
        ca_pub_path = self.ca_pub_path_input.text()
        output_pub_path = self.output_pub_path_input.text()
        
        if not cert_path or not ca_pub_path or not output_pub_path:
            self.result_output.setText("Vui lòng chọn đủ file Chứng chỉ, Public Key của CA, và chỉ định nơi lưu Public Key.")
            return

        try:
            # Gọi hàm backend với 3 tham số (Đã đồng bộ với verifyCertByPub.py)
            is_valid, result_text = verify_certificate(cert_path, ca_pub_path, output_pub_path)
            
            # Hiển thị kết quả
            self.result_output.setText(result_text)

        except Exception as e:
            self.result_output.setText(f"LỖI HỆ THỐNG XẢY RA:\n{e}")

# --- Test giao diện (Tùy chọn) ---
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = WidgetXacThucCert()
    window.show()
    sys.exit(app.exec())