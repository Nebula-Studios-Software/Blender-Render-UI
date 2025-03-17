from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                         QLineEdit, QPushButton, QFileDialog, QCheckBox, 
                         QComboBox, QSpinBox, QTabWidget, QScrollArea, 
                         QGroupBox, QFormLayout, QApplication, QFrame, QInputDialog, QDialog)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
import os
import sys
from ..core.param_definitions import ParamDefinitions
from ..utils.settings_manager import SettingsManager
from .preset_manager import PresetManagerDialog

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
        
        # Tab widget con stile moderno
        tabs = QTabWidget()
        tabs.setDocumentMode(True)
        tabs.setTabPosition(QTabWidget.West)  # Tab verticali a sinistra
        
        # Stile moderno per i tab con testo ruotato
        tabs.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background: #1e1e1e;
            }
            QTabBar::tab {
                padding: 8px;
                color: #e0e0e0;
                background: #252525;
                border: none;
                border-right: 2px solid #1e1e1e;
                min-width: 35px;
                max-width: 35px;
                min-height: 120px;
            }
            QTabBar::tab:selected {
                background: #1e1e1e;
                color: #eb5e28;
                border-right: 2px solid #eb5e28;
            }
            QTabBar::tab:hover:!selected {
                background: #2d2d2d;
            }
        """)
        
        # Ottiene le categorie di parametri
        param_categories = ParamDefinitions.get_categories()
        
        # Tab per le impostazioni generali (Blender Path e Preset)
        general_tab = QWidget()
        general_layout = QVBoxLayout(general_tab)
        general_layout.setContentsMargins(20, 20, 20, 20)
        general_layout.setSpacing(15)
        
        # Preset Section
        preset_frame = QFrame()
        preset_frame.setObjectName("presetFrame")
        preset_frame.setStyleSheet("""
            #presetFrame {
                background-color: #252525;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        preset_layout = QVBoxLayout(preset_frame)
        preset_layout.setContentsMargins(15, 15, 15, 15)
        preset_layout.setSpacing(10)
        
        preset_label = QLabel("Presets:")
        preset_label.setStyleSheet("color: #eb5e28; font-weight: bold;")
        
        # Preset controls container
        preset_controls = QHBoxLayout()
        
        self.preset_combo = QComboBox()
        self.preset_combo.currentTextChanged.connect(self.on_preset_selected)
        
        save_preset_btn = QPushButton("Save as...")
        save_preset_btn.clicked.connect(self.save_preset_dialog)
        
        manage_preset_btn = QPushButton("Manage")
        manage_preset_btn.clicked.connect(self.show_preset_manager)
        
        preset_controls.addWidget(self.preset_combo, stretch=1)
        preset_controls.addWidget(save_preset_btn)
        preset_controls.addWidget(manage_preset_btn)
        
        preset_layout.addWidget(preset_label)
        preset_layout.addLayout(preset_controls)
        
        # Blender Path Section
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
        path_label.setStyleSheet("color: #eb5e28; font-weight: bold;")
        self.blender_path_edit = QLineEdit()
        
        browse_btn = QPushButton("Browse")
        browse_btn.setFixedWidth(100)
        browse_btn.clicked.connect(self.browse_blender_path)
        
        path_layout.addWidget(path_label)
        path_layout.addWidget(self.blender_path_edit)
        path_layout.addWidget(browse_btn)
        
        general_layout.addWidget(preset_frame)
        general_layout.addWidget(path_frame)
        general_layout.addStretch()
        
        tabs.addTab(general_tab, "General")

        # ...existing code for creating parameter tabs...
        for category_name, parameters in param_categories.items():
            tab = QWidget()
            tab_layout = QVBoxLayout()
            tab_layout.setContentsMargins(20, 20, 20, 20)
            tab_layout.setSpacing(15)
            
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
            scroll_layout.setSpacing(10)  # Ridotto lo spacing
            scroll_layout.setContentsMargins(15, 10, 15, 10)  # Margini più compatti
            scroll_layout.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)  # Allinea le etichette a destra
            scroll_layout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
            
            for param in parameters:
                # Aggiungi la label con i due punti ma in una riga separata
                label = QLabel(param["name"])
                label.setStyleSheet("color: #eb5e28; font-weight: bold;")
                label.setWordWrap(True)  # Permette il wrapping del testo
                scroll_layout.addRow(label)
                
                # Aggiungi il widget del parametro nella riga successiva
                widget = self.create_parameter_widget(param)
                if widget:
                    widget.setToolTip(param["description"])
                    self.parameter_widgets[param["param"]] = widget
                    scroll_layout.addRow(widget)
                
                # Aggiungi un po' di spazio dopo ogni parametro
                spacer = QWidget()
                spacer.setFixedHeight(5)
                scroll_layout.addRow(spacer)
            
            scroll_content.setLayout(scroll_layout)
            scroll.setWidget(scroll_content)
            tab_layout.addWidget(scroll)
            tab.setLayout(tab_layout)
            tabs.addTab(tab, category_name)
        
        main_layout.addWidget(tabs)
        self.setLayout(main_layout)
        
        # Aggiorna il comando iniziale
        self.update_command()

        # Load presets
        self.load_presets()

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
            
            browse_button = QPushButton("Browse...")
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
            
            browse_button = QPushButton("Browse...")
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
        
        # Aggiorna il comando
        self.update_command()
        
        # Salva le impostazioni
        self.save_settings()
        
        # Se c'è un preset attivo, aggiornalo
        current_preset = self.preset_combo.currentText()
        if current_preset:
            # Raccogli tutte le impostazioni correnti
            current_settings = {
                'name': current_preset,
                'blender_path': self.blender_path_edit.text(),
                'parameters': self.get_current_parameters()
            }
            # Salva nel preset corrente
            self.settings_manager.save_as_preset(current_preset, current_settings)

    def update_command(self):
        """Aggiorna la visualizzazione del comando completo"""
        blender_path = self.blender_path_edit.text()
        command_parts = []
        
        # Aggiungi il percorso di Blender
        if blender_path:
            command_parts.append(f'"{blender_path}"')
        else:
            command_parts.append("blender")
        
        # Gestisci il file .blend separatamente
        blend_file = None
        background_mode = False
        
        ordered_params = []
        
        # Raccogli i parametri e gestisci -b e il file blend separatamente
        for param, value in self.parameter_values.items():
            if param == ParamDefinitions.FILE:
                blend_file = value
            elif param == ParamDefinitions.BACKGROUND and value:
                background_mode = True
            else:
                order = ParamDefinitions.get_param_order(param)
                ordered_params.append((order, param, value))
        
        # Ordina i parametri in base alla priorità
        ordered_params.sort(key=lambda x: x[0])
        
        # Gestisci -b e file blend
        if background_mode:
            if blend_file:
                command_parts.append(f'-b "{blend_file}"')
            else:
                command_parts.append("-b")
        elif blend_file:
            command_parts.append(f'"{blend_file}"')
        
        # Aggiungi gli altri parametri
        for _, param, value in ordered_params:
            if isinstance(value, bool):
                if value:
                    command_parts.append(param)
            else:
                command_parts.append(f'{param} "{value}"')
        
        # Unisci le parti con uno spazio
        command = " ".join(command_parts)
        if hasattr(self, 'main_window') and self.main_window is not None:
            self.main_window.update_command_preview(command)

    def build_command(self):
        """Build and return the command as a list"""
        # Forza l'aggiornamento del comando
        self.update_command()
        
        # Ottieni il comando dalla preview e splittalo in una lista
        # preservando le parti tra virgolette
        command_str = self.main_window.command_preview.text()
        if not command_str:
            return None
            
        # Split preservando le parti tra virgolette
        import shlex
        return shlex.split(command_str)

    def construct_command(self):
        """Internal method to construct the command"""
        blender_path = self.blender_path_edit.text()
        if not blender_path:
            return None

        command = [blender_path]
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
            elif isinstance(widget, QWidget):
                # Try to find a QLineEdit inside composite widgets
                line_edit = widget.findChild(QLineEdit)
                if line_edit:
                    value = line_edit.text()

            if value:
                # Add the parameter flag
                command.append(param_name)
                # Add the value only if it's not a boolean parameter
                if not isinstance(value, bool):
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

    def load_presets(self):
        """Carica i preset nel combo box"""
        self.preset_combo.clear()
        preset_names = self.settings_manager.get_preset_names()
        self.preset_combo.addItems(preset_names)

    def on_preset_selected(self, preset_name):
        """Gestisce la selezione di un preset"""
        if not preset_name:
            return
            
        preset = self.settings_manager.get_preset(preset_name)
        if preset:
            # Applica le impostazioni del preset
            if 'blender_path' in preset:
                self.blender_path_edit.setText(preset['blender_path'])
            
            if 'parameters' in preset:
                self.load_parameters(preset['parameters'])

    def load_parameters(self, parameters):
        """Carica i parametri nei widget corrispondenti"""
        for param_name, value in parameters.items():
            # Gestione speciale per il file .blend
            if param_name == 'blend_file':
                param_name = ParamDefinitions.FILE
            
            if param_name in self.parameter_widgets:
                widget = self.parameter_widgets[param_name]
                
                # Aggiorna il widget
                if isinstance(widget, QCheckBox):
                    widget.setChecked(bool(value))
                elif isinstance(widget, QSpinBox):
                    widget.setValue(int(value))
                elif isinstance(widget, QComboBox):
                    index = widget.findText(str(value))
                    if index >= 0:
                        widget.setCurrentIndex(index)
                elif isinstance(widget, QLineEdit):
                    widget.setText(str(value))
                elif isinstance(widget, QWidget):
                    # Cerca QLineEdit all'interno di container compositi
                    line_edit = widget.findChild(QLineEdit)
                    if line_edit:
                        line_edit.setText(str(value))
                
                # Aggiorna parameter_values
                if value:
                    if param_name == ParamDefinitions.FILE:
                        self.parameter_values[param_name] = value
                    else:
                        self.parameter_values[param_name] = value

    def save_preset_dialog(self):
        """Mostra un dialog per salvare il preset corrente"""
        name, ok = QInputDialog.getText(
            self, 
            "Save Preset",
            "Enter preset name:",
            QLineEdit.Normal,
            ""
        )
        
        if ok and name:
            # Raccogli tutte le impostazioni correnti
            current_settings = {
                'name': name,
                'blender_path': self.blender_path_edit.text(),
                'parameters': self.get_current_parameters()
            }
            
            # Salva il preset
            self.settings_manager.save_as_preset(name, current_settings)
            
            # Aggiorna la lista dei preset
            self.load_presets()
            
            # Seleziona il nuovo preset
            index = self.preset_combo.findText(name)
            if index >= 0:
                self.preset_combo.setCurrentIndex(index)

    def show_preset_manager(self):
        """Mostra il dialog per gestire i preset"""
        dialog = PresetManagerDialog(self.settings_manager, self)
        if dialog.exec_() == QDialog.Accepted:
            # Ricarica i preset dopo eventuali modifiche
            self.load_presets()

    def get_current_parameters(self):
        """Raccoglie tutti i parametri correnti dai widget"""
        parameters = {}
        for param_name, widget in self.parameter_widgets.items():
            # Gestione speciale per il file .blend
            if param_name == ParamDefinitions.FILE:
                # Salva con una chiave speciale che non interferisce col comando
                if isinstance(widget, QWidget):
                    line_edit = widget.findChild(QLineEdit)
                    if line_edit and line_edit.text():
                        parameters['blend_file'] = line_edit.text()
                continue
            
            # Gestione normale per tutti gli altri parametri
            if isinstance(widget, QCheckBox):
                parameters[param_name] = widget.isChecked()
            elif isinstance(widget, QSpinBox):
                parameters[param_name] = widget.value()
            elif isinstance(widget, QComboBox):
                parameters[param_name] = widget.currentText()
            elif isinstance(widget, QLineEdit):
                parameters[param_name] = widget.text()
            elif isinstance(widget, QWidget):
                # Cerca QLineEdit all'interno di container compositi
                line_edit = widget.findChild(QLineEdit)
                if line_edit:
                    parameters[param_name] = line_edit.text()
        return parameters

    def create_parameter_widget(self, param):
        """Crea il widget appropriato per il tipo di parametro"""
        param_type = param["type"]
        param_description = param["description"]
        
        if param_type == "bool":
            widget = QCheckBox()
            widget.stateChanged.connect(lambda state, p=param["param"]: 
                                    self.update_parameter(p, state == Qt.Checked))
            return widget
        
        elif param_type == "file":
            container = QWidget()
            file_layout = QHBoxLayout(container)
            file_layout.setContentsMargins(0, 0, 0, 0)
            file_layout.setSpacing(5)
            
            line_edit = QLineEdit()
            line_edit.setPlaceholderText(param_description)
            
            browse_button = QPushButton("...")
            browse_button.setFixedWidth(45)
            browse_button.clicked.connect(lambda _, le=line_edit, p=param["param"]: 
                                        self.browse_file(le, p))
            
            file_layout.addWidget(line_edit)
            file_layout.addWidget(browse_button)
            
            line_edit.textChanged.connect(lambda text, p=param["param"]: 
                                        self.update_parameter(p, text))
            return container
        
        elif param_type == "path":
            container = QWidget()
            path_layout = QHBoxLayout(container)
            path_layout.setContentsMargins(0, 0, 0, 0)
            path_layout.setSpacing(5)
            
            line_edit = QLineEdit()
            line_edit.setPlaceholderText(param_description)
            
            browse_button = QPushButton("...")
            browse_button.setFixedWidth(45)
            browse_button.clicked.connect(lambda _, le=line_edit, p=param["param"]: 
                                        self.browse_directory(le, p))
            
            path_layout.addWidget(line_edit)
            path_layout.addWidget(browse_button)
            
            line_edit.textChanged.connect(lambda text, p=param["param"]: 
                                        self.update_parameter(p, text))
            return container
        
        elif param_type == "string":
            widget = QLineEdit()
            widget.setPlaceholderText(param_description)
            widget.textChanged.connect(lambda text, p=param["param"]: 
                                    self.update_parameter(p, text))
            return widget
        
        elif param_type == "int":
            widget = QSpinBox()
            widget.setRange(-999999, 999999)
            widget.valueChanged.connect(lambda value, p=param["param"]: 
                                    self.update_parameter(p, value))
            return widget
        
        elif param_type == "enum" and "options" in param:
            widget = QComboBox()
            for option in param["options"]:
                widget.addItem(option)
            widget.currentTextChanged.connect(lambda text, p=param["param"]: 
                                        self.update_parameter(p, text))
            return widget
        
        return None