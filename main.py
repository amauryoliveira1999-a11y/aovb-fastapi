from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from drive_connector import DriveConnector
from memory_manager import MemoryManager

app = FastAPI(title="Aurora RC7 – AOVB Connect (Drive Integrated)")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

memory_manager = MemoryManager()
drive_connector = DriveConnector()

@app.get("/")
async def root():
    return {"status": "✅ Aurora RC7 Online", "drive_connected": drive_connector.is_connected()}

@app.get("/panel", response_class=HTMLResponse)
async def panel(request: Request):
    memories = memory_manager.load_memories()
    return templates.TemplateResponse("panel.html", {"request": request, "memories": memories})

@app.post("/memory/store")
async def store_memory(entry: str = Form(...)):
    memory_manager.save_memory(entry)
    drive_connector.sync_memory(memory_manager.memory_file)
    return {"message": "Memória salva com sucesso."}

@app.get("/memory/retrieve")
async def retrieve_memory():
    return {"memories": memory_manager.load_memories()}

@app.get("/drive/sync")
async def sync_drive():
    result = drive_connector.sync_memory(memory_manager.memory_file)
    return {
        "message": "Sincronização completa com o Google Drive.",
        **result,
    }
