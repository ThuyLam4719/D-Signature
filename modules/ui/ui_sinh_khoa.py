import os
from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QMessageBox, QCheckBox,
    QComboBox, QFileDialog
)
from modules.keyGenerate import sinh_khoa_rsa, sinh_khoa_ecdsa


class WidgetSinhKhoa(QWidget):
    def __init__(self):
        super().__init__()

        self.duong_dan_luu = None  # nơi lưu khóa

        # --- Tiêu đề ---
        tieu_de = QLabel("Tạo cặp khóa mới")
        tieu_de.setStyleSheet("font-size: 18px; font-weight: bold;")

        # --- Nhập tên khóa ---
        self.lbl_ten = QLabel("Tên khóa:")
        self.txt_ten = QLineEdit()
        self.txt_ten.setPlaceholderText("Nhập tên khóa...")

        # --- Chọn thuật toán ---
        self.lbl_thuat_toan = QLabel("Chọn thuật toán:")
        self.chk_rsa = QCheckBox("RSA")
        self.chk_ecdsa = QCheckBox("ECDSA")
        self.chk_rsa.setChecked(True)

        # Khi chọn RSA thì bỏ chọn ECDSA và ngược lại
        self.chk_rsa.stateChanged.connect(lambda: self.chon_thuat_toan("RSA"))
        self.chk_ecdsa.stateChanged.connect(lambda: self.chon_thuat_toan("ECDSA"))

        layout_thuat_toan = QHBoxLayout()
        layout_thuat_toan.addWidget(self.chk_rsa)
        layout_thuat_toan.addWidget(self.chk_ecdsa)

        # --- Độ dài hoặc loại đường cong ---
        self.lbl_thuoc_tinh = QLabel("Chọn độ dài khóa:")
        self.combo_thuoc_tinh = QComboBox()
        self.combo_thuoc_tinh.addItems(["2048", "3072", "4096"])

        # --- Nút chọn nơi lưu ---
        self.lbl_luu = QLabel("Chọn nơi lưu khóa:")
        self.o_noi_luu = QLineEdit()
        self.o_noi_luu.setPlaceholderText("Chưa chọn nơi lưu...")
        self.nut_chon_luu = QPushButton("Chọn")
        self.nut_chon_luu.clicked.connect(self.chon_noi_luu)

        layout_luu = QHBoxLayout()
        layout_luu.addWidget(self.o_noi_luu)
        layout_luu.addWidget(self.nut_chon_luu)

        # --- Nút sinh khóa ---
        self.btn_sinh = QPushButton("Tạo khóa")
        self.btn_sinh.clicked.connect(self.sinh_khoa)

        # --- Layout tổng ---
        layout = QVBoxLayout()
        layout.addWidget(tieu_de)
        layout.addWidget(self.lbl_ten)
        layout.addWidget(self.txt_ten)
        layout.addWidget(self.lbl_thuat_toan)
        layout.addLayout(layout_thuat_toan)
        layout.addWidget(self.lbl_thuoc_tinh)
        layout.addWidget(self.combo_thuoc_tinh)
        layout.addWidget(self.lbl_luu)
        layout.addLayout(layout_luu)
        layout.addWidget(self.btn_sinh)
        layout.addStretch()

        self.setLayout(layout)

    # ----------------------------
    #  Các hàm xử lý
    # ----------------------------
    def chon_thuat_toan(self, loai):
        """Đảm bảo chỉ 1 thuật toán được chọn"""
        if loai == "RSA":
            if self.chk_rsa.isChecked():
                self.chk_ecdsa.setChecked(False)
                self.lbl_thuoc_tinh.setText("Chọn độ dài khóa:")
                self.combo_thuoc_tinh.clear()
                self.combo_thuoc_tinh.addItems(["2048", "3072", "4096"])
        else:
            if self.chk_ecdsa.isChecked():
                self.chk_rsa.setChecked(False)
                self.lbl_thuoc_tinh.setText("Chọn loại đường cong:")
                self.combo_thuoc_tinh.clear()
                self.combo_thuoc_tinh.addItems(["P-256", "P-384", "P-521"])

    def chon_noi_luu(self):
        """Chọn nơi lưu khóa và đặt tên"""
        ten_goi_y = self.txt_ten.text().strip() or "mykey"
        duong_dan, _ = QFileDialog.getSaveFileName(
            self,
            "Chọn nơi lưu và đặt tên khóa (chỉ gợi ý, sẽ tạo thêm _private/_public)",
            f"data/keys/{ten_goi_y}",
            "Tệp PEM (*.pem)"
        )
        if duong_dan:
            self.duong_dan_luu = os.path.dirname(duong_dan)
            self.o_noi_luu.setText(self.duong_dan_luu)

    def sinh_khoa(self):
        """Thực hiện sinh khóa"""
        ten = self.txt_ten.text().strip()
        if not ten:
            QMessageBox.warning(self, "Thiếu thông tin", "Vui lòng nhập tên khóa.")
            return

        # Nếu chưa chọn nơi lưu thì hỏi lại
        if not self.duong_dan_luu:
            self.chon_noi_luu()
            if not self.duong_dan_luu:
                QMessageBox.information(self, "Hủy", "Bạn đã hủy lưu khóa.")
                return

        # Sinh khóa theo loại
        try:
            if self.chk_rsa.isChecked():
                bit = int(self.combo_thuoc_tinh.currentText())
                sinh_khoa_rsa(ten, bit, self.duong_dan_luu)
                loai = f"RSA {bit} bit"
            else:
                curve = self.combo_thuoc_tinh.currentText()
                sinh_khoa_ecdsa(ten, curve, self.duong_dan_luu)
                loai = f"ECDSA {curve}"

            QMessageBox.information(
                self,
                "Thành công",
                f"✅ Đã sinh khóa {loai}\nTên: {ten}\nLưu tại: {self.duong_dan_luu}"
            )
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể sinh khóa: {str(e)}")
