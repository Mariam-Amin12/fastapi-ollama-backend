import httpx
from fastapi import HTTPException

from app.core.config import get_settings
from app.models.schemas import ChatMessage


class OllamaService:

    def __init__(self, base_url: str | None = None ):
        # hst5dem local 
        self.base_url = (base_url or get_settings().OLLAMA_BASE_URL).rstrip("/")
        # al max time to say ano mafesh response 
        self.timeout = get_settings().OLLAMA_TIMEOUT

    async def _client(self) -> httpx.AsyncClient:  #hena ana b3mel al clint  mesh bastana ollama t2om f bsthkdem async
        return httpx.AsyncClient(base_url=self.base_url, timeout=self.timeout)

    async def health_check(self) -> bool:
        try:
            async with await self._client() as client: #bastana ollama t2om
                r = await client.get("/api/tags")  # bshof hal rag3ly response 
                return r.status_code == 200
        except httpx.RequestError:
            return False

    async def list_models(self) -> list[dict]:
        async with await self._client() as client:
            try:
                r = await client.get("/api/tags")
                r.raise_for_status() # bshof 2ader yosal lel service deh wala la2 
            except httpx.RequestError as exc: # b throw exception lw ma2drtsh yosal lel service deh
                raise HTTPException(
                    status_code=503,
                    detail=f"Could not reach Ollama at {self.base_url}. Is it running? ({exc})",
                ) from exc
            return r.json().get("models", []) #return available models 

    async def generate(self, prompt: str, model: str | None = None) -> dict:
        payload = {
            "model": model or get_settings().OLLAMA_DEFAULT_MODEL,
            "prompt": prompt,
            "stream": False,
        }
        async with await self._client() as client:
            try:
                r = await client.post("/api/generate", json=payload)
                r.raise_for_status()
            except httpx.HTTPStatusError as exc:
                raise HTTPException(
                    status_code=exc.response.status_code,
                    detail=f"Ollama error: {exc.response.text}",
                ) from exc
            except httpx.RequestError as exc:
                raise HTTPException(
                    status_code=503,
                    detail=f"Could not reach Ollama at {self.base_url}. Is it running? ({exc})",
                ) from exc

            print ("generate response:", r.json())
            return r.json()

    async def chat(self, messages: list[ChatMessage], model: str | None = None) -> dict:
        payload = {
            "model": model or get_settings().OLLAMA_DEFAULT_MODEL,
            "messages": [m.model_dump() for m in messages],
            "stream": True,
        }
        async with await self._client() as client:
            try:
                r = await client.post("/api/chat", json=payload)
                r.raise_for_status()
            except httpx.HTTPStatusError as exc:
                raise HTTPException(
                    status_code=exc.response.status_code,
                    detail=f"Ollama error: {exc.response.text}",
                ) from exc
            except httpx.RequestError as exc:
                raise HTTPException(
                    status_code=503,
                    detail=f"Could not reach Ollama at {self.base_url}. Is it running? ({exc})",
                ) from exc
            return r.json()


ollama_service = OllamaService()
