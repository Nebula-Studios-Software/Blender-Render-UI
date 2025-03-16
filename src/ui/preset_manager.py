from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                         QPushButton, QListWidget, QMessageBox)
from PyQt5.QtCore import Qt

class PresetManagerDialog(QDialog):
    def __init__(self, settings_manager, parent=None):
        super().__init__(parent)
        self.settings_manager = settings_manager
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Manage Presets")
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout()
        
        # Lista dei preset
        self.preset_list = QListWidget()
        self.preset_list.currentItemChanged.connect(self.on_selection_changed)
        
        # Pulsanti
        button_layout = QHBoxLayout()
        
        self.rename_btn = QPushButton("Rename")
        self.rename_btn.clicked.connect(self.rename_preset)
        self.rename_btn.setEnabled(False)
        
        self.delete_btn = QPushButton("Delete")
        self.delete_btn.clicked.connect(self.delete_preset)
        self.delete_btn.setEnabled(False)
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        
        button_layout.addWidget(self.rename_btn)
        button_layout.addWidget(self.delete_btn)
        button_layout.addStretch()
        button_layout.addWidget(close_btn)
        
        layout.addWidget(QLabel("Available Presets:"))
        layout.addWidget(self.preset_list)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # Carica i preset
        self.load_presets()
    
    def load_presets(self):
        """Carica la lista dei preset"""
        self.preset_list.clear()
        for preset_name in self.settings_manager.get_preset_names():
            self.preset_list.addItem(preset_name)
    
    def on_selection_changed(self, current, previous):
        """Gestisce il cambio di selezione nella lista"""
        is_selected = current is not None
        is_default = current.text() == 'default' if current else False
        
        self.rename_btn.setEnabled(is_selected and not is_default)
        self.delete_btn.setEnabled(is_selected and not is_default)
    
    def rename_preset(self):
        """Rinomina il preset selezionato"""
        current_item = self.preset_list.currentItem()
        if not current_item:
            return
        
        old_name = current_item.text()
        new_name, ok = QInputDialog.getText(
            self,
            "Rename Preset",
            "Enter new name:",
            text=old_name
        )
        
        if ok and new_name and new_name != old_name:
            success = self.settings_manager.rename_preset(old_name, new_name)
            if success:
                self.load_presets()
                # Seleziona il preset rinominato
                items = self.preset_list.findItems(new_name, Qt.MatchExactly)
                if items:
                    self.preset_list.setCurrentItem(items[0])
            else:
                QMessageBox.warning(
                    self,
                    "Error",
                    "Could not rename the preset. The default preset cannot be renamed."
                )
    
    def delete_preset(self):
        """Elimina il preset selezionato"""
        current_item = self.preset_list.currentItem()
        if not current_item:
            return
        
        preset_name = current_item.text()
        confirm = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete the preset '{preset_name}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if confirm == QMessageBox.Yes:
            success = self.settings_manager.delete_preset(preset_name)
            if success:
                self.load_presets()
            else:
                QMessageBox.warning(
                    self,
                    "Error",
                    "Could not delete the preset. The default preset cannot be deleted."
                )