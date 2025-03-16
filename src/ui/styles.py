"""
Definizione degli stili dell'interfaccia utente
Utilizza una palette di colori moderna e minimal con tema scuro
"""

STYLE = """
/* Stile generale dell'applicazione */
QWidget {
    background-color: #1e1e1e;
    color: #e0e0e0;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 10pt;
}

/* Gruppi */
QGroupBox {
    border: 2px solid #3d3d3d;
    border-radius: 8px;
    margin-top: 1em;
    padding-top: 1em;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px;
    color: #00b4d8;
}

/* Tab Widget */
QTabWidget::pane {
    border: none;
    background-color: #252525;
}

QTabBar::tab {
    background-color: #3d3d3d;
    color: #b0b0b0;
    min-width: 8ex;
    padding: 8px 12px;
}

QTabBar::tab:selected {
    background-color: #3d3d3d;
    color: #00b4d8;
}

QTabBar::tab:hover {
    background-color: #353535;
}

/* Pulsanti */
QPushButton {
    background-color: #2d2d2d;
    border: 2px solid #00b4d8;
    border-radius: 6px;
    padding: 5px 15px;
    color: #00b4d8;
}

QPushButton:hover {
    background-color: #00b4d8;
    color: #ffffff;
}

QPushButton:pressed {
    background-color: #0077b6;
}

QPushButton:disabled {
    background-color: #2d2d2d;
    border-color: #666666;
    color: #666666;
}

/* Input di testo */
QLineEdit {
    background-color: #2d2d2d;
    border: 2px solid #3d3d3d;
    border-radius: 6px;
    padding: 5px;
    color: #e0e0e0;
}

QLineEdit:focus {
    border-color: #00b4d8;
}

QLineEdit:disabled {
    background-color: #252525;
    color: #666666;
}

/* ComboBox */
QComboBox {
    background-color: #2d2d2d;
    border: 2px solid #3d3d3d;
    border-radius: 6px;
    padding: 5px;
    color: #e0e0e0;
}

QComboBox:hover {
    border-color: #00b4d8;
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
    background-color: #2d2d2d;
    border: 2px solid #3d3d3d;
    border-radius: 6px;
    padding: 5px;
    color: #e0e0e0;
}

QSpinBox:hover {
    border-color: #00b4d8;
}

/* CheckBox */
QCheckBox {
    spacing: 8px;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border: 2px solid #3d3d3d;
    border-radius: 4px;
    background-color: #2d2d2d;
}

QCheckBox::indicator:checked {
    background-color: #00b4d8;
    border-color: #00b4d8;
}

QCheckBox::indicator:hover {
    border-color: #00b4d8;
}

/* ScrollBar */
QScrollBar:vertical {
    border: none;
    background-color: #2d2d2d;
    width: 10px;
    border-radius: 5px;
}

QScrollBar::handle:vertical {
    background-color: #3d3d3d;
    border-radius: 5px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #00b4d8;
}

QScrollBar:horizontal {
    border: none;
    background-color: #2d2d2d;
    height: 10px;
    border-radius: 5px;
}

QScrollBar::handle:horizontal {
    background-color: #3d3d3d;
    border-radius: 5px;
    min-width: 20px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #00b4d8;
}

/* Progress Bar */
QProgressBar {
    border: 2px solid #3d3d3d;
    border-radius: 6px;
    background-color: #2d2d2d;
    text-align: center;
    color: #e0e0e0;
}

QProgressBar::chunk {
    background-color: #00b4d8;
    border-radius: 4px;
}

/* Menu e StatusBar */
QMenuBar {
    background-color: #252525;
}

QMenuBar::item {
    padding: 5px 10px;
    background-color: transparent;
}

QMenuBar::item:selected {
    background-color: #3d3d3d;
}

QStatusBar {
    background-color: #252525;
}

/* QScrollArea */
QScrollArea {
    border: none;
    background-color: transparent;
}

/* Lista e Table */
QListView, QTableView {
    background-color: #2d2d2d;
    border: 2px solid #3d3d3d;
    border-radius: 8px;
}

QListView::item:selected, QTableView::item:selected {
    background-color: #00b4d8;
    color: #ffffff;
}

QListView::item:hover, QTableView::item:hover {
    background-color: #353535;
}

/* Header */
QHeaderView::section {
    background-color: #2d2d2d;
    color: #00b4d8;
    padding: 5px;
    border: none;
}
"""