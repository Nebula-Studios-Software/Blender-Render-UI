import sys
import os
import logging
import traceback
from PyQt5.QtWidgets import QApplication, QMessageBox
from src.ui.main_window import MainWindow

# Configure logging
def setup_logging():
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'logs')
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, 'app.log')
    
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger('BlenderRenderUI')

def excepthook(exc_type, exc_value, exc_tb):
    """Handle uncaught exceptions"""
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    logger.error(f"Uncaught exception:\n{tb}")
    
    error_msg = f"{exc_type.__name__}: {exc_value}"
    QMessageBox.critical(None, "Error", 
                        f"An unexpected error occurred:\n\n{error_msg}\n\n"
                        f"Check the log file for details:\n{os.path.abspath('logs/app.log')}")

if __name__ == "__main__":
    # Setup logging
    logger = setup_logging()
    logger.info("Application starting...")
    
    # Install exception hook
    sys.excepthook = excepthook
    
    try:
        app = QApplication(sys.argv)
        
        # Get absolute path of style file
        style_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__), 
            "ui", 
            "styles.py"
        ))
    
        # Load initial styles
        logger.debug("Loading initial styles")
        from src.ui.styles import STYLE
        app.setStyleSheet(STYLE)
        
        # Start the application
        logger.debug("Creating main window")
        window = MainWindow()
        window.show()
        
        logger.info("Application started successfully")
        
        try:
            sys.exit(app.exec_())
        finally:
            # Stop the observer when app closes
            logger.info("Application closed normally")
            
    except Exception as e:
        logger.error(f"Failed to start application: {e}", exc_info=True)
        QMessageBox.critical(None, "Error", 
                           f"Failed to start application:\n\n{str(e)}\n\n"
                           f"Check the log file for details:\n{os.path.abspath('logs/app.log')}")
        sys.exit(1)