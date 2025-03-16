import json
import os
import logging
from pathlib import Path

class SettingsManager:
    """Manages application settings saving and loading"""
    
    def __init__(self):
        # Determine settings directory path
        if os.name == 'nt':  # Windows
            self.settings_dir = os.path.join(os.getenv('APPDATA'), 'BlenderRenderUI')
        else:  # Linux/Mac
            self.settings_dir = os.path.join(os.path.expanduser('~'), '.config', 'blender-render-ui')
        
        # Create directory if it doesn't exist
        os.makedirs(self.settings_dir, exist_ok=True)
        
        self.settings_file = os.path.join(self.settings_dir, 'settings.json')
        self.settings = self.load_settings()

        # Add presets file
        self.presets_file = os.path.join(self.settings_dir, 'presets.json')
        self.presets = self.load_presets()
    
    def load_settings(self):
        """Load settings from JSON file"""
        default_settings = {
            'blender_path': '',
            'parameters': {},
            'ui_state': {
                'log_filters': {
                    'show_info': True,
                    'show_warning': True,
                    'show_error': True,
                    'detail_level': 1  # 0=Detailed, 1=Standard, 2=Minimal
                }
            }
        }
        
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    # Update default settings with saved ones
                    default_settings.update(settings)
        except Exception as e:
            logging.error(f"Error loading settings: {e}")
        
        return default_settings
    
    def save_settings(self):
        """Save settings to JSON file"""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=4, ensure_ascii=False)
        except Exception as e:
            logging.error(f"Error saving settings: {e}")
    
    def get_setting(self, key, default=None):
        """Get a value from settings"""
        return self.settings.get(key, default)
    
    def set_setting(self, key, value):
        """Set a value in settings"""
        self.settings[key] = value
    
    def get_blender_path(self):
        """Get saved Blender path"""
        return self.settings.get('blender_path', '')
    
    def set_blender_path(self, path):
        """Set Blender path"""
        self.settings['blender_path'] = path
        self.save_settings()
    
    def get_parameters(self):
        """Get saved parameters"""
        return self.settings.get('parameters', {})
    
    def set_parameters(self, parameters):
        """Set parameters"""
        self.settings['parameters'] = parameters
        self.save_settings()
    
    def get_ui_state(self):
        """Get UI state"""
        return self.settings.get('ui_state', {})
    
    def set_ui_state(self, ui_state):
        """Set UI state"""
        self.settings['ui_state'] = ui_state
        self.save_settings()

    def load_presets(self):
        """Load presets from JSON file"""
        default_presets = {
            'default': {
                'name': 'Default',
                'parameters': {},
                'blender_path': ''
            }
        }
        
        try:
            if os.path.exists(self.presets_file):
                with open(self.presets_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logging.error(f"Error loading presets: {e}")
        
        return default_presets
    
    def save_presets(self):
        """Save presets to JSON file"""
        try:
            with open(self.presets_file, 'w', encoding='utf-8') as f:
                json.dump(self.presets, f, indent=4, ensure_ascii=False)
        except Exception as e:
            logging.error(f"Error saving presets: {e}")
    
    def get_preset_names(self):
        """Return list of available preset names"""
        return list(self.presets.keys())
    
    def get_preset(self, name):
        """Get a specific preset"""
        return self.presets.get(name, None)
    
    def save_as_preset(self, name, settings):
        """Save current settings as a new preset"""
        self.presets[name] = settings
        self.save_presets()
    
    def delete_preset(self, name):
        """Delete a preset"""
        if name in self.presets and name != 'default':
            del self.presets[name]
            self.save_presets()
            return True
        return False
    
    def rename_preset(self, old_name, new_name):
        """Rename a preset"""
        if old_name in self.presets and old_name != 'default':
            self.presets[new_name] = self.presets.pop(old_name)
            self.save_presets()
            return True
        return False

    def get_all_settings(self):
        """Get all current settings in a savable format"""
        return {
            'blender_path': self.get_blender_path(),
            'parameters': self.get_parameters(),
            'ui_state': self.get_ui_state()
        }

    def apply_settings(self, settings):
        """Apply a complete set of settings"""
        if 'blender_path' in settings:
            self.set_blender_path(settings['blender_path'])
        if 'parameters' in settings:
            self.set_parameters(settings['parameters'])
        if 'ui_state' in settings:
            self.set_ui_state(settings['ui_state'])