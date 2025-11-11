# modules/ui/main_app.py
import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton,
    QLabel, QListWidget, QListWidgetItem, QStackedWidget, QCheckBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

# Import giao diện con
from modules.ui.ui_sinh_khoa import WidgetSinhKhoa
from modules.ui.ui_ky_du_lieu import WidgetKyDuLieu
<<<<<<< Updated upstream

=======
from modules.ui.ui_dang_ky_chung_chi import WidgetDangKyChungChi
from modules.ui.ui_xac_thuc import WidgetXacThuc
>>>>>>> Stashed changes

class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ứng dụng PKI")
        self.resize(900, 600)

        #Layout chính (chia làm 2 phần: trái - phải)
        layout_chinh = QHBoxLayout(self)

        #Cột trái: danh sách chức năng
        self.menu = QListWidget()
        self.menu.addItem(QListWidgetItem("Tạo khóa"))
        self.menu.addItem(QListWidgetItem("Ký dữ liệu"))
<<<<<<< Updated upstream
=======
        self.menu.addItem(QListWidgetItem("Yêu cầu chứng chỉ"))
        self.menu.addItem(QListWidgetItem("Xác thực"))

>>>>>>> Stashed changes

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

        #Cột phải: vùng hiển thị nội dung
        self.noi_dung = QStackedWidget()
        self.widget_sinh_khoa = WidgetSinhKhoa()
        self.widget_ky_du_lieu = WidgetKyDuLieu()
<<<<<<< Updated upstream
        self.noi_dung.addWidget(self.widget_sinh_khoa)
        self.noi_dung.addWidget(self.widget_ky_du_lieu)
=======
        self.widget_dang_ky = WidgetDangKyChungChi()
        self.widget_xac_thuc = WidgetXacThuc()
        self.noi_dung.addWidget(self.widget_sinh_khoa)
        self.noi_dung.addWidget(self.widget_ky_du_lieu)
        self.noi_dung.addWidget(self.widget_dang_ky)
        self.noi_dung.addWidget(self.widget_xac_thuc)
>>>>>>> Stashed changes

        #Khi click menu, đổi trang
        self.menu.currentRowChanged.connect(self.noi_dung.setCurrentIndex)

        # Thêm vào layout chính
        layout_chinh.addWidget(self.menu)
        layout_chinh.addWidget(self.noi_dung)

        self.setLayout(layout_chinh)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/icon.jpg"))
    cua_so = MainApp()
    cua_so.show()
    sys.exit(app.exec())
