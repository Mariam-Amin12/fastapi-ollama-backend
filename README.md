# FastAPI + Ollama Backend

A FastAPI backend template that serves a **free, locally-run LLM** through
[Ollama](https://ollama.com) instead of a traditional ML model. This is the
same pattern many teams use: FastAPI handles routing/validation, and a
service layer talks to the model runtime (here, Ollama; swap it for
scikit-learn/PyTorch/TensorFlow later if you want).

## Project structure

```
fastapi-ollama-backend/
├── app/
│   ├── main.py                # FastAPI app + router registration
│   ├── core/
│   │   └── config.py          # Settings (reads .env)
│   ├── api/routes/
│   │   └── chat.py            # /generate, /chat, /models, /health endpoints
│   ├── services/
│   │   └── ollama_service.py  # HTTP client wrapping the Ollama API
│   └── models/
│       └── schemas.py         # Pydantic request/response models
├── requirements.txt
├── .env.example
└── README.md
```



1. **Install Ollama** (free): https://ollama.com/download
2. **Pull a model**:
   ```bash
   ollama pull llama3.2
   ```
   (Other good free options: `phi3`, `mistral`, `qwen2.5`, `gemma2` — pick
   one that fits your RAM.)
3. **Start Ollama** (it usually runs automatically after install, otherwise):
   ```bash
   ollama serve
   ```
4. **Set up the Python backend**:
   ```bash
   cd fastapi-ollama-backend
   python -m venv venv
   source venv/bin/activate        # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env
   ```
5. **Run the API**:
   ```bash
   uvicorn app.main:app --reload
   ```
6. Open http://localhost:8000/docs for interactive Swagger docs.
  You can also open http://localhost:8000/ for the small Ollama playground UI.

## Endpoints

| Method | Path              | Description                          |
|--------|-------------------|---------------------------------------|
| GET    | `/api/v1/health`  | Checks API + Ollama connectivity      |
| GET    | `/api/v1/models`  | Lists models pulled into Ollama       |
| POST   | `/api/v1/generate`| Single-turn prompt → completion       |
| POST   | `/api/v1/chat`    | Multi-turn chat (message history)     |

