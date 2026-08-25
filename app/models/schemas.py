from pydantic import BaseModel, Field


class GenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=1, example="Explain FastAPI in one sentence.")
    model: str | None = Field(
        default=None,
        description="Ollama model name. Defaults to OLLAMA_DEFAULT_MODEL if not given.",
    )
    stream: bool = Field(default=False, description="Whether to stream the response.")


class GenerateResponse(BaseModel):
    model: str
    response: str
    done: bool


class ChatMessage(BaseModel):
    role: str = Field(..., description="'system' | 'user' | 'assistant'")
    content: str


class ChatRequest(BaseModel):
    messages: list[ChatMessage]
    model: str | None = None
    stream: bool = False


class ChatResponse(BaseModel):
    model: str
    message: ChatMessage
    done: bool


class ModelInfo(BaseModel):
    name: str
    size: int | None = None
    modified_at: str | None = None
