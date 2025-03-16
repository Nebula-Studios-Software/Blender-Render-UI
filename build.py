import PyInstaller.__main__
import os
import shutil

def build_exe():
    """Build the executable for Windows"""
    # Percorsi assoluti
    root_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(root_dir, 'src', 'resources', 'icons', 'app_icon.ico')
    main_script = os.path.join(root_dir, 'src', 'main.py')
    
    # Crea directory per i log se non esiste
    log_dir = os.path.join(root_dir, 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    PyInstaller.__main__.run([
        main_script,
        '--name=BlenderRenderUI',
        '--onefile',
        f'--icon={icon_path}',
        '--clean',
        '--noconsole',
        '--add-data', f'{os.path.join(root_dir, "src/resources")}{";" if os.name == "nt" else ":"}resources',
        '--hidden-import=PyQt5.QtCore',
        '--hidden-import=PyQt5.QtGui',
        '--hidden-import=PyQt5.QtWidgets',
        '--hidden-import=regex',
        '--hidden-import=watchdog',
        '--version-file', os.path.join(root_dir, 'version.txt'),  # Info versione per Windows
    ])

if __name__ == '__main__':
    build_exe()