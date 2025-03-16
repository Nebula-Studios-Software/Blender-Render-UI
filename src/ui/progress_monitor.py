from PyQt5.QtWidgets import QWidget, QVBoxLayout, QProgressBar, QLabel, QGroupBox, QHBoxLayout
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot
from ..utils.settings_manager import SettingsManager
import time
import re

class RenderThread(QThread):
    progress = pyqtSignal(int)

    def run(self):
        for i in range(101):
            time.sleep(0.1)  # Simulate rendering time
            self.progress.emit(i)

class ProgressMonitor(QGroupBox):
    # Segnali per aggiornare la UI dal thread di rendering
    frame_updated = pyqtSignal(int, int)  # frame corrente, frame totale
    render_time_updated = pyqtSignal(str)  # tempo di rendering
    remaining_time_updated = pyqtSignal(str)  # tempo rimanente stimato
    render_completed = pyqtSignal()  # rendering completato

    def __init__(self):
        super().__init__("Rendering Progress")
        self.settings_manager = SettingsManager()
        self.current_frame = 0
        self.total_frames = 0
        
        # Carica le impostazioni salvate
        saved_settings = self.settings_manager.get_setting('progress_monitor', {})
        self.window_state = saved_settings.get('window_state', None)
        
        self.init_ui()
        
        # Collega i segnali ai metodi di aggiornamento UI
        self.frame_updated.connect(self.update_progress)
        self.render_time_updated.connect(self.update_render_time)
        self.remaining_time_updated.connect(self.update_remaining_time)
        self.render_completed.connect(self.handle_render_completed)
        
        # Ripristina lo stato della finestra se salvato
        if self.window_state:
            self.restoreGeometry(self.window_state)
    
    def save_settings(self):
        """Salva le impostazioni correnti"""
        settings = {
            'window_state': self.saveGeometry(),
            'current_frame': self.current_frame,
            'total_frames': self.total_frames
        }
        self.settings_manager.set_setting('progress_monitor', settings)
        self.settings_manager.save_settings()
    
    def closeEvent(self, event):
        """Salva le impostazioni quando la finestra viene chiusa"""
        self.save_settings()
        super().closeEvent(event)
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(10, 15, 10, 10)
        
        # Info Container superiore
        top_info_container = QWidget()
        top_info_layout = QHBoxLayout(top_info_container)
        top_info_layout.setContentsMargins(0, 0, 0, 0)
        top_info_layout.setSpacing(20)
        
        # Frame Counter con stile moderno
        self.frame_label = QLabel("Frame: 0/0")
        self.frame_label.setStyleSheet("""
            QLabel {
                color: #00b4d8;
                font-size: 11pt;
                font-weight: bold;
            }
        """)
        top_info_layout.addWidget(self.frame_label)
        
        # Percentuale con stile moderno
        self.percentage_label = QLabel("0%")
        self.percentage_label.setStyleSheet("""
            QLabel {
                color: #00b4d8;
                font-size: 11pt;
                font-weight: bold;
            }
        """)
        top_info_layout.addWidget(self.percentage_label)
        
        top_info_layout.addStretch()
        layout.addWidget(top_info_container)
        
        # Info Container inferiore
        bottom_info_container = QWidget()
        bottom_info_layout = QHBoxLayout(bottom_info_container)
        bottom_info_layout.setContentsMargins(0, 0, 0, 0)
        bottom_info_layout.setSpacing(20)
        
        # Status Label
        self.status_label = QLabel("In attesa...")
        self.status_label.setStyleSheet("""
            QLabel {
                color: #e0e0e0;
                font-size: 10pt;
            }
        """)
        bottom_info_layout.addWidget(self.status_label)
        
        # Tempo di Rendering
        self.render_time_label = QLabel("Tempo: 00:00:00")
        self.render_time_label.setStyleSheet("""
            QLabel {
                color: #e0e0e0;
                font-size: 10pt;
            }
        """)
        bottom_info_layout.addWidget(self.render_time_label)
        
        # Tempo Rimanente
        self.eta_label = QLabel("Rimanente: 00:00:00")
        self.eta_label.setStyleSheet("""
            QLabel {
                color: #e0e0e0;
                font-size: 10pt;
            }
        """)
        bottom_info_layout.addWidget(self.eta_label)
        
        bottom_info_layout.addStretch()
        layout.addWidget(bottom_info_container)
        
        # Progress Bar con stile moderno
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #3d3d3d;
                border-radius: 6px;
                background-color: #2d2d2d;
                height: 12px;
                text-align: center;
            }
            
            QProgressBar::chunk {
                background-color: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0077b6,
                    stop:1 #00b4d8
                );
                border-radius: 4px;
            }
        """)
        layout.addWidget(self.progress_bar)
        
        # Frame Progress Bar con stile moderno
        self.frame_progress = QProgressBar()
        self.frame_progress.setTextVisible(False)
        self.frame_progress.setStyleSheet("""
            QProgressBar {
                border: 2px solid #3d3d3d;
                border-radius: 6px;
                background-color: #2d2d2d;
                height: 8px;
                text-align: center;
            }
            
            QProgressBar::chunk {
                background-color: #00b4d8;
                border-radius: 3px;
            }
        """)
        layout.addWidget(self.frame_progress)
        
        self.setLayout(layout)
        self.reset()
    
    @pyqtSlot(int, int)
    def update_progress(self, current_frame, total_frames):
        """Aggiorna la progress bar e le informazioni sui frame"""
        self.current_frame = current_frame
        self.total_frames = total_frames
        
        if total_frames > 0:
            progress = int((current_frame / total_frames) * 100)
            self.progress_bar.setValue(progress)
            self.frame_label.setText(f"Frame: {current_frame}/{total_frames}")
            self.status_label.setText(f"Rendering frame {current_frame}...")
    
    @pyqtSlot(str)
    def update_render_time(self, time_str):
        """Aggiorna il tempo di rendering visualizzato"""
        self.render_time_label.setText(f"Tempo: {time_str}")
    
    @pyqtSlot(str)
    def update_remaining_time(self, time_str):
        """Aggiorna il tempo rimanente stimato"""
        self.eta_label.setText(f"Rimanente: {time_str}")
    
    @pyqtSlot()
    def handle_render_completed(self):
        """Gestisce il completamento del rendering"""
        self.status_label.setText("Rendering completato!")
        # Assicura che la progress bar sia al 100%
        self.progress_bar.setValue(100)
        self.frame_progress.setValue(100)
    
    def reset(self):
        """Resetta il monitor del progresso per un nuovo rendering"""
        self.progress_bar.setValue(0)
        self.frame_progress.setValue(0)
        self.frame_label.setText("Frame: 0/0")
        self.percentage_label.setText("0%")
        self.render_time_label.setText("Tempo: 00:00:00")
        self.eta_label.setText("Rimanente: 00:00:00")
        self.status_label.setText("In attesa...")
        self.current_frame = 0
        self.total_frames = 0
    
    def parse_blender_output(self, line):
        """Analizza una linea di output di Blender per estrarre informazioni sul progresso"""
        # Estrae il frame corrente (es: "Fra:10 Mem:...")
        frame_match = re.search(r'Fra:(\d+)', line)
        if frame_match:
            current_frame = int(frame_match.group(1))
            if self.total_frames > 0:  # Aggiorna solo se conosciamo il totale
                self.frame_updated.emit(current_frame, self.total_frames)
        
        # Estrae il tempo di rendering (es: "Time:00:00.99")
        time_match = re.search(r'Time:([\d:.]+)', line)
        if time_match:
            render_time = time_match.group(1)
            self.render_time_updated.emit(render_time)
        
        # Estrae il tempo rimanente stimato (es: "Remaining:00:03.85")
        remaining_match = re.search(r'Remaining:([\d:.]+)', line)
        if remaining_match:
            remaining_time = remaining_match.group(1)
            self.remaining_time_updated.emit(remaining_time)
        
        # Rileva il completamento del rendering
        if "Blender quit" in line or "Rendering completed" in line:
            self.render_completed.emit()
    
    def set_total_frames(self, start_frame, end_frame):
        """Imposta il numero totale di frame da renderizzare"""
        if end_frame >= start_frame:
            self.total_frames = end_frame - start_frame + 1
            self.frame_label.setText(f"Frame: 0/{self.total_frames}")
            # Reimposta la range della progress bar
            self.progress_bar.setRange(0, self.total_frames)