from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QTextEdit, QPushButton,
    QVBoxLayout, QFileDialog, QMessageBox, QHBoxLayout
)
from PySide6.QtCore import Qt
import os
# Đảm bảo đường dẫn import này đúng, nếu modules nằm ngang hàng signData.py thì cần sửa
from modules import signData


class WidgetKyDuLieu(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tạo Chữ Ký")

        # Biến lưu đường dẫn file cần ký và nơi lưu chữ ký
        self.duong_dan_file = None
        self.duong_dan_luu = None

        # Các thành phần giao diện 
        title = QLabel("Tạo Chữ Ký")
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 10px;")
        
        self.nhan_khoa = QLabel("Chọn file khóa bí mật:")
        self.o_khoa = QLineEdit()
        self.nut_chon_khoa = QPushButton("Chọn khóa...")
        self.nut_chon_khoa.setMinimumHeight(36)

        self.nhan_thong_diep = QLabel("Nhập thông điệp hoặc chọn file để ký:")
        self.nut_chon_file = QPushButton("Chọn file cần ký")
        self.nut_chon_file.setMinimumHeight(36)
        self.nhan_file_da_chon = QLabel("(Chưa chọn file)")
        self.o_thong_diep = QTextEdit()

        # Phần chọn nơi lưu chữ ký  
        self.nhan_luu = QLabel("Nơi lưu file chữ ký:")
        self.o_noi_luu = QLineEdit()
        self.o_noi_luu.setPlaceholderText("Chưa chọn nơi lưu...")
        self.nut_chon_luu = QPushButton("Chọn nơi lưu trữ")
        self.nut_chon_luu.setMinimumHeight(36)
        self.nut_ky = QPushButton("Ký dữ liệu")
        self.nut_ky.setMinimumHeight(40)

        # Layout khóa 
        layout_khoa = QHBoxLayout()
        layout_khoa.addWidget(self.o_khoa)
        layout_khoa.addWidget(self.nut_chon_khoa)

        # Layout chọn file
        layout_file = QHBoxLayout()
        layout_file.addWidget(self.nut_chon_file)
        layout_file.addWidget(self.nhan_file_da_chon)

        # Layout nơi lưu chữ ký
        layout_luu = QHBoxLayout()
        layout_luu.addWidget(self.o_noi_luu)
        layout_luu.addWidget(self.nut_chon_luu)

        # Layout chính
        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.setContentsMargins(40, 30, 40, 30)  # left, top, right, bottom
        layout.setSpacing(12)
        layout.addWidget(self.nhan_khoa)
        layout.addLayout(layout_khoa)
        layout.addWidget(self.nhan_thong_diep)
        layout.addLayout(layout_file)
        layout.addWidget(self.o_thong_diep)
        layout.addWidget(self.nhan_luu)
        layout.addLayout(layout_luu)
        layout.addWidget(self.nut_ky)
        self.setLayout(layout)

        # Kết nối sự kiện
        self.nut_chon_khoa.clicked.connect(self.chon_file_khoa)
        self.nut_chon_file.clicked.connect(self.chon_file_can_ky)
        self.nut_chon_luu.clicked.connect(self.chon_noi_luu)
        self.nut_ky.clicked.connect(self.thuc_hien_ky_du_lieu) # Đổi tên hàm

    # ----------------------------
    #   Các hàm chức năng giao diện
    # ----------------------------

    def doc_noi_dung_file(self, file_path):
        """Đọc toàn bộ nội dung file dưới dạng string."""
        try:
            # Đọc ở chế độ văn bản để lấy string, sử dụng 'errors="ignore"' cho an toàn
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi đọc file", f"Không thể đọc file: {str(e)}")
            return None

    def chon_file_khoa(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Chọn khóa bí mật", "data/keys", "PEM Files (*.pem)"
        )
        if file_path:
            self.o_khoa.setText(file_path)

    def chon_file_can_ky(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Chọn file cần ký", "data/files", "Tất cả các file (*)"
        )
        if file_path:
            self.duong_dan_file = file_path
            ten_file = os.path.basename(file_path)
            self.nhan_file_da_chon.setText(f"Đã chọn: {ten_file}")
            
            # Đọc nội dung file để hiển thị
            noi_dung_goc = self.doc_noi_dung_file(file_path)
            
            if noi_dung_goc is not None:
                # Hiển thị 4 dòng đầu
                dong = noi_dung_goc.splitlines()
                xem_truoc = "\n".join(dong[:4])
                if len(dong) > 4:
                    xem_truoc += "\n..."
                self.o_thong_diep.setPlainText(xem_truoc)


    def chon_noi_luu(self):
        """Chọn nơi lưu và đặt tên file chữ ký"""
        goi_y_ten = "chu_ky.sig"
        if self.duong_dan_file:
            ten_file = os.path.splitext(os.path.basename(self.duong_dan_file))[0]
            goi_y_ten = f"{ten_file}_chu_ky.sig"

        duong_dan, _ = QFileDialog.getSaveFileName(
            self,
            "Chọn nơi lưu và đặt tên file chữ ký",
            f"data/files/{goi_y_ten}",
            "File chữ ký (*.sig)"
        )

        if duong_dan:
            if not duong_dan.endswith(".sig"):
                duong_dan += ".sig"
            self.duong_dan_luu = duong_dan
            self.o_noi_luu.setText(duong_dan)

    # ----------------------------
    #   Hàm thực hiện ký
    # ----------------------------
    def thuc_hien_ky_du_lieu(self):
        duong_dan_khoa = self.o_khoa.text().strip()
        thong_diep_input = self.o_thong_diep.toPlainText() # Lấy nội dung từ textbox

        # 1. Xác định nội dung thông điệp gốc
        thong_diep_goc = None
        if self.duong_dan_file:
            # Nếu chọn file, phải đọc lại toàn bộ nội dung
            thong_diep_goc = self.doc_noi_dung_file(self.duong_dan_file)
            if thong_diep_goc is None: return
        elif thong_diep_input.strip():
            # Nếu chỉ nhập text vào ô
            thong_diep_goc = thong_diep_input
        else:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập thông điệp hoặc chọn file để ký!")
            return

        # 2. Kiểm tra khóa bí mật
        if not duong_dan_khoa or not os.path.exists(duong_dan_khoa):
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn khóa bí mật hợp lệ!")
            return
        
        # 3. Ký: Bắt buộc phải .strip() để loại bỏ tất cả ký tự trắng thừa
        # Đây là bước quan trọng nhất để khớp với xác thực.
        thong_diep_clean = thong_diep_goc.strip()

        # Gọi hàm ký
        chu_ky = signData.ky_du_lieu(duong_dan_khoa, thong_diep_clean) # <-- TRUYỀN DỮ LIỆU ĐÃ CLEAN

        if chu_ky.startswith("Lỗi"):
            QMessageBox.critical(self, "Ký thất bại", chu_ky)
            return

        # 4. Lưu chữ ký vào file
        if not self.duong_dan_luu:
            self.chon_noi_luu()
            if not self.duong_dan_luu:
                QMessageBox.information(self, "Hủy", "Bạn đã hủy lưu chữ ký.")
                return

        try:
            with open(self.duong_dan_luu, "w") as f:
                f.write(chu_ky)
            QMessageBox.information(
                self,
                "Thành công",
                f"Ký thành công!\nChữ ký đã lưu tại:\n{self.duong_dan_luu}",
            )
        except Exception as e:
            QMessageBox.critical(self, "Lỗi lưu file", f"Không thể lưu chữ ký:\n{str(e)}")