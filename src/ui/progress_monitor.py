from PyQt5.QtWidgets import QWidget, QVBoxLayout, QProgressBar, QLabel, QGroupBox, QHBoxLayout, QGridLayout
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
    # Signals to update the UI from the rendering thread
    frame_updated = pyqtSignal(int, int)  # current frame, total frame
    render_time_updated = pyqtSignal(str)  # rendering time
    remaining_time_updated = pyqtSignal(str)  # estimated remaining time
    render_completed = pyqtSignal()  # rendering completed

    def __init__(self):
        super().__init__("Rendering Progress")
        self.settings_manager = SettingsManager()
        self.current_frame = 0
        self.total_frames = 0
        self.current_sample = 0
        self.total_samples = 0
        self.in_compositing = False
        self.compositing_operation = ""
        self.current_memory = ""
        self.peak_memory = ""
        self.using_cycles = False  # Flag to indicate if we are using Cycles
        
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
        
        # Top Info Container with Grid Layout to align information
        top_info_container = QWidget()
        top_info_layout = QGridLayout(top_info_container)
        top_info_layout.setContentsMargins(0, 0, 0, 0)
        top_info_layout.setSpacing(20)
        
        # Frame Counter
        self.frame_label = QLabel("Frame: 0/0")
        self.frame_label.setStyleSheet("""
            QLabel {
                color: #eb5e28;
                font-size: 11pt;
                font-weight: bold;
            }
        """)
        top_info_layout.addWidget(self.frame_label, 0, 0)
        
        # Memory Usage
        self.memory_label = QLabel("Memory: 0MB (Peak: 0MB)")
        self.memory_label.setStyleSheet("""
            QLabel {
                color: #e0e0e0;
                font-size: 10pt;
            }
        """)
        top_info_layout.addWidget(self.memory_label, 0, 1)
        
        # Time Info
        self.time_label = QLabel("Time: 00:00:00")
        self.time_label.setStyleSheet("""
            QLabel {
                color: #e0e0e0;
                font-size: 10pt;
            }
        """)
        top_info_layout.addWidget(self.time_label, 0, 2)
        
        # Status and Scene Info
        self.status_container = QWidget()
        status_layout = QHBoxLayout(self.status_container)
        status_layout.setContentsMargins(0, 0, 0, 0)
        status_layout.setSpacing(10)
        
        self.status_label = QLabel("Waiting...")
        self.status_label.setStyleSheet("""
            QLabel {
                color: #eb5e28;
                font-size: 10pt;
            }
        """)
        status_layout.addWidget(self.status_label)
        
        self.scene_label = QLabel("")
        self.scene_label.setStyleSheet("""
            QLabel {
                color: #e0e0e0;
                font-size: 10pt;
            }
        """)
        status_layout.addWidget(self.scene_label)
        status_layout.addStretch()
        
        layout.addWidget(top_info_container)
        layout.addWidget(self.status_container)
        
        # Main Progress Bar for total progress
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
                    stop:1 #eb5e28
                );
                border-radius: 4px;
            }
        """)
        layout.addWidget(self.progress_bar)
        
        # Sample Progress Bar - initially hidden
        self.sample_progress = QProgressBar()
        self.sample_progress.setTextVisible(True)
        self.sample_progress.setFormat("Sample %v/%m")
        self.sample_progress.setVisible(False)  # Hidden by default
        self.sample_progress.setStyleSheet("""
            QProgressBar {
                border: 2px solid #3d3d3d;
                border-radius: 6px;
                background-color: #2d2d2d;
                height: 8px;
                text-align: center;
                color: #e0e0e0;
                font-size: 9pt;
            }
            
            QProgressBar::chunk {
                background-color: #eb5e28;
                border-radius: 3px;
            }
        """)
        layout.addWidget(self.sample_progress)
        
        self.setLayout(layout)
        self.reset()
    
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
    
    def reset(self):
        """Resets the progress monitor for a new render"""
        self.progress_bar.setValue(0)
        self.sample_progress.setValue(0)
        self.sample_progress.setVisible(False)
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
    
    def parse_blender_output(self, line):
        """Parses a line of Blender output to extract progress information"""
        # Extracts the current frame
        frame_match = re.search(r'Fra:(\d+)', line)
        if frame_match:
            self.current_frame = int(frame_match.group(1))
            if self.total_frames > 0:
                self.frame_label.setText(f"Frame: {self.current_frame}/{self.total_frames}")
                progress = int((self.current_frame / self.total_frames) * 100)
                self.progress_bar.setValue(progress)
        
        # Extracts memory information
        mem_match = re.search(r'Mem:([\d.]+)([MG]).*Peak\s+([\d.]+)([MG])', line)
        if mem_match:
            current = float(mem_match.group(1))
            current_unit = mem_match.group(2)
            peak = float(mem_match.group(3))
            peak_unit = mem_match.group(4)
            
            # Convert to MB if necessary
            if current_unit == 'G':
                current *= 1024
            if peak_unit == 'G':
                peak *= 1024
            
            self.memory_label.setText(f"Memory: {current:.2f}MB (Peak: {peak:.2f}MB)")
        
        # Extracts rendering time
        time_match = re.search(r'Time:([\d:.]+)', line)
        if time_match:
            render_time = time_match.group(1)
            self.time_label.setText(f"Time: {render_time}")
        
        # Handles compositing
        if "Compositing" in line:
            self.in_compositing = True
            self.status_label.setText("Compositing")
            
            # Resets sample progress when compositing starts
            if self.using_cycles:
                self.sample_progress.setValue(0)
            
            # Extracts compositing operation
            comp_match = re.search(r'Compositing \| (.*?)(?=\||$)', line)
            if comp_match:
                comp_status = comp_match.group(1).strip()
                if self.using_cycles:
                    self.sample_progress.setFormat(f"Compositing: {comp_status}")
                self.status_label.setText(f"Compositing: {comp_status}")
            elif "Initializing" in line:
                if self.using_cycles:
                    self.sample_progress.setFormat("Initializing compositing...")
                self.status_label.setText("Initializing compositing...")
        
        # Handles samples in rendering (only for Cycles)
        elif "Sample" in line and not self.in_compositing:
            sample_match = re.search(r'Sample (\d+)/(\d+)', line)
            if sample_match:
                self.using_cycles = True
                self.sample_progress.setVisible(True)
                self.current_sample = int(sample_match.group(1))
                self.total_samples = int(sample_match.group(2))
                self.sample_progress.setMaximum(self.total_samples)
                self.sample_progress.setValue(self.current_sample)
                self.sample_progress.setFormat(f"Sample %v/%m")
                self.status_label.setText(f"Rendering sample {self.current_sample}/{self.total_samples}")
        
        # Extracts scene and viewlayer name
        scene_match = re.search(r'\| ([^|]+), ([^|]+) \|', line)
        if scene_match:
            scene = scene_match.group(1).strip()
            viewlayer = scene_match.group(2).strip()
            self.scene_label.setText(f"{scene} - {viewlayer}")
        
        # Detects frame or compositing completion
        if "Finished" in line:
            self.in_compositing = False  # Reset compositing state
            if self.using_cycles:
                self.sample_progress.setValue(self.total_samples)
            self.status_label.setText("Frame completed")
    
    def set_total_frames(self, start_frame, end_frame):
        """Sets the total number of frames to render"""
        if end_frame >= start_frame:
            self.total_frames = end_frame - start_frame + 1
            self.frame_label.setText(f"Frame: 0/{self.total_frames}")
            self.progress_bar.setRange(0, 100)  # Total percentage