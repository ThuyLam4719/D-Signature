# modules/ui/main_app.py
import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton,
    QLabel, QStackedWidget, QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QFont

# Import giao diện con
from modules.ui.ui_sinh_khoa import WidgetSinhKhoa
from modules.ui.ui_ky_du_lieu import WidgetKyDuLieu
from modules.ui.ui_dang_ky_chung_chi import WidgetDangKyChungChi
from modules.ui.ui_xac_thuc import WidgetXacThuc
from modules.ui.ui_xac_thuc_cert import WidgetXacThucCert
from modules.ui.styles import LIGHT_THEME


class MenuButton(QPushButton):
    """Custom button with active state styling"""
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setObjectName("menuButton")
        self.is_active = False
    
    def set_active(self, active):
        self.is_active = active
        if active:
            self.setProperty("class", "active")
        else:
            self.setProperty("class", "")
        # Refresh stylesheet
        self.style().unpolish(self)
        self.style().polish(self)


class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("D-Signature | PKI Management")
        self.resize(1200, 700)
        self.setMinimumSize(1000, 600)
        
        self.current_index = 0
        self.menu_items = []

        # Layout chính
        layout_chinh = QHBoxLayout(self)
        layout_chinh.setContentsMargins(0, 0, 0, 0)
        layout_chinh.setSpacing(0)

        # ===== SIDEBAR =====
        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setMaximumWidth(280)
        self.sidebar.setMinimumWidth(280)
        
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)

        # Logo
        logo = QLabel("D-SIGNATURE")
        logo.setObjectName("logo")
        logo.setFont(QFont("Segoe UI", 12, QFont.Bold))
        sidebar_layout.addWidget(logo)

        # Menu container
        menu_container = QFrame()
        menu_container.setObjectName("menuContainer")
        menu_layout = QVBoxLayout(menu_container)
        menu_layout.setContentsMargins(0, 0, 0, 0)
        menu_layout.setSpacing(0)

        # Menu items with icons
        self.menu_data = [
            ("Tạo khóa", "Tạo cặp khóa RSA/ECDSA", WidgetSinhKhoa()),
            ("Tạo chữ ký", "Ký dữ liệu hoặc tệp", WidgetKyDuLieu()),
            ("Tạo CSR", "Tạo CSR & đăng ký", WidgetDangKyChungChi()),
            ("Xác Thực Chữ Ký", "Xác thực chữ ký số", WidgetXacThuc()),
            ("Xác Thực Chứng Chỉ", "Kiểm tra chứng chỉ", WidgetXacThucCert())
        ]

        self.widgets_list = []
        
        for idx, (label, tooltip, widget) in enumerate(self.menu_data):
            btn = MenuButton(label)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setToolTip(tooltip)
            btn.clicked.connect(lambda checked, i=idx: self.switch_page(i))
            btn.setMinimumHeight(48)
            menu_layout.addWidget(btn)
            self.menu_items.append(btn)
            self.widgets_list.append(widget)

        menu_container.setLayout(menu_layout)
        sidebar_layout.addWidget(menu_container)
        sidebar_layout.addStretch()

        # ===== CONTENT AREA =====
        self.noi_dung = QStackedWidget()
        self.noi_dung.setObjectName("contentArea")
        
        for widget in self.widgets_list:
            self.noi_dung.addWidget(widget)

        # Thêm vào layout chính
        layout_chinh.addWidget(self.sidebar)
        layout_chinh.addWidget(self.noi_dung, 1)

        self.setLayout(layout_chinh)
        
        # Apply stylesheet
        self.setStyleSheet(LIGHT_THEME)
        
        # Set icon
        try:
            self.setWindowIcon(QIcon("./images/icon.jpg"))
        except:
            pass
        
        # Set trang mặc định
        self.switch_page(0)

    def switch_page(self, index):
        """Chuyển trang"""
        self.current_index = index
        self.noi_dung.setCurrentIndex(index)
        
        # Cập nhật style cho tất cả menu items
        for i, btn in enumerate(self.menu_items):
            btn.set_active(i == index)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    cua_so = MainApp()
    cua_so.show()
    sys.exit(app.exec())
