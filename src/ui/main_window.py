from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                         QPushButton, QLabel, QSplitter, QMessageBox, QFrame, QLineEdit, QGroupBox, QTextEdit, QApplication)
from PyQt5.QtCore import Qt, QSize, QThread

from src.ui.command_builder import CommandBuilder
from src.ui.progress_monitor import ProgressMonitor
from src.ui.log_viewer import LogViewer
from src.core.blender_executor import BlenderExecutor
from src.core.param_definitions import ParamDefinitions
from .styles import STYLE


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Blender Render UI")
        self.setMinimumSize(1200, 800)
        
        self.setStyleSheet(STYLE)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        splitter = QSplitter(Qt.Horizontal)
        splitter.setHandleWidth(2)
        splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #2d2d2d;
            }
            QSplitter::handle:hover {
                background-color: #00b4d8;
            }
        """)
        
        # Right container first to ensure command_preview exists
        right_container = QFrame()
        right_container.setObjectName("rightContainer")
        right_container.setStyleSheet("""
            #rightContainer {
                background-color: #1e1e1e;
                border-left: 1px solid #333333;
            }
        """)
        right_layout = QVBoxLayout(right_container)
        right_layout.setContentsMargins(10, 10, 10, 10)
        right_layout.setSpacing(10)
        
        # Container per i pulsanti e preview
        top_frame = QFrame()
        top_frame.setObjectName("topFrame")
        top_frame.setStyleSheet("""
            #topFrame {
                background-color: #252525;
                border-radius: 8px;
            }
        """)
        top_layout = QVBoxLayout(top_frame)
        top_layout.setContentsMargins(15, 15, 15, 15)
        top_layout.setSpacing(10)
        
        # Command Preview
        preview_label = QLabel("Command Preview")
        preview_label.setStyleSheet("color: #00b4d8; font-weight: bold;")
        self.command_preview = QLineEdit()
        self.command_preview.setReadOnly(True)
        self.command_preview.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                background: #1e1e1e;
                border: 1px solid #333333;
                border-radius: 4px;
                color: #e0e0e0;
            }
        """)
        
        # Pulsanti Render e Stop
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        
        self.render_button = QPushButton("Start Render")
        self.render_button.setFixedHeight(40)
        self.render_button.setStyleSheet("""
            QPushButton {
                background-color: #00b4d8;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0096b4;
            }
            QPushButton:disabled {
                background-color: #404040;
                color: #808080;
            }
        """)
        self.render_button.clicked.connect(self.run_render)
        
        self.stop_button = QPushButton("Stop")
        self.stop_button.setFixedHeight(40)
        self.stop_button.setEnabled(False)
        self.stop_button.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #bb2d3b;
            }
            QPushButton:disabled {
                background-color: #404040;
                color: #808080;
            }
        """)
        self.stop_button.clicked.connect(self.stop_render)
        
        buttons_layout.addWidget(self.render_button)
        buttons_layout.addWidget(self.stop_button)
        buttons_layout.addStretch()
        
        top_layout.addWidget(preview_label)
        top_layout.addWidget(self.command_preview)
        top_layout.addLayout(buttons_layout)
        
        # Progress Monitor e Log Viewer
        self.progress_monitor = ProgressMonitor()
        self.log_viewer = LogViewer()
        
        right_layout.addWidget(top_frame)
        right_layout.addWidget(self.progress_monitor)
        right_layout.addWidget(self.log_viewer, stretch=1)
        
        # Now create the left container since command_preview exists
        left_container = QFrame()
        left_container.setObjectName("leftContainer")
        left_container.setStyleSheet("""
            #leftContainer {
                background-color: #1e1e1e;
                border: none;
            }
        """)
        left_layout = QVBoxLayout(left_container)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(0)
        
        # Create CommandBuilder after command_preview exists
        self.command_builder = CommandBuilder(self)
        self.command_builder.main_window = self
        left_layout.addWidget(self.command_builder)
        
        # Add containers to splitter
        splitter.addWidget(left_container)
        splitter.addWidget(right_container)
        
        # Set initial proportions (70% left, 30% right)
        splitter.setSizes([840, 360])
        
        main_layout.addWidget(splitter)
        central_widget.setLayout(main_layout)
        
        # Initialize BlenderExecutor and connect signals
        self.blender_executor = BlenderExecutor()
        self.connect_signals()
        
        self.center_window()
    
    def center_window(self):
        """Centra la finestra sullo schermo"""
        frame = self.frameGeometry()
        screen = self.screen().availableGeometry().center()
        frame.moveCenter(screen)
        self.move(frame.topLeft())
    
    def connect_signals(self):
        """Collega i segnali tra i vari componenti"""
        # Segnali dal BlenderExecutor al LogViewer
        self.blender_executor.output_received.connect(self.handle_output_received)
        self.blender_executor.render_started.connect(self.handle_render_started)
        self.blender_executor.render_completed.connect(self.handle_render_completed)
        self.blender_executor.render_progress.connect(self.handle_render_progress)
    
    def handle_output_received(self, output_line):
        """Gestisce una nuova linea di output dal processo Blender"""
        self.log_viewer.process_blender_output(output_line)
        self.progress_monitor.parse_blender_output(output_line)
    
    def handle_render_started(self):
        """Gestisce l'evento di avvio del rendering"""
        self.render_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.log_viewer.append_log("Rendering avviato", "INFO")
    
    def handle_render_completed(self, success, message):
        """Gestisce l'evento di completamento del rendering"""
        self.render_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        
        log_level = "INFO" if success else "ERROR"
        self.log_viewer.append_log(message, log_level)
        
        # Mostra un messaggio all'utente
        if success:
            QMessageBox.information(self, "Rendering Completato", message)
        else:
            QMessageBox.warning(self, "Rendering Fallito", message)
    
    def handle_render_progress(self, progress):
        """Gestisce un aggiornamento del progresso del rendering"""
        progress_percent = int(progress * 100)
        # Non c'è bisogno di aggiornare la UI qui poiché viene fatto tramite parse_blender_output
    
    def run_render(self):
        """Avvia il processo di rendering con i parametri configurati"""
        # Ottieni il comando da CommandBuilder
        command = self.command_builder.build_command()
        
        if not command:
            QMessageBox.warning(self, "Errore", "Comando non valido o percorso Blender non specificato")
            return
        
        # Estrai i valori di frame start e end dai parametri se disponibili
        start_frame = 1
        end_frame = 1
        
        # Cerca i parametri di frame nel comando
        for i, arg in enumerate(command):
            if arg == ParamDefinitions.FRAME_START and i + 1 < len(command):
                try:
                    start_frame = int(command[i + 1])
                except ValueError:
                    pass
            elif arg == ParamDefinitions.FRAME_END and i + 1 < len(command):
                try:
                    end_frame = int(command[i + 1])
                except ValueError:
                    pass
        
        # Imposta il numero totale di frame nel progress monitor
        self.progress_monitor.set_total_frames(start_frame, end_frame)
        
        # Reset del log e del monitor
        self.log_viewer.append_log("Preparazione rendering...", "INFO")
        self.progress_monitor.reset()
        
        # Esegui il comando Blender
        success = self.blender_executor.execute(command, start_frame, end_frame)
        
        if not success:
            QMessageBox.warning(self, "Errore", "Impossibile avviare il rendering. Controlla i log per maggiori dettagli.")
    
    def stop_render(self):
        """Interrompe il processo di rendering in corso"""
        if self.blender_executor.is_rendering():
            confirm = QMessageBox.question(
                self, 
                "Conferma Interruzione", 
                "Sei sicuro di voler interrompere il rendering in corso?",
                QMessageBox.Yes | QMessageBox.No, 
                QMessageBox.No
            )
            
            if confirm == QMessageBox.Yes:
                success = self.blender_executor.terminate()
                if not success:
                    QMessageBox.warning(self, "Errore", "Impossibile interrompere il rendering")
    
    def closeEvent(self, event):
        """Gestisce l'evento di chiusura della finestra"""
        if self.blender_executor.is_rendering():
            confirm = QMessageBox.question(
                self, 
                "Conferma Uscita", 
                "Un rendering è in corso. Terminarlo e uscire?",
                QMessageBox.Yes | QMessageBox.No, 
                QMessageBox.No
            )
            
            if confirm == QMessageBox.Yes:
                self.blender_executor.terminate()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

    def update_command_preview(self, command):
        """Updates the command preview text field with the given command"""
        if command:
            self.command_preview.setText(command)
        else:
            self.command_preview.clear()

    def copy_command(self):
        command_text = self.command_preview.toPlainText()
        if command_text:
            clipboard = QApplication.clipboard()
            clipboard.setText(command_text)

    def reset_command(self):
        self.command_preview.clear()
        # Reset the command builder
        self.command_builder.load_saved_settings()