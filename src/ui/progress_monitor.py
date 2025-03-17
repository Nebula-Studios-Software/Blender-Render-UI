from PyQt5.QtWidgets import QWidget, QVBoxLayout, QProgressBar, QLabel, QGroupBox, QHBoxLayout, QGridLayout
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot, QTimer
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
    # Signals to update the UI from the rendering thread
    frame_updated = pyqtSignal(int, int)  # current frame, total frame
    render_time_updated = pyqtSignal(str)  # rendering time
    remaining_time_updated = pyqtSignal(str)  # estimated remaining time
    render_completed = pyqtSignal()  # rendering completed

    def __init__(self):
        super().__init__("Rendering Progress")
        self.settings_manager = SettingsManager()
        self.current_frame = 0
        self.start_frame = 1
        self.end_frame = 1
        self.total_frames = 0
        self.current_sample = 0
        self.total_samples = 0
        self.in_compositing = False
        self.compositing_operation = ""
        self.current_memory = ""
        self.peak_memory = ""
        self.using_cycles = False  # Flag to indicate if we are using Cycles
        self.render_start_time = None
        self.blender_executor = None  # Will be set by MainWindow
        
        # Load saved settings
        saved_settings = self.settings_manager.get_setting('progress_monitor', {})
        self.window_state = saved_settings.get('window_state', None)
        
        self.init_ui()
        
        # Connect signals to UI update methods
        self.frame_updated.connect(self.update_progress)
        self.render_time_updated.connect(self.update_render_time)
        self.remaining_time_updated.connect(self.update_remaining_time)
        self.render_completed.connect(self.handle_render_completed)
        
        # Restore window state if saved
        if self.window_state:
            self.restoreGeometry(self.window_state)
    
    def save_settings(self):
        """Save current settings"""
        settings = {
            'window_state': self.saveGeometry(),
            'current_frame': self.current_frame,
            'total_frames': self.total_frames
        }
        self.settings_manager.set_setting('progress_monitor', settings)
        self.settings_manager.save_settings()
    
    def closeEvent(self, event):
        """Save settings when the window is closed"""
        self.save_settings()
        super().closeEvent(event)
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(10, 15, 10, 10)

        # Info section
        info_layout = QHBoxLayout()
        
        self.frame_label = QLabel("Frame: 0/0")
        self.frame_label.setStyleSheet("color: #eb5e28; font-weight: bold;")
        info_layout.addWidget(self.frame_label)
        
        self.memory_label = QLabel("Memory: 0MB (Peak: 0MB)")
        self.memory_label.setStyleSheet("color: #e0e0e0;")
        info_layout.addWidget(self.memory_label)
        
        self.time_label = QLabel("Time: 00:00:00")
        self.time_label.setStyleSheet("color: #e0e0e0;")
        info_layout.addWidget(self.time_label)
        
        info_layout.addStretch()
        layout.addLayout(info_layout)

        # Status section
        status_layout = QHBoxLayout()
        
        self.status_label = QLabel("Waiting...")
        self.status_label.setStyleSheet("color: #eb5e28;")
        status_layout.addWidget(self.status_label)
        
        self.scene_label = QLabel("")
        self.scene_label.setStyleSheet("color: #e0e0e0;")
        status_layout.addWidget(self.scene_label)
        
        status_layout.addStretch()
        layout.addLayout(status_layout)

        # Progress bars section
        progress_section = QVBoxLayout()
        progress_section.setSpacing(10)

        # Frame Progress
        frame_label = QLabel("Frame Progress")
        frame_label.setStyleSheet("color: #e0e0e0; font-weight: bold;")
        progress_section.addWidget(frame_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setFormat("%v%")
        self.progress_bar.setMinimumHeight(20)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #3d3d3d;
                border-radius: 6px;
                background-color: #2d2d2d;
                text-align: center;
                font-size: 9pt;
            }
            QProgressBar::chunk {
                background-color: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0077b6,
                    stop:1 #eb5e28
                );
                border-radius: 4px;
            }
        """)
        progress_section.addWidget(self.progress_bar)

        # Sample Progress
        self.sample_label = QLabel("Sample Progress")
        self.sample_label.setStyleSheet("color: #e0e0e0; font-weight: bold;")
        progress_section.addWidget(self.sample_label)

        self.sample_progress = QProgressBar()
        self.sample_progress.setFormat("Sample %v/%m")
        self.sample_progress.setMinimum(0)
        self.sample_progress.setMaximum(1)  # Inizializziamo a 1 per evitare divisione per zero
        self.sample_progress.setMinimumHeight(20)
        self.sample_progress.setStyleSheet("""
            QProgressBar {
                border: 2px solid #3d3d3d;
                border-radius: 6px;
                background-color: #2d2d2d;
                text-align: center;
                font-size: 9pt;
            }
            QProgressBar::chunk {
                background-color: #eb5e28;
                border-radius: 4px;
            }
        """)
        progress_section.addWidget(self.sample_progress)

        layout.addLayout(progress_section)
        self.setLayout(layout)
        
        # Initialize visibility
        self.sample_label.hide()
        self.sample_progress.hide()

    def reset(self):
        """Resets the progress monitor for a new render"""
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("Frame %v%")
        self.sample_progress.setValue(0)
        self.sample_progress.setMaximum(1)  # Reset to 1 invece che 100
        self.sample_progress.setFormat("Sample %v/%m")
        self.frame_label.setText("Frame: 0/0")
        self.memory_label.setText("Memory: 0MB (Peak: 0MB)")
        self.time_label.setText("Time: 00:00:00")
        self.status_label.setText("Waiting...")
        self.scene_label.setText("")
        self.current_frame = 0
        self.total_frames = 0
        self.current_sample = 0
        self.total_samples = 0
        self.in_compositing = False
        self.using_cycles = False
        self.render_start_time = None
        # Hide sample section
        self.sample_label.hide()
        self.sample_progress.hide()

    @pyqtSlot(int, int)
    def update_progress(self, current_frame, total_frames):
        """Update the progress bar and frame information"""
        self.current_frame = current_frame
        self.total_frames = total_frames
        
        if total_frames > 0:
            progress = int((current_frame / total_frames) * 100)
            self.progress_bar.setValue(progress)
            self.frame_label.setText(f"Frame: {current_frame}/{total_frames}")
            self.status_label.setText(f"Rendering frame {current_frame}...")
    
    @pyqtSlot(str)
    def update_render_time(self, time_str):
        """Update the displayed rendering time"""
        self.render_time_label.setText(f"Time: {time_str}")
    
    @pyqtSlot(str)
    def update_remaining_time(self, time_str):
        """Update the estimated remaining time"""
        self.eta_label.setText(f"Remaining: {time_str}")
    
    @pyqtSlot()
    def handle_render_completed(self):
        """Handles render completion"""
        self.status_label.setText("Rendering completed!")
        # Ensure progress bar is at 100%
        self.progress_bar.setValue(100)
        self.sample_progress.setValue(100)
    
    def start_render(self):
        """Called when rendering starts"""
        self.render_start_time = time.time()
        self.update_elapsed_time()

    def set_blender_executor(self, executor):
        """Sets the BlenderExecutor reference"""
        self.blender_executor = executor

    def update_elapsed_time(self):
        """Updates the elapsed time display"""
        if self.render_start_time is None:
            return
        
        elapsed = int(time.time() - self.render_start_time)
        hours = elapsed // 3600
        minutes = (elapsed % 3600) // 60
        seconds = elapsed % 60
        self.time_label.setText(f"Time: {hours:02d}:{minutes:02d}:{seconds:02d}")
        
        # Continue updating while rendering
        if self.blender_executor and self.blender_executor.is_running:
            QTimer.singleShot(1000, self.update_elapsed_time)
    
    def parse_blender_output(self, line):
        """Parses a line of Blender output to extract progress information"""
        # Start timing on first frame
        if self.render_start_time is None and "Fra:" in line:
            self.start_render()

        # Handle sample progress first (since it's the most specific)
        sample_match = re.search(r'Sample (\d+)/(\d+)', line)
        if sample_match:
            try:
                current_sample = int(sample_match.group(1))
                total_samples = int(sample_match.group(2))
                
                # Se è il primo sample che troviamo, mostriamo la progress bar
                if not self.using_cycles:
                    self.using_cycles = True
                    self.sample_label.show()
                    self.sample_progress.show()
                    self.sample_progress.setMaximum(total_samples)
                
                # Aggiorna il valore corrente
                self.sample_progress.setValue(current_sample)
                self.current_sample = current_sample
                self.total_samples = total_samples
                
                # Forza l'aggiornamento del testo
                self.sample_progress.setFormat(f"Sample {current_sample}/{total_samples}")
                self.status_label.setText(f"Rendering sample {current_sample}/{total_samples}")
            except (ValueError, IndexError) as e:
                print(f"Error parsing sample numbers: {e}")
                return

        # Handle frame progress
        frame_match = re.search(r'Fra:(\d+)', line)
        if frame_match:
            self.current_frame = int(frame_match.group(1))
            self.frame_label.setText(f"Frame: {self.current_frame}/{self.end_frame}")
            if self.total_frames > 0:
                progress = int(((self.current_frame - self.start_frame + 1) / self.total_frames) * 100)
                progress = max(0, min(100, progress))
                self.progress_bar.setValue(progress)
                self.progress_bar.setFormat(f"{progress}%")

        # Handle compositing separately
        if "Compositing" in line and "Sample" not in line:
            self.in_compositing = True
            if "|" in line:
                comp_match = re.search(r'Compositing \| (.*?)(?=\||$)', line)
                if comp_match:
                    self.compositing_operation = comp_match.group(1).strip()
                    self.status_label.setText(f"Compositing: {self.compositing_operation}")
            else:
                self.status_label.setText("Compositing")
                
        # Handle memory info
        mem_match = re.search(r'Mem:([\d.]+)([MG]).*Peak\s+([\d.]+)([MG])', line)
        if mem_match:
            current = float(mem_match.group(1))
            current_unit = mem_match.group(2)
            peak = float(mem_match.group(3))
            peak_unit = mem_match.group(4)
            
            if current_unit == 'G':
                current *= 1024
            if peak_unit == 'G':
                peak *= 1024
            
            self.memory_label.setText(f"Memory: {current:.2f}MB (Peak: {peak:.2f}MB)")

        # Handle scene info
        scene_match = re.search(r'\| ([^|]+), ([^|]+) \|', line)
        if scene_match:
            scene = scene_match.group(1).strip()
            viewlayer = scene_match.group(2).strip()
            self.scene_label.setText(f"{scene} - {viewlayer}")

        # Handle render completion
        if "Finished" in line:
            if self.using_cycles:
                self.sample_progress.setValue(self.total_samples)
            self.status_label.setText("Frame completed")

    def set_total_frames(self, start_frame, end_frame):
        """Sets the total number of frames to render"""
        if end_frame >= start_frame:
            self.start_frame = start_frame
            self.end_frame = end_frame
            self.total_frames = end_frame - start_frame + 1
            self.progress_bar.setRange(0, 100)
            # Initialize with start frame
            self.frame_label.setText(f"Frame: {start_frame}/{end_frame}")
            self.progress_bar.setValue(0)