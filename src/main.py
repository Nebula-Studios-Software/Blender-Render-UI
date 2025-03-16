import sys
import os
from PyQt5.QtWidgets import QApplication
from src.ui.main_window import MainWindow
from src.ui.hot_reload import setup_hot_reload

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Path assoluto del file di stile
    style_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__), 
        "ui", 
        "styles.py"
    ))
    
    # Configura l'hot reload
    observer = setup_hot_reload(app, style_path)
    
    # Carica gli stili iniziali
    from src.ui.styles import STYLE
    app.setStyleSheet(STYLE)
    
    # Avvia l'applicazione
    window = MainWindow()
    window.show()
    
    try:
        sys.exit(app.exec_())
    finally:
        # Ferma l'observer quando l'app viene chiusa
        observer.stop()
        observer.join()