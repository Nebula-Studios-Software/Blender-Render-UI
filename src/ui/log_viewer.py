from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPlainTextEdit, QGroupBox,
                         QHBoxLayout, QCheckBox, QComboBox, QLabel)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCharFormat, QBrush, QColor, QFont
from ..utils.settings_manager import SettingsManager
import datetime

class LogViewer(QGroupBox):
    def __init__(self):
        super().__init__("Log Output")
        self.settings_manager = SettingsManager()
        self.log_entries = []
        
        # Carica le impostazioni dei filtri salvate
        ui_state = self.settings_manager.get_ui_state()
        log_filters = ui_state.get('log_filters', {})
        
        # Default impostazioni di filtraggio
        self.show_info = log_filters.get('show_info', True)
        self.show_warning = log_filters.get('show_warning', True)
        self.show_error = log_filters.get('show_error', True)
        
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(10, 15, 10, 10)
        
        # Filter controls container
        filter_container = QWidget()
        filter_layout = QHBoxLayout(filter_container)
        filter_layout.setContentsMargins(0, 0, 0, 5)
        filter_layout.setSpacing(10)
        
        # Filter checkboxes
        self.info_checkbox = QCheckBox("Info")
        self.info_checkbox.setChecked(self.show_info)
        self.info_checkbox.stateChanged.connect(self.filter_changed)
        self.info_checkbox.setStyleSheet("""
            QCheckBox {
                color: #e0e0e0;
            }
        """)
        
        self.warning_checkbox = QCheckBox("Warning")
        self.warning_checkbox.setChecked(self.show_warning)
        self.warning_checkbox.stateChanged.connect(self.filter_changed)
        self.warning_checkbox.setStyleSheet("""
            QCheckBox {
                color: #ffd700;
            }
        """)
        
        self.error_checkbox = QCheckBox("Error")
        self.error_checkbox.setChecked(self.show_error)
        self.error_checkbox.stateChanged.connect(self.filter_changed)
        self.error_checkbox.setStyleSheet("""
            QCheckBox {
                color: #ff6b6b;
            }
        """)
        
        # Detail level combo
        detail_label = QLabel("Detail Level:")
        detail_label.setStyleSheet("color: #e0e0e0;")
        self.detail_combo = QComboBox()
        self.detail_combo.addItems(["All", "Standard", "Minimal"])
        self.detail_combo.setCurrentIndex(1)  # Standard by default
        self.detail_combo.currentIndexChanged.connect(self.filter_changed)
        
        filter_layout.addWidget(self.info_checkbox)
        filter_layout.addWidget(self.warning_checkbox)
        filter_layout.addWidget(self.error_checkbox)
        filter_layout.addSpacing(20)
        filter_layout.addWidget(detail_label)
        filter_layout.addWidget(self.detail_combo)
        filter_layout.addStretch()
        
        layout.addWidget(filter_container)
        
        # Configura l'area di log con stile moderno
        self.log_text = QPlainTextEdit()
        self.log_text.setReadOnly(True)
        
        # Imposta il font monospace per una migliore leggibilità dei log
        font = QFont("Consolas" if hasattr(QFont, "Consolas") else "Courier")
        font.setPointSize(9)
        self.log_text.setFont(font)
        
        # Definisci i formati per i diversi tipi di log
        self.formats = {
            "INFO": QTextCharFormat(),
            "WARNING": QTextCharFormat(),
            "ERROR": QTextCharFormat(),
            "SUCCESS": QTextCharFormat(),
            "FRAME": QTextCharFormat()
        }
        
        # INFO: colore standard
        self.formats["INFO"].setForeground(QBrush(QColor("#e0e0e0")))
        
        # WARNING: giallo
        self.formats["WARNING"].setForeground(QBrush(QColor("#ffd700")))
        
        # ERROR: rosso
        self.formats["ERROR"].setForeground(QBrush(QColor("#ff6b6b")))
        
        # SUCCESS: verde
        self.formats["SUCCESS"].setForeground(QBrush(QColor("#69db7c")))
        
        # FRAME: azzurro (per info sui frame)
        self.formats["FRAME"].setForeground(QBrush(QColor("#eb5e28")))
        
        layout.addWidget(self.log_text)
        self.setLayout(layout)
        
        # Imposta lo stato iniziale dei filtri
        self.filter_changed()
    
    def append_log(self, message, level="INFO"):
        """Aggiunge un messaggio al log con il formato appropriato"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        log_entry = {"timestamp": timestamp, "message": message, "level": level}
        self.log_entries.append(log_entry)
        
        if self.should_show_message(message, level):
            cursor = self.log_text.textCursor()
            cursor.movePosition(cursor.End)
            
            # Seleziona il formato appropriato
            format = self.formats.get(level, self.formats["INFO"])
            
            # Aggiungi timestamp e livello
            cursor.insertText(f"[{timestamp}] [{level}] ", format)
            cursor.insertText(f"{message}\n", format)
            
            # Scorri automaticamente verso il basso
            self.log_text.setTextCursor(cursor)
            self.log_text.ensureCursorVisible()
    
    def should_show_message(self, message, level):
        """Determina se un messaggio deve essere mostrato in base ai filtri attuali"""
        # Controlla il livello
        if ((level == "INFO" and not self.show_info) or 
            (level == "WARNING" and not self.show_warning) or 
            (level == "ERROR" and not self.show_error)):
            return False
        
        # Controlla il livello di dettaglio
        detail_level = self.detail_combo.currentIndex()
        if detail_level == 2:  # Minimal
            return self.is_important_message(message, level)
        elif detail_level == 1:  # Standard
            return not self.is_technical_message(message) or level == "ERROR"
        
        return True  # All
    
    def is_important_message(self, message, level):
        """Determina se un messaggio è importante"""
        if level in ["ERROR", "WARNING"]:
            return True
        
        important_patterns = [
            "Rendering started", "Rendering completed", "Saved:", 
            "Blender quit", "Fra:", "Current Frame:"
        ]
        
        return any(pattern in message for pattern in important_patterns)
    
    def is_technical_message(self, message):
        """Determina se un messaggio è troppo tecnico o di debug"""
        technical_patterns = [
            "malloc", "Memory:", "AL lib:", "pure-virtual:", 
            "OpenGL", "libGL", "0x", "libpng", "libjpeg"
        ]
        
        return any(pattern in message for pattern in technical_patterns)
    
    def filter_changed(self):
        """Gestisce il cambio di stato dei filtri"""
        self.show_info = self.info_checkbox.isChecked()
        self.show_warning = self.warning_checkbox.isChecked()
        self.show_error = self.error_checkbox.isChecked()
        
        # Salva lo stato dei filtri
        ui_state = self.settings_manager.get_ui_state()
        ui_state['log_filters'] = {
            'show_info': self.show_info,
            'show_warning': self.show_warning,
            'show_error': self.show_error,
            'detail_level': self.detail_combo.currentIndex()
        }
        self.settings_manager.set_ui_state(ui_state)
        
        # Riapplica i filtri
        self.apply_filters()
    
    def apply_filters(self):
        """Riapplica i filtri a tutti i messaggi di log"""
        self.log_text.clear()
        for entry in self.log_entries:
            if self.should_show_message(entry["message"], entry["level"]):
                cursor = self.log_text.textCursor()
                cursor.movePosition(cursor.End)
                
                format = self.formats.get(entry["level"], self.formats["INFO"])
                cursor.insertText(f"[{entry['timestamp']}] [{entry['level']}] ", format)
                cursor.insertText(f"{entry['message']}\n", format)
    
    def process_blender_output(self, output_line):
        """Processa una linea di output da Blender e la formatta appropriatamente"""
        if "Saved:" in output_line:
            self.append_log(output_line, "SUCCESS")
        elif "Fra:" in output_line:
            self.append_log(output_line, "FRAME")
        elif "Error:" in output_line or "ERROR" in output_line:
            self.append_log(output_line, "ERROR")
        elif "Warning:" in output_line or "WARNING" in output_line:
            self.append_log(output_line, "WARNING")
        else:
            self.append_log(output_line, "INFO")
    
    def clear(self):
        """Pulisce il log"""
        self.log_entries.clear()
        self.log_text.clear()