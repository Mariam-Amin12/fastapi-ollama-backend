from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
# from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.chat import router as chat_router
from app.core.config import get_settings    

app = FastAPI(
    title=get_settings().APP_NAME,
    version=get_settings().APP_VERSION,
    description="FastAPI backend that talks to a local/free LLM served by Ollama.",
)


app.include_router(chat_router)

UI_FILE = Path(__file__).parent / "static" / "index.html"

@app.get("/")
async def root():
    return FileResponse(UI_FILE)
