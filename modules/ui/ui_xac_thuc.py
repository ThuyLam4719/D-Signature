from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QLineEdit, QMessageBox, QFileDialog, QTextEdit, QTabWidget # Thêm QTextEdit
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
        layout.setContentsMargins(40, 30, 40, 30)  # left, top, right, bottom
        layout.setSpacing(12)

        # --- Tiêu đề ---
        title = QLabel("Xác Thực Chữ Ký Số")
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)


        #Chọn Khóa Công Khai
        layout.addWidget(QLabel("Khóa Công Khai (Public Key):"))
        self.key_path_input = QLineEdit()
        self.key_path_input.setPlaceholderText("Đường dẫn tới file public key (.pem)")
        self.key_path_input.setReadOnly(True)
        btn_chon_khoa = QPushButton("Chọn")
        btn_chon_khoa.setMinimumHeight(36)
        btn_chon_khoa.clicked.connect(lambda: self.chon_file(
            self.key_path_input, "PEM Public Key (*.pem)", "Chọn Public Key", "public_key"
        ))
        
        h_layout_key = QHBoxLayout()
        h_layout_key.addWidget(self.key_path_input, 3)
        h_layout_key.addWidget(btn_chon_khoa, 1)
        layout.addLayout(h_layout_key)
        
        #Chọn Thông Điệp Gốc - Tab giữa File và Direct Input
        layout.addWidget(QLabel("Thông Điệp Gốc:"))
        
        # Tab widget cho Thông Điệp
        message_tab = QTabWidget()
        message_tab.setMaximumHeight(120)
        
        # Tab 1: Import từ File
        tab_file = QWidget()
        tab_file_layout = QVBoxLayout(tab_file)
        tab_file_layout.setContentsMargins(0, 0, 0, 0)
        self.message_path_input = QLineEdit()
        self.message_path_input.setPlaceholderText("Đường dẫn tới file thông điệp gốc (.txt, .data, ...)")
        self.message_path_input.setReadOnly(True)
        btn_chon_message = QPushButton("Chọn File")
        btn_chon_message.setMinimumHeight(36)
        btn_chon_message.clicked.connect(lambda: self.chon_file(
            self.message_path_input, "Tất cả Files (*);;Text Files (*.txt)", "Chọn File Thông Điệp Gốc", "message"
        ))
        h_layout_msg = QHBoxLayout()
        h_layout_msg.addWidget(self.message_path_input, 3)
        h_layout_msg.addWidget(btn_chon_message, 1)
        tab_file_layout.addLayout(h_layout_msg)
        tab_file.setLayout(tab_file_layout)
        
        # Tab 2: Nhập trực tiếp
        tab_direct = QWidget()
        tab_direct_layout = QVBoxLayout(tab_direct)
        tab_direct_layout.setContentsMargins(0, 0, 0, 0)
        self.message_direct_input = QTextEdit()
        self.message_direct_input.setPlaceholderText("Nhập thông điệp trực tiếp tại đây...")
        self.message_direct_input.setMaximumHeight(80)
        tab_direct_layout.addWidget(self.message_direct_input)
        tab_direct.setLayout(tab_direct_layout)
        
        message_tab.addTab(tab_file, "Import File")
        message_tab.addTab(tab_direct, "Nhập Trực Tiếp")
        layout.addWidget(message_tab)

        #Chọn Chữ Ký
        layout.addWidget(QLabel("Chữ Ký Số:"))
        self.signature_path_input = QLineEdit()
        self.signature_path_input.setPlaceholderText("Đường dẫn tới file chữ ký (.sig, .txt, ...)")
        self.signature_path_input.setReadOnly(True)
        btn_chon_signature = QPushButton("Chọn")
        btn_chon_signature.setMinimumHeight(36)
        btn_chon_signature.clicked.connect(lambda: self.chon_file(
            self.signature_path_input, "Tất cả Files (*);;Signature Files (*.sig)", "Chọn File Chữ Ký Base64", "signature"
        ))
        
        h_layout_sig = QHBoxLayout()
        h_layout_sig.addWidget(self.signature_path_input, 3)
        h_layout_sig.addWidget(btn_chon_signature, 1)
        layout.addLayout(h_layout_sig)


        #Nút Xác Thực
        btn_xac_thuc = QPushButton("Xác Thực Chữ Ký")
        btn_xac_thuc.setMinimumHeight(40)
        btn_xac_thuc.clicked.connect(self.thuc_hien_xac_thuc)
        layout.addWidget(btn_xac_thuc)

        # Vùng hiển thị kết quả (QTextEdit MỚI)
        layout.addWidget(QLabel("Kết Quả và Hash:"))
        self.result_output = QTextEdit()
        self.result_output.setReadOnly(True)
        self.result_output.setMinimumHeight(250)
        self.result_output.setStyleSheet("font-size: 14px;")
        layout.addWidget(self.result_output, 1)  # Thêm stretch factor để chiếm không gian

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
        signature_path = self.signature_path_input.text()

        if not key_path or not signature_path:
            self.result_output.setText("Vui lòng chọn Khóa Công Khai và Chữ Ký Số.")
            return

        # Lấy thông điệp từ file hoặc nhập trực tiếp
        message_path = self.message_path_input.text()
        message_direct = self.message_direct_input.toPlainText().strip()
        
        # Ưu tiên thông điệp nhập trực tiếp, nếu không có thì lấy từ file
        if message_direct:
            thong_diep_raw = message_direct
        elif message_path:
            thong_diep_raw = self.doc_noi_dung_file(message_path, is_signature=False)
            if thong_diep_raw is None:
                return
        else:
            self.result_output.setText("Vui lòng nhập thông điệp hoặc chọn file thông điệp.")
            return

        # Đọc chữ ký từ file
        chu_ky_base64_raw = self.doc_noi_dung_file(signature_path, is_signature=True)
        if chu_ky_base64_raw is None:
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
                f"<b><br>HASH GỐC (từ Thông điệp):</b><br>"  # Dùng <b> cho in đậm
                f"<br>{hash_goc}<br><br>"
                f"<b>HASH GIẢI MÃ (từ Chữ ký):</b><br>"
                f"<br>{hash_giai_ma}<br><br>"
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