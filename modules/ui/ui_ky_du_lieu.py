from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QTextEdit, QPushButton,
    QVBoxLayout, QFileDialog, QMessageBox, QHBoxLayout
)
import os
from modules import signData


class WidgetKyDuLieu(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ký dữ liệu")

        # Biến lưu đường dẫn file cần ký và nơi lưu chữ ký
        self.duong_dan_file = None
        self.duong_dan_luu = None

        # --- Các thành phần giao diện ---
        self.nhan_khoa = QLabel("Chọn file khóa bí mật:")
        self.o_khoa = QLineEdit()
        self.nut_chon_khoa = QPushButton("Chọn khóa...")

        self.nhan_thong_diep = QLabel("Nhập thông điệp hoặc chọn file để ký:")
        self.nut_chon_file = QPushButton("Chọn file cần ký")
        self.nhan_file_da_chon = QLabel("(Chưa chọn file)")
        self.o_thong_diep = QTextEdit()

        # --- Phần chọn nơi lưu chữ ký ---
        self.nhan_luu = QLabel("Nơi lưu file chữ ký:")
        self.o_noi_luu = QLineEdit()
        self.o_noi_luu.setPlaceholderText("Chưa chọn nơi lưu...")
        self.nut_chon_luu = QPushButton("Chọn nơi lưu trữ")
        self.nut_ky = QPushButton("Ký dữ liệu")

        # --- Layout khóa ---
        layout_khoa = QHBoxLayout()
        layout_khoa.addWidget(self.o_khoa)
        layout_khoa.addWidget(self.nut_chon_khoa)

        # --- Layout chọn file ---
        layout_file = QHBoxLayout()
        layout_file.addWidget(self.nut_chon_file)
        layout_file.addWidget(self.nhan_file_da_chon)

        # --- Layout nơi lưu chữ ký ---
        layout_luu = QHBoxLayout()
        layout_luu.addWidget(self.o_noi_luu)
        layout_luu.addWidget(self.nut_chon_luu)

        # --- Layout chính ---
        layout = QVBoxLayout()
        layout.addWidget(self.nhan_khoa)
        layout.addLayout(layout_khoa)
        layout.addWidget(self.nhan_thong_diep)
        layout.addLayout(layout_file)
        layout.addWidget(self.o_thong_diep)
        layout.addWidget(self.nhan_luu)
        layout.addLayout(layout_luu)
        layout.addWidget(self.nut_ky)
        self.setLayout(layout)

        # --- Kết nối sự kiện ---
        self.nut_chon_khoa.clicked.connect(self.chon_file_khoa)
        self.nut_chon_file.clicked.connect(self.chon_file_can_ky)
        self.nut_chon_luu.clicked.connect(self.chon_noi_luu)
        self.nut_ky.clicked.connect(self.ky_du_lieu)

    # ----------------------------
    #  Các hàm chức năng giao diện
    # ----------------------------

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
            # Hiển thị 4 dòng đầu của nội dung file
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    dong = f.readlines()
                    xem_truoc = "".join(dong[:4])
                    if len(dong) > 4:
                        xem_truoc += "\n..."
                    self.o_thong_diep.setPlainText(xem_truoc)
            except Exception as e:
                self.o_thong_diep.setPlainText(f"Lỗi đọc file: {str(e)}")

    def chon_noi_luu(self):
        """Chọn nơi lưu và đặt tên file chữ ký"""
        goi_y_ten = "chu_ky.sig"
        if self.duong_dan_file:
            # Nếu đang ký file, gợi ý tên chữ ký theo tên file
            ten_file = os.path.splitext(os.path.basename(self.duong_dan_file))[0]
            goi_y_ten = f"{ten_file}_chu_ky.sig"

        duong_dan, _ = QFileDialog.getSaveFileName(
            self,
            "Chọn nơi lưu và đặt tên file chữ ký",
            f"data/files/{goi_y_ten}",
            "File chữ ký (*.sig)"
        )

        if duong_dan:
            # Đảm bảo đuôi file là .sig
            if not duong_dan.endswith(".sig"):
                duong_dan += ".sig"
            self.duong_dan_luu = duong_dan
            self.o_noi_luu.setText(duong_dan)

    # ----------------------------
    #  Hàm thực hiện ký
    # ----------------------------
    def ky_du_lieu(self):
        duong_dan_khoa = self.o_khoa.text().strip()
        thong_diep = self.o_thong_diep.toPlainText().strip()

        # Kiểm tra khóa bí mật
        if not duong_dan_khoa or not os.path.exists(duong_dan_khoa):
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn khóa bí mật hợp lệ!")
            return

        # Nếu người dùng chọn file thì đọc file, ngược lại lấy nội dung nhập
        if self.duong_dan_file:
            try:
                with open(self.duong_dan_file, "rb") as f:
                    du_lieu = f.read()
                thong_diep = du_lieu.decode("utf-8", errors="ignore")
            except Exception as e:
                QMessageBox.critical(self, "Lỗi đọc file", f"Không thể đọc file: {str(e)}")
                return
        elif not thong_diep:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập thông điệp hoặc chọn file để ký!")
            return

        # Gọi hàm ký
        chu_ky = signData.ky_du_lieu(duong_dan_khoa, thong_diep)

        if chu_ky.startswith("Lỗi"):
            QMessageBox.critical(self, "Ký thất bại", chu_ky)
            return

        # Nếu chưa chọn nơi lưu, hỏi lại người dùng
        if not self.duong_dan_luu:
            self.chon_noi_luu()
            if not self.duong_dan_luu:
                QMessageBox.information(self, "Hủy", "Bạn đã hủy lưu chữ ký.")
                return

        # Lưu chữ ký vào file
        try:
            with open(self.duong_dan_luu, "w") as f:
                f.write(chu_ky)
            QMessageBox.information(
                self,
                "Thành công",
                f"✅ Ký thành công!\nChữ ký đã lưu tại:\n{self.duong_dan_luu}",
            )
        except Exception as e:
            QMessageBox.critical(self, "Lỗi lưu file", f"Không thể lưu chữ ký:\n{str(e)}")
