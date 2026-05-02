import os
from typing import List, Union, Generator, Iterator
from schemas import OpenAIChatMessage
from pydantic import BaseModel
import requests


class Pipeline:
    class Valves(BaseModel):
        OLLAMA_BASE_URL: str
        LMSTUDIO_BASE_URL: str

    def __init__(self):
        self.type = "manifold"
        self.name = ""

        self.valves = self.Valves(
            **{
                "OLLAMA_BASE_URL": os.getenv(
                    "OLLAMA_CPU_BASE_URL",
                    "http://ollama-cpu:11434",
                ),
                "LMSTUDIO_BASE_URL": os.getenv(
                    "LMSTUDIO_BASE_URL",
                    "",
                ),
            }
        )

        self.pipelines = []

    async def on_startup(self):
        print(f"on_startup:{__name__}")
        self.pipelines = self.get_all_models()

    async def on_shutdown(self):
        print(f"on_shutdown:{__name__}")

    async def on_valves_updated(self):
        print(f"on_valves_updated:{__name__}")
        self.pipelines = self.get_all_models()

    # -----------------------------
    # Model Discovery
    # -----------------------------
    def get_all_models(self):
        models = []
        models.extend(self.get_ollama_models())
        models.extend(self.get_lmstudio_models())
        return models

    def get_ollama_models(self):
        base = self.valves.OLLAMA_BASE_URL
        if not base:
            return []

        try:
            r = requests.get(f"{base}/api/tags", timeout=10)
            r.raise_for_status()
            data = r.json()

            return [
                {
                    "id": f"ollama::{m['model']}",
                    "name": f"CPU：{m['name']}",
                }
                for m in data.get("models", [])
            ]
        except Exception as e:
            print(f"[Ollama] Error: {e}")
            return []

    def get_lmstudio_models(self):
        base = self.valves.LMSTUDIO_BASE_URL
        if not base:
            return []

        try:
            r = requests.get(f"{base}/v1/models", timeout=10)
            r.raise_for_status()
            data = r.json()

            return [
                {
                    "id": f"lmstudio::{m['id']}",
                    "name": f"LM：{m['id']}",
                }
                for m in data.get("data", [])
            ]
        except Exception as e:
            print(f"[LMStudio] Error: {e}")
            return []

    # -----------------------------
    # Inference Routing
    # -----------------------------
    def pipe(
        self, user_message: str, model_id: str, messages: List[dict], body: dict
    ) -> Union[str, Generator, Iterator]:

        if "user" in body:
            print("######################################")
            print(f'# User: {body["user"]["name"]} ({body["user"]["id"]})')
            print(f"# Message: {user_message}")
            print("######################################")

        # --- Routing ---
        if model_id.startswith("ollama::"):
            base = self.valves.OLLAMA_BASE_URL
            real_model = model_id.replace("ollama::", "")

        elif model_id.startswith("lmstudio::"):
            base = self.valves.LMSTUDIO_BASE_URL
            real_model = model_id.replace("lmstudio::", "")

        else:
            return "Error: Unknown model provider"

        print(f"[pipeline] POST -> {base}/v1/chat/completions model={real_model}")

        try:
            r = requests.post(
                url=f"{base}/v1/chat/completions",
                json={**body, "model": real_model},
                stream=True,
                timeout=300,
            )
            r.raise_for_status()

            if body.get("stream"):
                return r.iter_lines()

            return r.json()

        except Exception as e:
            return f"Error: {e}"
