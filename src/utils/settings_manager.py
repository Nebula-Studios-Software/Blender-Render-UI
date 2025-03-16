import json
import os
import logging
from pathlib import Path

class SettingsManager:
    """Gestisce il salvataggio e il caricamento delle impostazioni dell'applicazione"""
    
    def __init__(self):
        # Determina il percorso della directory delle impostazioni
        if os.name == 'nt':  # Windows
            self.settings_dir = os.path.join(os.getenv('APPDATA'), 'BlenderRenderUI')
        else:  # Linux/Mac
            self.settings_dir = os.path.join(os.path.expanduser('~'), '.config', 'blender-render-ui')
        
        # Crea la directory se non esiste
        os.makedirs(self.settings_dir, exist_ok=True)
        
        self.settings_file = os.path.join(self.settings_dir, 'settings.json')
        self.settings = self.load_settings()
    
    def load_settings(self):
        """Carica le impostazioni dal file JSON"""
        default_settings = {
            'blender_path': '',
            'parameters': {},
            'ui_state': {
                'log_filters': {
                    'show_info': True,
                    'show_warning': True,
                    'show_error': True,
                    'detail_level': 1  # 0=Dettagliato, 1=Standard, 2=Minimo
                }
            }
        }
        
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    # Aggiorna le impostazioni di default con quelle salvate
                    default_settings.update(settings)
        except Exception as e:
            logging.error(f"Errore nel caricamento delle impostazioni: {e}")
        
        return default_settings
    
    def save_settings(self):
        """Salva le impostazioni nel file JSON"""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=4, ensure_ascii=False)
        except Exception as e:
            logging.error(f"Errore nel salvataggio delle impostazioni: {e}")
    
    def get_setting(self, key, default=None):
        """Ottiene un valore dalle impostazioni"""
        return self.settings.get(key, default)
    
    def set_setting(self, key, value):
        """Imposta un valore nelle impostazioni"""
        self.settings[key] = value
    
    def get_blender_path(self):
        """Ottiene il percorso di Blender salvato"""
        return self.settings.get('blender_path', '')
    
    def set_blender_path(self, path):
        """Imposta il percorso di Blender"""
        self.settings['blender_path'] = path
        self.save_settings()
    
    def get_parameters(self):
        """Ottiene i parametri salvati"""
        return self.settings.get('parameters', {})
    
    def set_parameters(self, parameters):
        """Imposta i parametri"""
        self.settings['parameters'] = parameters
        self.save_settings()
    
    def get_ui_state(self):
        """Ottiene lo stato dell'interfaccia utente"""
        return self.settings.get('ui_state', {})
    
    def set_ui_state(self, ui_state):
        """Imposta lo stato dell'interfaccia utente"""
        self.settings['ui_state'] = ui_state
        self.save_settings()