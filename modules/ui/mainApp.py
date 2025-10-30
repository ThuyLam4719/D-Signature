# modules/ui/main_app.py
import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton,
    QLabel, QListWidget, QListWidgetItem, QStackedWidget, QCheckBox
)
from PySide6.QtCore import Qt

# Import giao diện con
from modules.ui.ui_sinh_khoa import WidgetSinhKhoa
from modules.ui.ui_ky_du_lieu import WidgetKyDuLieu


class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ứng dụng PKI")
        self.resize(900, 600)

        # === Layout chính (chia làm 2 phần: trái - phải)
        layout_chinh = QHBoxLayout(self)

        # --- Cột trái: danh sách chức năng
        self.menu = QListWidget()
        self.menu.addItem(QListWidgetItem("Tạo khóa"))
        self.menu.addItem(QListWidgetItem("Ký dữ liệu"))

        self.menu.setMaximumWidth(200)
        self.menu.setStyleSheet("""
            QListWidget {
                background-color: #2f3542;
                color: white;
                font-size: 18px;
            }
            QListWidget::item:selected {
                background-color: #57606f;
            }
        """)

        # --- Cột phải: vùng hiển thị nội dung
        self.noi_dung = QStackedWidget()
        self.widget_sinh_khoa = WidgetSinhKhoa()
        self.widget_ky_du_lieu = WidgetKyDuLieu()
        self.noi_dung.addWidget(self.widget_sinh_khoa)
        self.noi_dung.addWidget(self.widget_ky_du_lieu)

        # --- Khi click menu, đổi trang ---
        self.menu.currentRowChanged.connect(self.noi_dung.setCurrentIndex)

        # Thêm vào layout chính
        layout_chinh.addWidget(self.menu)
        layout_chinh.addWidget(self.noi_dung)

        self.setLayout(layout_chinh)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    cua_so = MainApp()
    cua_so.show()
    sys.exit(app.exec())
