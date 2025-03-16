"""
Definition of user interface styles
Uses a modern and minimal color palette with dark theme
"""

STYLE = """
/* General application style */
QWidget {
    background-color: #131211;
    color: #fffcf2;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 10pt;
}

/* Groups */
QGroupBox {
    border: 2px solid #2a2826;
    border-radius: 8px;
    margin-top: 1em;
    padding-top: 1em;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px;
    color: #eb5e28;
}

/* Tab Widget */
QTabWidget::pane {
    border: none;
    background-color: #1a1918;
}

QTabBar::tab {
    background-color: #1a1918;
    color: #fffcf2;
    min-width: 8ex;
    padding: 8px 12px;
}

QTabBar::tab:selected {
    background-color: #1a1918;
    color: #eb5e28;
    border-right: 2px solid #eb5e28;
}

QTabBar::tab:hover {
    background-color: #252321;
}

/* Buttons */
QPushButton {
    background-color: #1a1918;
    border: 2px solid #eb5e28;
    border-radius: 6px;
    padding: 5px 15px;
    color: #eb5e28;
}

QPushButton:hover {
    background-color: #eb5e28;
    color: #fffcf2;
}

QPushButton:pressed {
    background-color: #d44d1c;
}

QPushButton:disabled {
    background-color: #1a1918;
    border-color: #666666;
    color: #666666;
}

/* Text Input */
QLineEdit {
    background-color: #1a1918;
    border: 2px solid #2a2826;
    border-radius: 6px;
    padding: 5px;
    color: #fffcf2;
}

QLineEdit:focus {
    border-color: #eb5e28;
}

QLineEdit:disabled {
    background-color: #1a1918;
    color: #666666;
}

/* ComboBox */
QComboBox {
    background-color: #1a1918;
    border: 2px solid #2a2826;
    border-radius: 6px;
    padding: 5px;
    color: #fffcf2;
}

QComboBox:hover {
    border-color: #eb5e28;
}

QComboBox::drop-down {
    border: none;
}

QComboBox::down-arrow {
    image: url(down_arrow.png);
    width: 12px;
    height: 12px;
}

/* SpinBox */
QSpinBox {
    background-color: #1a1918;
    border: 2px solid #2a2826;
    border-radius: 6px;
    padding: 5px;
    color: #fffcf2;
}

QSpinBox:hover {
    border-color: #eb5e28;
}

/* CheckBox */
QCheckBox {
    spacing: 8px;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border: 2px solid #2a2826;
    border-radius: 4px;
    background-color: #1a1918;
}

QCheckBox::indicator:checked {
    background-color: #eb5e28;
    border-color: #eb5e28;
}

QCheckBox::indicator:hover {
    border-color: #eb5e28;
}

/* ScrollBar */
QScrollBar:vertical {
    border: none;
    background-color: #1a1918;
    width: 10px;
    border-radius: 5px;
}

QScrollBar::handle:vertical {
    background-color: #2a2826;
    border-radius: 5px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #eb5e28;
}

QScrollBar:horizontal {
    border: none;
    background-color: #1a1918;
    height: 10px;
    border-radius: 5px;
}

QScrollBar::handle:horizontal {
    background-color: #2a2826;
    border-radius: 5px;
    min-width: 20px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #eb5e28;
}

/* Progress Bar */
QProgressBar {
    border: 2px solid #2a2826;
    border-radius: 6px;
    background-color: #1a1918;
    text-align: center;
    color: #fffcf2;
}

QProgressBar::chunk {
    background-color: #eb5e28;
    border-radius: 4px;
}

/* Menu and StatusBar */
QMenuBar {
    background-color: #1a1918;
}

QMenuBar::item {
    padding: 5px 10px;
    background-color: transparent;
}

QMenuBar::item:selected {
    background-color: #2a2826;
}

QStatusBar {
    background-color: #131211;
    color: #fffcf2;
    padding: 2px 8px;
}

QStatusBar QLabel {
    padding: 3px;
    color: #fffcf2;
}

QStatusBar::item {
    border: none;
}

/* Status Indicators */
#statusIndicator {
    border: 2px solid #2a2826;
    border-radius: 6px;
    padding: 2px 8px;
}

#statusIndicator[status="idle"] {
    background-color: #1a1918;
    color: #fffcf2;
}

#statusIndicator[status="rendering"] {
    background-color: #eb5e28;
    color: #fffcf2;
}

#statusIndicator[status="error"] {
    background-color: #ff0040;
    color: #fffcf2;
}

#statusIndicator[status="completed"] {
    background-color: #00ff73;
    color: #131211;
}

/* List and Table */
QListView, QTableView {
    background-color: #1a1918;
    border: 2px solid #2a2826;
    border-radius: 8px;
}

QListView::item:selected, QTableView::item:selected {
    background-color: #eb5e28;
    color: #fffcf2;
}

QListView::item:hover, QTableView::item:hover {
    background-color: #252321;
}

/* Header */
QHeaderView::section {
    background-color: #1a1918;
    color: #eb5e28;
    padding: 5px;
    border: none;
}

/* Main Window */
QMainWindow {
    background-color: #1a1918;
}

/* Status Indicator styles */
#statusIndicator {
    padding: 4px 8px;
    border-radius: 4px;
    font-weight: bold;
}

#statusIndicator[status="idle"] {
    color: #808080;
}

#statusIndicator[status="rendering"] {
    color: #00ff73;
}

#statusIndicator[status="completed"] {
    color: #eb5e28;
}

#statusIndicator[status="error"] {
    color: #ff0040;
}
"""