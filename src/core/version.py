"""Gestione centralizzata della versione dell'applicazione"""

VERSION = "0.2.1"  # Versione corrente dell'applicazione
VERSION_TAG = f"v{VERSION}"  # Il formato usato per i tag su GitHub

def get_version():
    """Restituisce la versione corrente dell'applicazione"""
    return VERSION

def get_version_tag():
    """Restituisce il tag della versione nel formato utilizzato su GitHub"""
    return VERSION_TAG