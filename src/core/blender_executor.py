import subprocess
import threading
import os
from PyQt5.QtCore import QObject, pyqtSignal
import sys
import io

class BlenderExecutor(QObject):
    """
    Classe per l'esecuzione dei comandi Blender e il monitoraggio dell'output in tempo reale.
    Utilizza segnali Qt per comunicare con l'interfaccia utente.
    """
    
    # Segnali per comunicare con l'interfaccia utente
    output_received = pyqtSignal(str)  # Emesso quando si riceve una nuova linea di output
    render_started = pyqtSignal()  # Emesso all'avvio del rendering
    render_completed = pyqtSignal(bool, str)  # Emesso al completamento (successo, messaggio)
    render_progress = pyqtSignal(float)  # Emesso per aggiornamenti di progresso (0.0-1.0)

    def __init__(self):
        super().__init__()
        self.process = None
        self.is_running = False
        self.start_frame = 1
        self.end_frame = 1
        self.verbose = True  # Controlla se stampare l'output anche nella console

    def execute(self, command, start_frame=1, end_frame=1, background_process=False):
        """
        Esegue un comando Blender con monitoraggio dell'output
        
        Args:
            command: Lista di argomenti del comando (per subprocess)
            start_frame: Frame iniziale del rendering
            end_frame: Frame finale del rendering
            background_process: Se True, esegue in background e non attende il completamento
        
        Returns:
            True se l'esecuzione è avviata con successo, False altrimenti
        """
        if self.is_running:
            self.output_received.emit("ERRORE: Un altro processo di rendering è già in esecuzione")
            return False
        
        self.start_frame = start_frame
        self.end_frame = end_frame
        self.is_running = True
        
        # Avvia un thread per l'esecuzione del processo
        threading.Thread(
            target=self._execute_process_thread,
            args=(command, background_process),
            daemon=True
        ).start()
        
        return True

    def _execute_process_thread(self, command, background_process):
        """Thread worker per l'esecuzione del processo Blender"""
        try:
            # Crea il processo con pipe per stdout e stderr
            self.output_received.emit(f"Avvio comando: {' '.join(command)}")
            self.render_started.emit()
            
            # Windows utilizza un meccanismo diverso per ereditare i file handle
            # e richiede creationflags per non mostrare la finestra del processo
            startupinfo = None
            creationflags = 0
            
            if sys.platform == "win32":
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                creationflags = subprocess.CREATE_NO_WINDOW
            
            # Impostiamo esplicitamente la codifica UTF-8 per l'output
            self.process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=False,  # Disabilitiamo universal_newlines
                bufsize=1,  # Line buffered
                startupinfo=startupinfo,
                creationflags=creationflags
            )
            
            # Usiamo TextIOWrapper per gestire la codifica UTF-8
            with io.TextIOWrapper(self.process.stdout, encoding='utf-8', errors='replace') as text_output:
                # Legge l'output linea per linea in tempo reale
                for line in text_output:
                    if line:
                        self._process_output_line(line.rstrip())
            
            # Attende il completamento del processo
            return_code = self.process.wait()
            
            if return_code == 0:
                self.output_received.emit("Rendering completato con successo")
                self.render_completed.emit(True, "Rendering completato con successo")
            else:
                self.output_received.emit(f"Blender è terminato con codice di errore {return_code}")
                self.render_completed.emit(False, f"Errore nel rendering (codice {return_code})")
        
        except Exception as e:
            self.output_received.emit(f"Errore durante l'esecuzione del processo: {str(e)}")
            self.render_completed.emit(False, f"Errore: {str(e)}")
        
        finally:
            self.is_running = False

    def _process_output_line(self, line):
        """Elabora una linea di output dal processo Blender"""
        if not line:
            return
        
        # Emette il segnale di output
        self.output_received.emit(line)
        
        # Se verbose è attivo, stampa anche nella console
        if self.verbose:
            print(line)
        
        # Analizza la linea per informazioni di progresso
        self._parse_progress_info(line)

    def _parse_progress_info(self, line):
        """
        Analizza una linea di output per estrarre informazioni sul progresso
        Esempio: "Fra:10 Mem:8.40M (0.00M, Peak 8.40M) | Time:00:00.12 | Mem:0.00M, Peak:0.00M | Scene, RenderLayer | Path Tracing Tile 1/4"
        """
        import re
        
        # Cerca il numero del frame corrente
        frame_match = re.search(r'Fra:(\d+)', line)
        if frame_match:
            current_frame = int(frame_match.group(1))
            total_frames = self.end_frame - self.start_frame + 1
            
            if total_frames > 0:
                # Calcola e emetti il progresso
                progress = (current_frame - self.start_frame) / total_frames
                progress = max(0.0, min(1.0, progress))  # Limita tra 0 e 1
                self.render_progress.emit(progress)

    def terminate(self):
        """Termina il processo Blender se è in esecuzione"""
        if self.process and self.is_running:
            self.output_received.emit("Terminazione del processo di rendering...")
            
            try:
                # Il metodo più appropriato dipende dal sistema operativo
                if hasattr(self.process, "kill"):
                    self.process.kill()
                else:
                    self.process.terminate()
                
                self.is_running = False
                self.output_received.emit("Processo terminato")
                self.render_completed.emit(False, "Rendering interrotto dall'utente")
                return True
            
            except Exception as e:
                self.output_received.emit(f"Errore durante la terminazione: {str(e)}")
                return False
        
        return False

    def is_rendering(self):
        """Restituisce True se c'è un processo di rendering attivo"""
        return self.is_running