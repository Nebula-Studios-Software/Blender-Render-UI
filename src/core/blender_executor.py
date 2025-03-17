import subprocess
import threading
import os
from PyQt5.QtCore import QObject, pyqtSignal
import sys
import io

class BlenderExecutor(QObject):
    """
    Class for executing Blender commands and monitoring output in real time.
    Uses Qt signals to communicate with the user interface.
    """
    
    # Signals to communicate with the user interface
    output_received = pyqtSignal(str)  # Emitted when new output line is received
    render_started = pyqtSignal()  # Emitted when rendering starts
    render_completed = pyqtSignal(bool, str)  # Emitted when completed (success, message)
    render_progress = pyqtSignal(float)  # Emitted for progress updates (0.0-1.0)

    def __init__(self):
        super().__init__()
        self.process = None
        self.is_running = False
        self.start_frame = 1
        self.end_frame = 1
        self.verbose = True  # Controls whether to print output to console as well

    def execute(self, command, start_frame=1, end_frame=1, background_process=False):
        """
        Executes a Blender command with output monitoring
        
        Args:
            command: List of command arguments (for subprocess)
            start_frame: Starting frame of the rendering
            end_frame: Ending frame of the rendering
            background_process: If True, runs in background and does not wait for completion
        
        Returns:
            True if execution started successfully, False otherwise
        """
        if self.is_running:
            self.output_received.emit("ERROR: Another rendering process is already running")
            return False
        
        self.start_frame = start_frame
        self.end_frame = end_frame
        self.is_running = True
        
        # Start a thread for process execution
        threading.Thread(
            target=self._execute_process_thread,
            args=(command, background_process),
            daemon=True
        ).start()
        
        return True

    def _execute_process_thread(self, command, background_process):
        """Thread worker for executing the Blender process"""
        try:
            # Create the process with pipes for stdout and stderr
            self.output_received.emit(f"Starting command: {' '.join(command)}")
            self.render_started.emit()
            
            # Windows uses a different mechanism for inheriting file handles
            # and requires creationflags to not show the process window
            startupinfo = None
            creationflags = 0
            
            if sys.platform == "win32":
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                creationflags = subprocess.CREATE_NO_WINDOW
            
            # Explicitly set UTF-8 encoding for output
            self.process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=False,  # Disable universal_newlines
                bufsize=1,  # Line buffered
                startupinfo=startupinfo,
                creationflags=creationflags
            )
            
            # Use TextIOWrapper to handle UTF-8 encoding
            with io.TextIOWrapper(self.process.stdout, encoding='utf-8', errors='replace') as text_output:
                # Read output line by line in real time
                for line in text_output:
                    if line:
                        self._process_output_line(line.rstrip())
            
            # Wait for process completion
            return_code = self.process.wait()
            
            if return_code == 0:
                self.output_received.emit("Rendering completed successfully")
                self.render_completed.emit(True, "Rendering completed successfully")
            else:
                self.output_received.emit(f"Blender exited with error code {return_code}")
                self.render_completed.emit(False, f"Rendering error (code {return_code})")
        
        except Exception as e:
            self.output_received.emit(f"Error during process execution: {str(e)}")
            self.render_completed.emit(False, f"Error: {str(e)}")
        
        finally:
            self.is_running = False

    def _process_output_line(self, line):
        """Processes an output line from the Blender process"""
        if not line:
            return
        
        # Emit the output signal
        self.output_received.emit(line)
        
        # If verbose is enabled, also print to console
        if self.verbose:
            print(line)
        
        # Parse the line for progress information
        self._parse_progress_info(line)

    def _parse_progress_info(self, line):
        """
        Parses an output line to extract progress information
        Example: "Fra:10 Mem:8.40M (0.00M, Peak 8.40M) | Time:00:00.12 | Mem:0.00M, Peak:0.00M | Scene, RenderLayer | Path Tracing Tile 1/4"
        """
        import re
        
        # Look for the current frame number
        frame_match = re.search(r'Fra:(\d+)', line)
        if frame_match:
            current_frame = int(frame_match.group(1))
            total_frames = self.end_frame - self.start_frame + 1
            
            if total_frames > 0:
                # Calculate actual progress considering start frame
                current_progress = current_frame - self.start_frame + 1
                progress = current_progress / total_frames
                progress = max(0.0, min(1.0, progress))  # Clamp between 0 and 1
                self.render_progress.emit(progress)

    def terminate(self):
        """Terminates the Blender process if it is running"""
        if self.process and self.is_running:
            self.output_received.emit("Terminating rendering process...")
            
            try:
                # The most appropriate method depends on the operating system
                if hasattr(self.process, "kill"):
                    self.process.kill()
                else:
                    self.process.terminate()
                
                self.is_running = False
                self.output_received.emit("Process terminated")
                self.render_completed.emit(False, "Rendering interrupted by user")
                return True
            
            except Exception as e:
                self.output_received.emit(f"Error during termination: {str(e)}")
                return False
        
        return False

    def is_rendering(self):
        """Returns True if there is an active rendering process"""
        return self.is_running