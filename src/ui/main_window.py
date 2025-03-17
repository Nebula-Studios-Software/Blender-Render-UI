from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                         QPushButton, QLabel, QSplitter, QMessageBox, QFrame, QLineEdit, QGroupBox, QTextEdit, QApplication)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
import os
import sys
import subprocess
from .styles import STYLE  # Aggiunto import di STYLE

from src.ui.command_builder import CommandBuilder
from src.ui.progress_monitor import ProgressMonitor
from src.ui.log_viewer import LogViewer
from src.core.blender_executor import BlenderExecutor
from src.core.param_definitions import ParamDefinitions
from src.utils.update_checker import UpdateChecker

def get_resource_path(relative_path):
    """Get the absolute path to a resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    
    return os.path.join(base_path, relative_path)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Set application icon
        icon_path = get_resource_path(os.path.join('resources', 'icons', 'app_icon.ico'))
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
            # Set application icon at process level
            if hasattr(sys, 'frozen'):  # If we're in an exe
                import ctypes
                myappid = 'nebulastudios.blenderrenderui.1.0.0'  # Arbitrary identifier
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        
        self.init_ui()
        # Controllo automatico aggiornamenti all'avvio
        self.check_for_updates(silent=True)

    def init_ui(self):
        self.setWindowTitle("Blender Render UI")
        self.setMinimumSize(1200, 800)
        
        # Create status bar
        self.statusBar().setFixedHeight(40)
        
        # App info
        app_info = QLabel("Blender Render UI | By Nebula Studios")
        self.statusBar().addPermanentWidget(app_info)
        
        # Separator
        separator = QLabel("|")
        separator.setStyleSheet("color: #2a2826;")
        self.statusBar().addPermanentWidget(separator)
        
        # Check for updates button
        self.update_button = QPushButton("Check Updates")
        self.update_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #eb5e28;
                border: none;
                padding: 5px 10px;
            }
            QPushButton:hover {
                color: #ff7f50;
            }
        """)
        self.update_button.clicked.connect(lambda: self.check_for_updates(silent=False))
        self.statusBar().addPermanentWidget(self.update_button)
        
        # Another separator
        separator2 = QLabel("|")
        separator2.setStyleSheet("color: #2a2826;")
        self.statusBar().addPermanentWidget(separator2)
        
        # Status indicator
        self.status_indicator = QLabel("⬤ Waiting")
        self.status_indicator.setObjectName("statusIndicator")
        self.status_indicator.setProperty("status", "idle")
        self.statusBar().addPermanentWidget(self.status_indicator)
        
        self.setStyleSheet(STYLE)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Crea il QSplitter con handle più visibile e interattivo
        splitter = QSplitter(Qt.Horizontal)
        splitter.setHandleWidth(4)  # Handle più largo per una migliore interazione
        splitter.setChildrenCollapsible(False)  # Impedisce il collasso totale delle sezioni
        splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #2d2d2d;
                margin: 0 2px;
            }
            QSplitter::handle:hover {
                background-color: #eb5e28;
            }
            QSplitter::handle:pressed {
                background-color: #eb5e28;
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
        right_container.setMinimumWidth(400)  # Larghezza minima per la sezione destra
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
        
        # Command Preview e buttons
        preview_label = QLabel("Command Preview")
        preview_label.setStyleSheet("color: #eb5e28; font-weight: bold;")
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
        
        # Comando buttons
        command_buttons_layout = QHBoxLayout()
        command_buttons_layout.setSpacing(10)
        
        self.copy_button = QPushButton("Copy Command")
        self.copy_button.setFixedWidth(150)
        self.copy_button.clicked.connect(self.copy_command)
        self.copy_button.setStyleSheet("""
            QPushButton {
                background-color: #1a1918;
                color: #eb5e28;
                border: 2px solid #eb5e28;
                border-radius: 4px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #eb5e28;
                color: #fffcf2;
            }
        """)
        
        self.reset_button = QPushButton("Reset")
        self.reset_button.setFixedWidth(100)
        self.reset_button.clicked.connect(self.reset_command)
        self.reset_button.setStyleSheet("""
            QPushButton {
                background-color: #1a1918;
                color: #ff0040;
                border: 2px solid #ff0040;
                border-radius: 4px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #ff0040;
                color: #fffcf2;
            }
        """)
        
        command_buttons_layout.addWidget(self.copy_button)
        command_buttons_layout.addWidget(self.reset_button)
        command_buttons_layout.addStretch()
        
        # Render buttons
        render_buttons_layout = QHBoxLayout()
        render_buttons_layout.setSpacing(10)
        
        self.render_button = QPushButton("Start Render")
        self.render_button.setFixedHeight(40)
        self.render_button.setStyleSheet("""
            QPushButton {
                background-color: #00ff73;
                color: #131211;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #00e566;
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
                background-color: #ff0040;
                color: #fffcf2;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e50039;
            }
            QPushButton:disabled {
                background-color: #404040;
                color: #808080;
            }
        """)
        self.stop_button.clicked.connect(self.stop_render)
        
        self.open_output_button = QPushButton("Open Output Folder")
        self.open_output_button.setFixedHeight(40)
        self.open_output_button.setEnabled(False)
        self.open_output_button.setStyleSheet("""
            QPushButton {
                background-color: #1a1918;
                color: #eb5e28;
                border: 2px solid #eb5e28;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #eb5e28;
                color: #fffcf2;
            }
            QPushButton:disabled {
                background-color: #1a1918;
                border-color: #666666;
                color: #666666;
            }
        """)
        self.open_output_button.clicked.connect(self.open_output_directory)
        
        render_buttons_layout.addWidget(self.render_button)
        render_buttons_layout.addWidget(self.stop_button)
        render_buttons_layout.addWidget(self.open_output_button)
        render_buttons_layout.addStretch()
        
        top_layout.addWidget(preview_label)
        top_layout.addWidget(self.command_preview)
        top_layout.addLayout(command_buttons_layout)
        top_layout.addLayout(render_buttons_layout)
        
        # Progress Monitor e Log Viewer
        self.progress_monitor = ProgressMonitor()
        self.log_viewer = LogViewer()
        
        # Initialize BlenderExecutor and connect signals
        self.blender_executor = BlenderExecutor()
        self.progress_monitor.set_blender_executor(self.blender_executor)  # Pass the reference
        self.connect_signals()
        
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
        left_container.setMinimumWidth(300)  # Larghezza minima per la sezione sinistra
        
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
        
        # Set initial proportions (60% left, 40% right)
        total_width = self.width()
        splitter.setSizes([int(total_width * 0.6), int(total_width * 0.4)])
        
        main_layout.addWidget(splitter)
        central_widget.setLayout(main_layout)
        
        self.center_window()
    
    def center_window(self):
        """Center the window on the screen"""
        frame = self.frameGeometry()
        screen = self.screen().availableGeometry().center()
        frame.moveCenter(screen)
        self.move(frame.topLeft())
    
    def connect_signals(self):
        """Connect signals between various components"""
        # Signals from BlenderExecutor to LogViewer
        self.blender_executor.output_received.connect(self.handle_output_received)
        self.blender_executor.render_started.connect(self.handle_render_started)
        self.blender_executor.render_completed.connect(self.handle_render_completed)
        self.blender_executor.render_progress.connect(self.handle_render_progress)
    
    def handle_output_received(self, output_line):
        """Handles a new output line from the Blender process"""
        self.log_viewer.process_blender_output(output_line)
        self.progress_monitor.parse_blender_output(output_line)
    
    def handle_render_started(self):
        """Handles the render start event"""
        self.render_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.log_viewer.append_log("Rendering started", "INFO")
        self.status_indicator.setText("⬤ In Progress")
        self.status_indicator.setProperty("status", "rendering")
        self.status_indicator.style().unpolish(self.status_indicator)
        self.status_indicator.style().polish(self.status_indicator)
    
    def handle_render_completed(self, success, message):
        """Handles the render completion event"""
        self.render_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.open_output_button.setEnabled(True)  # Enable the output button
        
        log_level = "INFO" if success else "ERROR"
        self.log_viewer.append_log(message, log_level)
        
        # Update status indicator
        if success:
            self.status_indicator.setText("⬤ Completed")
            self.status_indicator.setProperty("status", "completed")
        else:
            self.status_indicator.setText("⬤ Error")
            self.status_indicator.setProperty("status", "error")
        self.status_indicator.style().unpolish(self.status_indicator)
        self.status_indicator.style().polish(self.status_indicator)
        
        # Show message to user
        if success:
            QMessageBox.information(self, "Rendering Completed", message)
        else:
            QMessageBox.warning(self, "Rendering Failed", message)
    
    def handle_render_progress(self, progress):
        """Handles a render progress update"""
        progress_percent = int(progress * 100)
        # No need to update the UI here as it is done via parse_blender_output
    
    def run_render(self):
        """Starts the rendering process with configured parameters"""
        # Get command from CommandBuilder
        command = self.command_builder.build_command()
        
        if not command:
            QMessageBox.warning(self, "Error", "Invalid command or Blender path not specified")
            return
        
        # Extract frame start and end values from parameters
        start_frame = 1
        end_frame = 1
        
        # First check for animation render
        is_animation = False
        for i, arg in enumerate(command):
            if arg == ParamDefinitions.RENDER:
                is_animation = True
                break
        
        # If animation, look for start/end frames
        if is_animation:
            for i, arg in enumerate(command):
                if (arg == ParamDefinitions.FRAME_START and i + 1 < len(command)):
                    try:
                        start_frame = int(command[i + 1])
                    except ValueError:
                        pass
                elif (arg == ParamDefinitions.FRAME_END and i + 1 < len(command)):
                    try:
                        end_frame = int(command[i + 1])
                    except ValueError:
                        pass
        # If not animation, check for single frame
        else:
            for i, arg in enumerate(command):
                if (arg == ParamDefinitions.RENDER_FRAME and i + 1 < len(command)):
                    try:
                        frame_value = command[i + 1]
                        # Handle range notation (e.g., "1-10")
                        if "-" in frame_value:
                            parts = frame_value.split("-")
                            if len(parts) == 2:
                                start_frame = int(parts[0])
                                end_frame = int(parts[1])
                        else:
                            # Single frame
                            start_frame = int(frame_value)
                            end_frame = start_frame
                    except ValueError:
                        pass
        
        # Reset log and monitor
        self.log_viewer.append_log("Preparing rendering...", "INFO")
        self.progress_monitor.reset()
        
        # Set total frames in progress monitor
        self.progress_monitor.set_total_frames(start_frame, end_frame)
        
        # Execute Blender command
        success = self.blender_executor.execute(command, start_frame, end_frame)
        
        if not success:
            QMessageBox.warning(self, "Error", "Unable to start rendering. Check logs for more details.")
    
    def stop_render(self):
        """Stops the current rendering process"""
        if self.blender_executor.is_rendering():
            confirm = QMessageBox.question(
                self, 
                "Confirm Stop", 
                "Are you sure you want to stop the current rendering?",
                QMessageBox.Yes | QMessageBox.No, 
                QMessageBox.No
            )
            
            if confirm == QMessageBox.Yes:
                success = self.blender_executor.terminate()
                if not success:
                    QMessageBox.warning(self, "Error", "Unable to stop rendering")
    
    def closeEvent(self, event):
        """Handles window close event"""
        if self.blender_executor.is_rendering():
            confirm = QMessageBox.question(
                self, 
                "Confirm Exit", 
                "A rendering is in progress. Stop it and exit?",
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
        command_text = self.command_preview.text()
        if command_text:
            clipboard = QApplication.clipboard()
            clipboard.setText(command_text)

    def reset_command(self):
        self.command_preview.clear()
        # Reset the command builder
        self.command_builder.load_saved_settings()

    def open_output_directory(self):
        """Opens the output directory in file explorer"""
        # Get the output path from the command builder
        output_path = None
        for param_name, widget in self.command_builder.parameter_widgets.items():
            if param_name == ParamDefinitions.RENDER_OUTPUT:
                if isinstance(widget, QWidget):
                    line_edit = widget.findChild(QLineEdit)
                    if line_edit:
                        output_path = os.path.dirname(line_edit.text())
                        break

        if output_path and os.path.exists(output_path):
            # Use the default system file explorer to open the directory
            if sys.platform == "win32":
                os.startfile(output_path)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", output_path])
            else:
                subprocess.Popen(["xdg-open", output_path])
        else:
            QMessageBox.warning(self, "Error", "Output directory not found or not specified")

    def check_for_updates(self, silent=False):
        """Controlla la disponibilità di aggiornamenti"""
        update_available, latest_version, download_url = UpdateChecker.check_for_updates()
        
        if update_available and latest_version and download_url:
            reply = QMessageBox.question(
                self,
                "Update Available",
                f"A new version ({latest_version}) is available!\n\n"
                f"Would you like to download it?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.Yes
            )
            
            if reply == QMessageBox.Yes:
                import webbrowser
                webbrowser.open(download_url)
        elif not silent:
            QMessageBox.information(
                self,
                "No Updates",
                "You are using the latest version.",
                QMessageBox.Ok
            )