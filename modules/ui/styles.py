# Stylesheet - Cyberpunk Hacker Theme (Softer)
# Color Palette: Almost Black (#0a0e27), Soft Cyan (#00b8d4), Soft Green (#2dd700)
# Warning Red (#ff006e), Accent Yellow (#ffbe0b)

LIGHT_THEME = """
    * {
        font-family: "Courier New", "Consolas", monospace;
        outline: none;
    }
    
    QWidget {
        background-color: #0a0e27;
        color: #00b8d4;
    }
    
    QMainWindow {
        background-color: #0a0e27;
    }
    
    /* ===== SIDEBAR ===== */
    #sidebar {
        background: qlineargradient(x1:0, y1:0, x1:0, y1:1,
                                    stop:0 #0f1729,
                                    stop:1 #0a0e27);
        border-right: 2px solid #00b8d4;
    }
    
    #logo {
        color: #0a0e27;
        font-size: 24px;
        font-weight: 800;
        letter-spacing: 3px;
        padding: 28px 24px;
        background: qlineargradient(x1:0, y1:0, x1:1, y1:0,
                                    stop:0 rgba(0, 184, 212, 0.5),
                                    stop:1 #00b8d4);
        border-bottom: 2px solid #00b8d4;
        text-transform: uppercase;
    }
    
    #menuContainer {
        background-color: transparent;
        padding: 12px 0px;
    }
    
    #menuButton {
        color: #5a9db0;
        background-color: transparent;
        border: none;
        text-align: left;
        padding: 12px 16px;
        margin: 4px 8px;
        font-size: 15px;
        font-weight: 600;
        border-radius: 8px;
    }
    
    #menuButton:hover {
        color: #00b8d4;
        background: rgba(0, 184, 212, 0.08);
        border-left: 3px solid #00b8d4;
        padding-left: 20px;
    }
    
    #menuButton:pressed {
        background: rgba(0, 184, 212, 0.12);
    }
    
    #menuButton.active {
        color: #00b8d4;
        background: qlineargradient(x1:0, y1:0, x1:1, y1:0,
                                    stop:0 rgba(0, 184, 212, 0.12),
                                    stop:1 transparent);
        border-left: 3px solid #00b8d4;
        padding-left: 20px;
        font-weight: 600;
    }
    
    /* ===== CONTENT AREA ===== */
    #contentArea {
        background-color: #0a0e27;
    }
    
    /* ===== BUTTONS ===== */
    QPushButton {
        background: qlineargradient(x1:0, y1:0, x1:0, y1:1,
                                    stop:0 #00b8d4,
                                    stop:1 #008ba3);
        color: #0a0e27;
        border: 2px solid #00b8d4;
        border-radius: 6px;
        padding: 10px 24px;
        font-weight: 700;
        font-size: 15px;
        min-height: 24px;
        letter-spacing: 1px;
    }
    
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x1:0, y1:1,
                                    stop:0 #2dd700,
                                    stop:1 #00b8d4);
        border: 2px solid #2dd700;
        color: #0a0e27;
    }
    
    QPushButton:pressed {
        background: qlineargradient(x1:0, y1:0, x1:0, y1:1,
                                    stop:0 #0091b3,
                                    stop:1 #005970);
        border: 2px solid #0091b3;
    }
    
    QPushButton:disabled {
        background: qlineargradient(x1:0, y1:0, x1:0, y1:1,
                                    stop:0 #2a3f5f,
                                    stop:1 #1a2a3f);
        color: #6b7280;
        border: 2px solid #3a4f6f;
    }
    
    /* ===== INPUT FIELDS ===== */
    QLineEdit, QTextEdit, QPlainTextEdit {
        background-color: #0a0e27;
        border: 2px solid #00b8d4;
        border-radius: 6px;
        padding: 10px 12px;
        color: #00b8d4;
        font-size: 13px;
        font-family: "Courier New", monospace;
        selection-background-color: rgba(0, 184, 212, 0.3);
    }
    
    QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
        border: 2px solid #2dd700;
        background-color: rgba(45, 215, 0, 0.03);
        color: #2dd700;
    }
    
    /* ===== COMBO BOX ===== */
    QComboBox {
        background-color: #0a0e27;
        border: 2px solid #00b8d4;
        border-radius: 6px;
        padding: 6px 10px;
        color: #00b8d4;
        font-size: 18px;
    }
    
    QComboBox:focus {
        border: 2px solid #2dd700;
        color: #2dd700;
    }
    
    QComboBox::drop-down {
        border: none;
        background-color: transparent;
        width: 20px;
    }
    
    QComboBox QAbstractItemView {
        background-color: #0a0e27;
        border: 2px solid #00b8d4;
        color: #00b8d4;
        selection-background-color: rgba(0, 184, 212, 0.2);
    }
    
    /* ===== SCROLL BAR ===== */
    QScrollBar:vertical {
        background-color: transparent;
        width: 10px;
    }
    
    QScrollBar::handle:vertical {
        background: qlineargradient(x1:0, y1:0, x1:1, y1:0,
                                    stop:0 #00b8d4,
                                    stop:1 #008ba3);
        border-radius: 5px;
        min-height: 24px;
        border: 1px solid #00b8d4;
    }
    
    QScrollBar::handle:vertical:hover {
        background: qlineargradient(x1:0, y1:0, x1:1, y1:0,
                                    stop:0 #2dd700,
                                    stop:1 #00b8d4);
        border: 1px solid #2dd700;
    }
    
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        background: none;
        border: none;
    }
    
    /* ===== CHECKBOXES ===== */
    QCheckBox, QRadioButton {
        color: #00b8d4;
        background-color: transparent;
        spacing: 8px;
    }
    
    QCheckBox::indicator, QRadioButton::indicator {
        width: 18px;
        height: 18px;
        border-radius: 4px;
        background-color: #0a0e27;
        border: 2px solid #00b8d4;
    }
    
    QCheckBox::indicator:hover, QRadioButton::indicator:hover {
        border: 2px solid #2dd700;
        background-color: rgba(45, 215, 0, 0.08);
    }
    
    QCheckBox::indicator:checked, QRadioButton::indicator:checked {
        background: qlineargradient(x1:0, y1:0, x1:0, y1:1,
                                    stop:0 #2dd700,
                                    stop:1 #00b8d4);
        border: 2px solid #2dd700;
    }
    
    /* ===== LABELS ===== */
    QLabel {
        color: #00b8d4;
        background-color: transparent;
        font-size: 16px;
        font-weight: 500;
    }
    
    /* ===== FRAMES & CARDS ===== */
    #card, #frame {
        background-color: rgba(10, 14, 39, 0.6);
        border: 2px solid #00b8d4;
        border-radius: 8px;
    }
    
    #cardTitle {
        color: #2dd700;
        font-size: 16px;
        font-weight: 700;
        letter-spacing: 1px;
    }
    
    /* ===== TABS ===== */
    QTabWidget::pane {
        border-top: 2px solid #00b8d4;
        background-color: #0a0e27;
    }
    
    QTabBar::tab {
        background-color: transparent;
        color: #5a9db0;
        padding: 10px 20px;
        border: none;
        border-bottom: 2px solid transparent;
        margin-right: 2px;
    }
    
    QTabBar::tab:hover {
        color: #00b8d4;
        background-color: rgba(0, 184, 212, 0.05);
    }
    
    QTabBar::tab:selected {
        color: #2dd700;
        background: rgba(45, 215, 0, 0.08);
        border-bottom: 2px solid #2dd700;
    }
    
    /* ===== SPINBOX ===== */
    QSpinBox, QDoubleSpinBox {
        background-color: #0a0e27;
        border: 2px solid #00b8d4;
        border-radius: 6px;
        padding: 6px 8px;
        color: #00b8d4;
        font-size: 15px;
    }
    
    QSpinBox:focus, QDoubleSpinBox:focus {
        border: 2px solid #2dd700;
        color: #2dd700;
    }
    
    /* ===== SCROLL AREA ===== */
    QScrollArea {
        background-color: #0a0e27;
        border: none;
    }
    
    /* ===== GROUPBOX ===== */
    QGroupBox {
        color: #00b8d4;
        border: 2px solid #00b8d4;
        border-radius: 6px;
        margin-top: 8px;
        padding-top: 8px;
    }
    
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 3px 0 3px;
        color: #2dd700;
    }
"""

