from fastapi import APIRouter

from app.models.schemas import (
    ChatMessage,
    ChatRequest,
    ChatResponse,
    GenerateRequest,
    GenerateResponse,
    ModelInfo,
)
from app.services.ollama_service import ollama_service

router = APIRouter(prefix="/api/v1", tags=["LLM"])


@router.get("/health")
async def health():
    ollama_up = await ollama_service.health_check()
    return {"status": "ok", "ollama_connected": ollama_up}


@router.get("/models", response_model=list[ModelInfo])
async def list_models():
    
    models = await ollama_service.list_models()
    return [
        ModelInfo(
            name=m.get("name", "unknown"),
            size=m.get("size"),
            modified_at=m.get("modified_at"),
        )
        for m in models
    ]


@router.post("/generate", response_model=GenerateResponse)
async def generate(payload: GenerateRequest):
    """Single-turn text"""

    result = await ollama_service.generate(prompt=payload.prompt, model=payload.model)
    return GenerateResponse(
        model=result.get("model", payload.model or ""),
        response=result.get("response", ""),
        done=result.get("done", True),
    )


@router.post("/chat", response_model=ChatResponse)
async def chat(payload: ChatRequest):
    """Multi-turn chat"""

    result = await ollama_service.chat(messages=payload.messages, model=payload.model)
    message = result.get("message", {"role": "assistant", "content": ""})
    return ChatResponse(
        model=result.get("model", payload.model or ""),
        message=ChatMessage(role=message.get("role", "assistant"), content=message.get("content", "")),
        done=result.get("done", True),
    )
