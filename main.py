import logging

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from drive_connector import DriveConnector
from memory_manager import MemoryManager


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Aurora RC7 – AOVB Connect (Drive Integrated)")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

memory_manager = MemoryManager()
drive_connector = DriveConnector()


@app.get("/")
async def root():
    """Retorna o status básico da API e o estado de conexão com o Drive."""
    logger.info("Status check requested: drive_connected=%s", drive_connector.is_connected())
    return {"status": "✅ Aurora RC7 Online", "drive_connected": drive_connector.is_connected()}


@app.get("/panel", response_class=HTMLResponse)
async def panel(request: Request):
    """Exibe o painel web com as memórias armazenadas."""
    memories = memory_manager.load_memories()
    logger.info("Rendering panel with %d memories", len(memories))
    return templates.TemplateResponse("panel.html", {"request": request, "memories": memories})


@app.post("/memory/store")
async def store_memory(entry: str = Form(...)):
    """Salva uma nova memória e sincroniza com o Drive."""
    memory_manager.save_memory(entry)
    logger.info("New memory stored: %s", entry)
    drive_connector.sync_memory(memory_manager.memory_file)
    return {"message": "Memória salva com sucesso."}


@app.get("/memory/retrieve")
async def retrieve_memory():
    """Retorna todas as memórias disponíveis."""
    memories = memory_manager.load_memories()
    logger.info("Retrieved %d memories", len(memories))
    return {"memories": memories}


@app.get("/drive/sync")
async def sync_drive():
    """Força a sincronização manual do arquivo de memória com o Drive."""
    drive_connector.sync_memory(memory_manager.memory_file)
    logger.info("Manual Drive sync triggered")
    return {"message": "Sincronização com o Google Drive concluída."}
