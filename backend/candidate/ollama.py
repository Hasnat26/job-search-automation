import json
import os
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

DEFAULT_BASE_URL = "http://127.0.0.1:11434"
DEFAULT_MODEL = "qwen3:4b"

class OllamaError(RuntimeError):
    pass

class OllamaProvider:
    def __init__(self, base_url: str | None = None, model: str | None = None, timeout: int = 300):
        self.base_url = (base_url or os.getenv("OLLAMA_BASE_URL", DEFAULT_BASE_URL)).rstrip("/")
        self.model = model or os.getenv("OLLAMA_MODEL", DEFAULT_MODEL)
        self.timeout = timeout

    def generate_json(self, prompt: str) -> str:
        payload = json.dumps({
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "format": "json",
            "think": False,
            "options": {"temperature": 0},
            "keep_alive": "5m",
        }).encode()
        request = Request(f"{self.base_url}/api/generate", data=payload, headers={"Content-Type": "application/json"}, method="POST")
        try:
            with urlopen(request, timeout=self.timeout) as response:
                data = json.loads(response.read().decode("utf-8"))
        except (HTTPError, URLError, TimeoutError, OSError) as exc:
            raise OllamaError(f"Ollama request failed: {exc}") from exc
        text = data.get("response")
        if not isinstance(text, str) or not text.strip():
            raise OllamaError("Ollama returned no response text")
        return text
