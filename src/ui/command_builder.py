from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                         QLineEdit, QPushButton, QFileDialog, QCheckBox, 
                         QComboBox, QSpinBox, QTabWidget, QScrollArea, 
                         QGroupBox, QFormLayout, QApplication, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont
import os
import sys
from ..core.param_definitions import ParamDefinitions
from ..utils.settings_manager import SettingsManager

class CommandBuilder(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings_manager = SettingsManager()
        self.parameter_widgets = {}
        self.parameter_values = {}  # Initialize the parameter_values dictionary
        self.main_window = parent  # Move this line before init_ui()
        self.init_ui()
        self.load_saved_settings()

    def load_saved_settings(self):
        """Carica le impostazioni salvate"""
        # Carica il percorso di Blender
        blender_path = self.settings_manager.get_blender_path()
        if blender_path and hasattr(self, 'blender_path_edit'):
            self.blender_path_edit.setText(blender_path)
        
        # Carica i parametri
        parameters = self.settings_manager.get_parameters()
        for param_name, value in parameters.items():
            if param_name in self.parameter_widgets:
                widget = self.parameter_widgets[param_name]
                if isinstance(widget, QLineEdit):
                    widget.setText(str(value))
                elif isinstance(widget, QCheckBox):
                    widget.setChecked(bool(value))
                elif isinstance(widget, QSpinBox):
                    widget.setValue(int(value))
                elif isinstance(widget, QComboBox):
                    index = widget.findText(str(value))
                    if index >= 0:
                        widget.setCurrentIndex(index)

    def init_ui(self):
        main_layout = QHBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Tab widget con stile moderno e orientamento verticale
        tabs = QTabWidget()
        tabs.setDocumentMode(True)
        tabs.setTabPosition(QTabWidget.West)  # Tab verticali a sinistra
        
        # Stile moderno per i tab
        tabs.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background: #1e1e1e;
            }
            QTabBar::tab {
                padding: 15px;
                color: #e0e0e0;
                background: #252525;
                border: none;
                border-right: 2px solid #1e1e1e;
                min-width: 120px;
                max-width: 120px;
            }
            QTabBar::tab:selected {
                background: #1e1e1e;
                color: #00b4d8;
                border-right: 2px solid #00b4d8;
            }
            QTabBar::tab:hover:!selected {
                background: #2d2d2d;
            }
        """)
        
        # Ottiene le categorie di parametri
        param_categories = ParamDefinitions.get_categories()
        
        # Tab per le impostazioni generali (Blender Path)
        general_tab = QWidget()
        general_layout = QVBoxLayout(general_tab)
        general_layout.setContentsMargins(20, 20, 20, 20)
        general_layout.setSpacing(15)
        
        # Blender Path Section con stile moderno
        path_frame = QFrame()
        path_frame.setObjectName("pathFrame")
        path_frame.setStyleSheet("""
            #pathFrame {
                background-color: #252525;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        path_layout = QVBoxLayout(path_frame)
        path_layout.setContentsMargins(15, 15, 15, 15)
        path_layout.setSpacing(10)
        
        path_label = QLabel("Blender Path:")
        path_label.setStyleSheet("color: #00b4d8; font-weight: bold;")
        self.blender_path_edit = QLineEdit()
        
        browse_btn = QPushButton("Browse")
        browse_btn.setFixedWidth(100)
        browse_btn.clicked.connect(self.browse_blender_path)
        
        path_layout.addWidget(path_label)
        path_layout.addWidget(self.blender_path_edit)
        path_layout.addWidget(browse_btn)
        
        general_layout.addWidget(path_frame)
        general_layout.addStretch()
        
        tabs.addTab(general_tab, "General")
        
        # Crea un tab per ogni categoria
        for category_name, parameters in param_categories.items():
            tab = QWidget()
            tab_layout = QVBoxLayout()
            tab_layout.setContentsMargins(20, 20, 20, 20)
            tab_layout.setSpacing(15)
            
            # ScrollArea con stile moderno
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            scroll.setFrameShape(QFrame.NoFrame)
            scroll.setStyleSheet("""
                QScrollArea {
                    border: none;
                    background: transparent;
                }
                QScrollBar:vertical {
                    border: none;
                    background: #252525;
                    width: 10px;
                    margin: 0;
                }
                QScrollBar::handle:vertical {
                    background: #404040;
                    min-height: 20px;
                    border-radius: 5px;
                }
                QScrollBar::handle:vertical:hover {
                    background: #4a4a4a;
                }
                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                    height: 0;
                    background: none;
                }
            """)
            
            scroll_content = QWidget()
            scroll_layout = QFormLayout(scroll_content)
            scroll_layout.setSpacing(15)
            scroll_layout.setContentsMargins(0, 0, 15, 0)
            
            # Aggiunge i parametri per questa categoria
            for param in parameters:
                self.add_parameter_widget(param, scroll_layout)
            
            scroll_content.setLayout(scroll_layout)
            scroll.setWidget(scroll_content)
            tab_layout.addWidget(scroll)
            tab.setLayout(tab_layout)
            tabs.addTab(tab, category_name)
        
        main_layout.addWidget(tabs, stretch=1)
        
        # Container per pulsanti
        right_container = QFrame()
        right_container.setObjectName("rightContainer")
        right_container.setStyleSheet("""
            #rightContainer {
                background-color: #252525;
                border-left: 1px solid #333333;
            }
        """)
        right_layout = QVBoxLayout(right_container)
        right_layout.setContentsMargins(20, 20, 20, 20)
        right_layout.setSpacing(15)
        
        # Buttons container
        buttons_container = QFrame()
        buttons_layout = QHBoxLayout(buttons_container)
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setSpacing(10)
        
        self.copy_button = QPushButton("Copy Command")
        self.copy_button.setFixedWidth(150)
        self.copy_button.clicked.connect(self.copy_command)
        
        self.reset_button = QPushButton("Reset")
        self.reset_button.setFixedWidth(100)
        self.reset_button.clicked.connect(self.reset_parameters)
        
        buttons_layout.addWidget(self.copy_button)
        buttons_layout.addWidget(self.reset_button)
        buttons_layout.addStretch()
        
        right_layout.addWidget(buttons_container)
        right_layout.addStretch()
        
        main_layout.addWidget(right_container, stretch=0)
        right_container.setFixedWidth(400)  # Larghezza fissa per il pannello destro
        
        self.setLayout(main_layout)
        
        # Aggiorna il comando iniziale
        self.update_command()

    def add_parameter_widget(self, param, layout):
        """Aggiunge un widget appropriato al tipo di parametro"""
        param_name = param["name"]
        param_type = param["type"]
        param_description = param["description"]
        
        widget = None
        
        if param_type == "bool":
            widget = QCheckBox(param_name)
            widget.setToolTip(param_description)
            widget.stateChanged.connect(lambda state, p=param["param"]: 
                                       self.update_parameter(p, state == Qt.Checked))
        
        elif param_type == "file":
            container = QWidget()
            file_layout = QHBoxLayout(container)
            file_layout.setContentsMargins(0, 0, 0, 0)
            
            line_edit = QLineEdit()
            line_edit.setPlaceholderText(param_description)
            
            browse_button = QPushButton("Sfoglia...")
            browse_button.clicked.connect(lambda _, le=line_edit, p=param["param"]: 
                                        self.browse_file(le, p))
            
            file_layout.addWidget(line_edit)
            file_layout.addWidget(browse_button)
            widget = container
            
            line_edit.textChanged.connect(lambda text, p=param["param"]: 
                                       self.update_parameter(p, text))
        
        elif param_type == "path":
            container = QWidget()
            path_layout = QHBoxLayout(container)
            path_layout.setContentsMargins(0, 0, 0, 0)
            
            line_edit = QLineEdit()
            line_edit.setPlaceholderText(param_description)
            
            browse_button = QPushButton("Sfoglia...")
            browse_button.clicked.connect(lambda _, le=line_edit, p=param["param"]: 
                                        self.browse_directory(le, p))
            
            path_layout.addWidget(line_edit)
            path_layout.addWidget(browse_button)
            widget = container
            
            line_edit.textChanged.connect(lambda text, p=param["param"]: 
                                       self.update_parameter(p, text))
        
        elif param_type == "string":
            widget = QLineEdit()
            widget.setPlaceholderText(param_description)
            widget.textChanged.connect(lambda text, p=param["param"]: 
                                       self.update_parameter(p, text))
        
        elif param_type == "int":
            widget = QSpinBox()
            widget.setRange(-999999, 999999)
            widget.setToolTip(param_description)
            widget.valueChanged.connect(lambda value, p=param["param"]: 
                                       self.update_parameter(p, value))
        
        elif param_type == "enum" and "options" in param:
            widget = QComboBox()
            widget.setToolTip(param_description)
            for option in param["options"]:
                widget.addItem(option)
            widget.currentTextChanged.connect(lambda text, p=param["param"]: 
                                           self.update_parameter(p, text))
        
        if widget:
            self.parameter_widgets[param["param"]] = widget
            layout.addRow(param_name + ":", widget)

    def browse_file(self, line_edit, param_name):
        """Apre il dialogo per selezionare un file"""
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleziona File", "", "Tutti i file (*)")
        if file_path:
            line_edit.setText(file_path)
            self.update_parameter(param_name, file_path)

    def browse_directory(self, line_edit, param_name):
        """Apre il dialogo per selezionare una directory"""
        directory = QFileDialog.getExistingDirectory(self, "Seleziona Directory")
        if directory:
            line_edit.setText(directory)
            self.update_parameter(param_name, directory)
    
    def browse_blender_path(self):
        """Apre il dialogo per selezionare il percorso di Blender"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Seleziona Blender Executable", "", 
            "Executable (*.exe);;All Files (*)" if sys.platform == "win32" else "All Files (*)")
        if file_path:
            self.blender_path_edit.setText(file_path)
            self.update_command()
            # Salva il nuovo percorso di Blender
            self.settings_manager.set_blender_path(file_path)

    def update_parameter(self, param_name, value):
        """Aggiorna il valore di un parametro e rigenera il comando"""
        if not value and param_name in self.parameter_values:
            del self.parameter_values[param_name]
        elif value:
            self.parameter_values[param_name] = value
        self.update_command()
        # Salva le impostazioni ogni volta che vengono modificate
        self.save_settings()

    def update_command(self):
        """Aggiorna la visualizzazione del comando completo"""
        blender_path = self.blender_path_edit.text()
        command_parts = [f'"{blender_path}"'] if blender_path else ["blender"]
        
        # Gestisci il file .blend separatamente
        blend_file = None
        # Controlla se -b è attivo
        background_mode = False
        
        ordered_params = []
        
        for param, value in self.parameter_values.items():
            if param == ParamDefinitions.FILE:
                blend_file = value
                continue
            elif param == ParamDefinitions.BACKGROUND and value:
                background_mode = True
            
            # Ottieni l'ordine del parametro
            order = ParamDefinitions.get_param_order(param)
            ordered_params.append((order, param, value))
        
        # Ordina i parametri in base alla priorità
        ordered_params.sort(key=lambda x: x[0])
        
        # Se abbiamo un file .blend, inseriscilo nella posizione corretta
        if blend_file:
            if background_mode:
                # Cerca la posizione di -b nei parametri ordinati
                b_index = -1
                for i, (_, param, _) in enumerate(ordered_params):
                    if param == ParamDefinitions.BACKGROUND:
                        b_index = i
                        break
                
                # Inserisci il file .blend dopo -b
                if b_index >= 0:
                    first_params = ordered_params[:b_index + 1]
                    remaining_params = ordered_params[b_index + 1:]
                    
                    # Aggiungi i parametri fino a -b incluso
                    for _, param, value in first_params:
                        if isinstance(value, bool) and value:
                            command_parts.append(param)
                        elif not isinstance(value, bool) and value:
                            command_parts.extend([param, f'"{value}"'])
                    
                    # Aggiungi il file .blend
                    command_parts.extend([f'"{blend_file}"'])
                    
                    # Aggiungi i parametri rimanenti
                    for _, param, value in remaining_params:
                        if isinstance(value, bool) and value:
                            command_parts.append(param)
                        elif not isinstance(value, bool) and value:
                            command_parts.extend([param, f'"{value}"'])
            else:
                # Se non c'è -b, aggiungi il file subito dopo l'exe
                command_parts.extend([f'"{blend_file}"'])
                
                # Poi aggiungi tutti gli altri parametri
                for _, param, value in ordered_params:
                    if isinstance(value, bool) and value:
                        command_parts.append(param)
                    elif not isinstance(value, bool) and value:
                        command_parts.extend([param, f'"{value}"'])
        else:
            # Se non c'è file .blend, aggiungi tutti i parametri normalmente
            for _, param, value in ordered_params:
                if isinstance(value, bool) and value:
                    command_parts.append(param)
                elif not isinstance(value, bool) and value:
                    command_parts.extend([param, f'"{value}"'])
        
        command = " ".join(command_parts)
        if hasattr(self, 'main_window') and self.main_window is not None:
            self.main_window.update_command_preview(command)

    def build_command(self):
        """Build and return the command without showing preview"""
        # Return the command for the main window to display
        return self.construct_command()

    def construct_command(self):
        """Internal method to construct the command"""
        blender_path = self.blender_path_edit.text()
        if not blender_path:
            return None

        command = [blender_path, '-b']
        # Add other parameters based on widget values
        for param_name, widget in self.parameter_widgets.items():
            value = None
            if isinstance(widget, QLineEdit):
                value = widget.text()
            elif isinstance(widget, QCheckBox):
                value = widget.isChecked()
            elif isinstance(widget, QSpinBox):
                value = widget.value()
            elif isinstance(widget, QComboBox):
                value = widget.currentText()

            if value:
                param_def = ParamDefinitions.get_param(param_name)
                if param_def:
                    if isinstance(value, bool) and value:
                        command.append(param_def)
                    else:
                        command.append(param_def)
                        command.append(str(value))

        return command

    def copy_command(self):
        """Copia il comando negli appunti"""
        command = self.construct_command()
        clipboard = QApplication.clipboard()
        clipboard.setText(" ".join(command))

    def reset_parameters(self):
        """Resetta tutti i parametri"""
        self.parameter_values.clear()
        
        for param, widget in self.parameter_widgets.items():
            if isinstance(widget, QCheckBox):
                widget.setChecked(False)
            elif isinstance(widget, QComboBox):
                widget.setCurrentIndex(0)
            elif isinstance(widget, QSpinBox):
                widget.setValue(0)
            elif isinstance(widget, QWidget):
                # Cerca QLineEdit all'interno di container compositi
                line_edit = widget.findChild(QLineEdit)
                if line_edit:
                    line_edit.clear()
            elif isinstance(widget, QLineEdit):
                widget.clear()
        
        self.update_command()
        # Salva lo stato resettato
        self.save_settings()

    def load_settings(self, settings):
        """Carica le impostazioni salvate nei widget"""
        if 'blender_path' in settings:
            self.blender_path_edit.setText(settings['blender_path'])
        
        for param, value in settings.items():
            if param in self.parameter_widgets:
                widget = self.parameter_widgets[param]
                if isinstance(widget, QCheckBox):
                    widget.setChecked(value)
                elif isinstance(widget, QLineEdit):
                    widget.setText(value)
                elif isinstance(widget, QSpinBox):
                    widget.setValue(value)
                elif isinstance(widget, QComboBox):
                    index = widget.findText(value)
                    if index >= 0:
                        widget.setCurrentIndex(index)
                        
    def save_settings(self):
        """Salva le impostazioni correnti"""
        # Salva il percorso di Blender
        self.settings_manager.set_blender_path(self.blender_path_edit.text())
        
        # Prepara il dizionario dei parametri
        parameters = {}
        for param, widget in self.parameter_widgets.items():
            if isinstance(widget, QCheckBox):
                parameters[param] = widget.isChecked()
            elif isinstance(widget, QLineEdit):
                parameters[param] = widget.text()
            elif isinstance(widget, QSpinBox):
                parameters[param] = widget.value()
            elif isinstance(widget, QComboBox):
                parameters[param] = widget.currentText()
        
        # Salva i parametri
        self.settings_manager.set_parameters(parameters)