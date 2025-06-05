import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logging(log_file="application.log", log_level=logging.INFO):
    """
    Konfiguriert das Logging-Framework, um Logs in eine Datei zu schreiben.
    
    Args:
        log_file: Der Pfad zur Log-Datei
        log_level: Das Log-Level (Standard: INFO)
    """
    # Stelle sicher, dass das Verzeichnis existiert
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Konfiguriere den Root-Logger
    logger = logging.getLogger()
    logger.setLevel(log_level)
    
    # Entferne bestehende Handler, um Duplikate zu vermeiden
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Erstelle einen Datei-Handler mit Rotation (max. 5 MB pro Datei, max. 5 Dateien)
    file_handler = RotatingFileHandler(
        log_file, 
        maxBytes=5*1024*1024,  # 5 MB
        backupCount=5
    )
    
    # Definiere das Format der Log-Nachrichten
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    
    # Füge den Handler zum Logger hinzu
    logger.addHandler(file_handler)
    
    # Optional: Füge einen Stream-Handler hinzu, um Logs auch in der Konsole anzuzeigen
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)  # Nur Warnungen und Fehler in der Konsole
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    logging.info("Logging wurde initialisiert")
