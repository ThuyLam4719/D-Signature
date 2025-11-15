from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QLineEdit, QMessageBox, QFileDialog, QTextEdit # Thêm QTextEdit
)
from PySide6.QtCore import Qt
import os
import re 

from modules.verifySign import xac_thuc_chu_ky 

class WidgetXacThuc(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Xác thực Chữ ký")
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop) # Căn chỉnh layout

        # --- Tiêu đề ---
        title = QLabel("Xác Thực Chữ Ký Số")
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)


        #Chọn Khóa Công Khai
        layout.addWidget(QLabel("1. Khóa Công Khai (Public Key):"))
        self.key_path_input = QLineEdit()
        self.key_path_input.setPlaceholderText("Đường dẫn tới file public key (.pem)")
        self.key_path_input.setReadOnly(True)
        btn_chon_khoa = QPushButton("Chọn File Khóa")
        btn_chon_khoa.clicked.connect(lambda: self.chon_file(
            self.key_path_input, "PEM Public Key (*.pem)", "Chọn Public Key", "public_key"
        ))
        
        h_layout_key = QHBoxLayout()
        h_layout_key.addWidget(self.key_path_input, 3)
        h_layout_key.addWidget(btn_chon_khoa, 1)
        layout.addLayout(h_layout_key)
        
        #Chọn Thông Điệp Gốc
        layout.addWidget(QLabel("2. Thông Điệp Gốc (File đã được ký):"))
        self.message_path_input = QLineEdit()
        self.message_path_input.setPlaceholderText("Đường dẫn tới file thông điệp gốc (.txt, .data, ...)")
        self.message_path_input.setReadOnly(True)
        btn_chon_message = QPushButton("Chọn File Thông Điệp")
        btn_chon_message.clicked.connect(lambda: self.chon_file(
            self.message_path_input, "Tất cả Files (*);;Text Files (*.txt)", "Chọn File Thông Điệp Gốc", "message"
        ))
        
        h_layout_msg = QHBoxLayout()
        h_layout_msg.addWidget(self.message_path_input, 3)
        h_layout_msg.addWidget(btn_chon_message, 1)
        layout.addLayout(h_layout_msg)

        #Chọn Chữ Ký
        layout.addWidget(QLabel("3. Chữ Ký Số (File Base64):"))
        self.signature_path_input = QLineEdit()
        self.signature_path_input.setPlaceholderText("Đường dẫn tới file chữ ký (.sig, .txt, ...)")
        self.signature_path_input.setReadOnly(True)
        btn_chon_signature = QPushButton("Chọn File Chữ Ký")
        btn_chon_signature.clicked.connect(lambda: self.chon_file(
            self.signature_path_input, "Tất cả Files (*);;Signature Files (*.sig)", "Chọn File Chữ Ký Base64", "signature"
        ))
        
        h_layout_sig = QHBoxLayout()
        h_layout_sig.addWidget(self.signature_path_input, 3)
        h_layout_sig.addWidget(btn_chon_signature, 1)
        layout.addLayout(h_layout_sig)


        #Nút Xác Thực
        btn_xac_thuc = QPushButton("Xác Thực Chữ Ký")
        btn_xac_thuc.setStyleSheet("background-color: #007bff; color: white; font-weight: bold; padding: 10px;")
        btn_xac_thuc.clicked.connect(self.thuc_hien_xac_thuc)
        layout.addWidget(btn_xac_thuc)

        # Vùng hiển thị kết quả (QTextEdit MỚI)
        layout.addWidget(QLabel("4. Kết Quả và Hash:"))
        self.result_output = QTextEdit()
        self.result_output.setReadOnly(True)
        self.result_output.setFixedHeight(200)
        layout.addWidget(self.result_output)

        layout.addStretch()
        self.setLayout(layout)

    def chon_file(self, line_edit, name_filter, caption, file_type):
        """Hàm chung để mở hộp thoại chọn file"""
        dialog = QFileDialog(self)
        dialog.setWindowTitle(caption)
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.setNameFilter(name_filter)

        if dialog.exec():
            selected_files = dialog.selectedFiles()
            if selected_files:
                file_path = selected_files[0]
                line_edit.setText(file_path)
                # Giữ lại QMessageBox thông báo đã chọn file (tùy chọn)
                QMessageBox.information(self, "Đã chọn", f"Đã chọn file {file_type}: {os.path.basename(file_path)}")
    
    def doc_noi_dung_file(self, file_path, is_signature=False):
        """Đọc nội dung file và xử lý Base64 nghiêm ngặt"""
        if not file_path:
            return None
        try:
            # Đọc file nhị phân nếu không phải chữ ký (để đảm bảo tính toàn vẹn của dữ liệu)
            mode = "r"
            encoding = "utf-8"
            if not is_signature:
                # Nếu là thông điệp gốc (data), đọc dưới dạng bytes (mode="rb")
                # Tuy nhiên, nếu hàm xac_thuc_chu_ky yêu cầu string, ta giữ 'r'
                # Giả định xac_thuc_chu_ky nhận chuỗi string/bytes sạch.
                pass 
                
            with open(file_path, mode, encoding=encoding) as f:
                content = f.read()
            
            # Nếu là chữ ký, loại bỏ tất cả khoảng trắng, tab, xuống dòng bên trong chuỗi Base64
            if is_signature:
                content = re.sub(r'\s+', '', content)
                
            return content

        except Exception as e:
            QMessageBox.critical(self, "Lỗi đọc file", f"Không thể đọc file {file_path}: {str(e)}")
            return None

    def thuc_hien_xac_thuc(self):
        """Thực hiện xác thực chữ ký số và hiển thị hash vào QTextEdit"""
        self.result_output.clear()
        
        key_path = self.key_path_input.text()
        message_path = self.message_path_input.text()
        signature_path = self.signature_path_input.text()

        if not key_path or not message_path or not signature_path:
            self.result_output.setText("Vui lòng chọn đủ 3 file (Khóa, Thông điệp, Chữ ký).")
            return

        # Đọc nội dung thông điệp và chữ ký từ file
        thong_diep_raw = self.doc_noi_dung_file(message_path, is_signature=False)
        chu_ky_base64_raw = self.doc_noi_dung_file(signature_path, is_signature=True)

        if thong_diep_raw is None or chu_ky_base64_raw is None:
            return

        # Áp dụng .strip() cuối cùng để loại bỏ ký tự trắng ở đầu/cuối
        thong_diep_clean = thong_diep_raw.strip()
        chu_ky_base64_clean = chu_ky_base64_raw.strip() 

        try:
            # Gọi hàm xác thực (Nhận về tuple: (bool, hash_gốc, hash_giải_mã))
            ket_qua, hash_goc, hash_giai_ma = xac_thuc_chu_ky(
                key_path,
                thong_diep_clean,
                chu_ky_base64_clean
            )
            
            # Chuẩn bị thông báo hiển thị trên QTextEdit
            hash_msg = (
                f"**HASH GỐC (từ Thông điệp):**\n"
                f"```\n{hash_goc}\n```\n\n"
                f"**HASH GIẢI MÃ (từ Chữ ký):**\n"
                f"```\n{hash_giai_ma}\n```"
            )
            
            if ket_qua:
                # Nếu thành công, H1 và H2 đã khớp
                thong_bao = (
                    "<h3 style='color: green;'>CHỮ KÝ HỢP LỆ</h3>"
                    "Thông điệp không bị thay đổi (Hash Gốc == Hash Giải mã).\n\n"
                    f"{hash_msg}"
                )
            else:
                # Nếu thất bại, hiển thị cả hai hash
                thong_bao = (
                    "<h3 style='color: red;'>CHỮ KÝ KHÔNG HỢP LỆ</h3>"
                    "Thông điệp đã bị thay đổi, hoặc chữ ký/khóa không đúng.\n\n"
                    f"{hash_msg}"
                )
            
            # Thiết lập nội dung cho QTextEdit, dùng HTML để làm nổi bật kết quả
            self.result_output.setText(thong_bao)
            self.result_output.ensureCursorVisible()

        except Exception as e:
            self.result_output.setText(f"<h3 style='color: red;'>LỖI XỬ LÝ CHỮ KÝ</h3>Không thể thực hiện xác thực: {e}")