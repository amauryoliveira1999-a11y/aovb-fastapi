import os
from memory_manager import DriveSyncManager


class DriveConnector:
    """
    Adaptador simples para o DriveSyncManager.

    - self.connected: flag lógica (pode virar health check depois)
    - sync_memory(file_path): pega o arquivo local (ex: memory.json)
      e manda para o Google Drive usando o DriveSyncManager.
    """

    def __init__(self):
        self.connected = True
        # Usa o DriveSyncManager que você definiu em memory_manager.py
        self.sync_manager = DriveSyncManager()

    def is_connected(self):
        return self.connected

    def sync_memory(self, file_path: str):
        """
        file_path: caminho do arquivo local de memória (ex: 'memory.json')
        Retorna o dicionário resultante do DriveSyncManager.
        """
        if not self.connected:
            raise RuntimeError("Google Drive não está conectado.")

        # Aqui a mágica real acontece: subida/atualização no Drive
        return self.sync_manager.sync_memory_file(local_path=file_path)
