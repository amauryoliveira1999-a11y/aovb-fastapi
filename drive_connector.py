import os

class DriveConnector:
    def __init__(self):
        self.connected = True  # Simulação de conexão (modo de teste)

    def is_connected(self):
        return self.connected

    def sync_memory(self, file_path):
        print(f"🔄 Simulando upload do arquivo {file_path} para o Google Drive...")
        return True
