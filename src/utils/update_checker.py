import requests
import re
import logging
from typing import Optional, Tuple
from ..core.version import get_version

class UpdateChecker:
    GITHUB_API_URL = "https://api.github.com/repos/Nebula-Studios-Software/Blender-Render-UI/releases/latest"
    
    @staticmethod
    def parse_version(version_str: str) -> tuple:
        """Converte una stringa di versione in una tupla di numeri."""
        match = re.search(r'(\d+)\.(\d+)\.(\d+)', version_str)
        if match:
            return tuple(map(int, match.groups()))
        return (0, 0, 0)
    
    @classmethod
    def check_for_updates(cls) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Controlla se sono disponibili aggiornamenti.
        
        Returns:
            Tuple[bool, Optional[str], Optional[str]]: 
            - bool: True se è disponibile un aggiornamento
            - str: Versione più recente (o None se errore)
            - str: URL di download (o None se errore)
        """
        try:
            response = requests.get(cls.GITHUB_API_URL, timeout=5)
            response.raise_for_status()
            
            release_data = response.json()
            latest_version = release_data['tag_name'].lstrip('v')
            download_url = release_data['html_url']
            
            current_version_tuple = cls.parse_version(get_version())
            latest_version_tuple = cls.parse_version(latest_version)
            
            update_available = latest_version_tuple > current_version_tuple
            
            return update_available, latest_version, download_url
            
        except requests.RequestException as e:
            logging.error(f"Errore nel controllo degli aggiornamenti: {e}")
            return False, None, None
        except (KeyError, ValueError) as e:
            logging.error(f"Errore nel parsing della risposta GitHub: {e}")
            return False, None, None