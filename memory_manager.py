import json, os
from typing import Optional
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io

class MemoryManager:
    def __init__(self, file_path='memory.json'):
        self.memory_file = file_path
        if not os.path.exists(self.memory_file):
            with open(self.memory_file, 'w') as f:
                json.dump([], f)

    def load_memories(self):
        with open(self.memory_file, 'r') as f:
            return json.load(f)

    def save_memory(self, entry):
        memories = self.load_memories()
        memories.append({"entry": entry})
        with open(self.memory_file, 'w') as f:
            json.dump(memories, f, indent=2)
class DriveSyncManager:
    """
    Modelo A:
    - Fonte principal: arquivo local memory.json
    - Drive: espelho/backup
    """

    def __init__(
        self,
        drive_filename: str = "Aurora_RC7_memory.json",
        folder_id: Optional[str] = None,
    ):
        self.drive_filename = drive_filename
        self.folder_id = folder_id or os.getenv("GOOGLE_DRIVE_FOLDER_ID")
        self.service = self._build_service()

    def _build_service(self):
        """
        Cria o cliente da API do Drive usando
        o JSON da service account na variável de ambiente
        GOOGLE_SERVICE_ACCOUNT_JSON.
        """
        creds_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
        if not creds_json:
            raise RuntimeError(
                "Variável de ambiente GOOGLE_SERVICE_ACCOUNT_JSON não configurada."
            )

        info = json.loads(creds_json)
        creds = service_account.Credentials.from_service_account_info(
            info,
            scopes=["https://www.googleapis.com/auth/drive.file"],
        )
        return build("drive", "v3", credentials=creds)

    def _find_existing_file(self) -> Optional[str]:
        """
        Procura se já existe um arquivo com esse nome (e pasta) no Drive.
        Retorna o fileId se encontrar, senão None.
        """
        q_parts = [f"name = '{self.drive_filename}'", "trashed = false"]
        if self.folder_id:
            q_parts.append(f"'{self.folder_id}' in parents")
        query = " and ".join(q_parts)

        results = (
            self.service.files()
            .list(q=query, fields="files(id, name)", pageSize=1)
            .execute()
        )
        files = results.get("files", [])
        return files[0]["id"] if files else None

    def sync_memory_file(self, local_path: str = "memory.json") -> dict:
        """
        Lê o arquivo local (memory.json) e faz upload/atualização
        no Drive.
        """
        if not os.path.exists(local_path):
            return {"synced": False, "reason": "local_file_not_found"}

        with open(local_path, "rb") as f:
            data = f.read()

        media = MediaIoBaseUpload(
            io.BytesIO(data),
            mimetype="application/json",
            resumable=False,
        )

        file_metadata = {"name": self.drive_filename}
        if self.folder_id:
            file_metadata["parents"] = [self.folder_id]

        existing_id = self._find_existing_file()

        if existing_id:
            file = (
                self.service.files()
                .update(
                    fileId=existing_id,
                    media_body=media,
                )
                .execute()
            )
            action = "updated"
        else:
            file = (
                self.service.files()
                .create(
                    body=file_metadata,
                    media_body=media,
                    fields="id, name",
                )
                .execute()
            )
            action = "created"

        return {
            "synced": True,
            "action": action,
            "fileId": file.get("id"),
            "fileName": file.get("name"),
        }
