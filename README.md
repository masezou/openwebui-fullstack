# OpenWebUI Fullstack (GPU + CPU + RAG + Image Generation)

## ⚠️ WARNING (IMPORTANT)

This repository is provided **as a full-stack configuration sample only**.

- It is designed to demonstrate a working environment.
- **Security considerations are intentionally NOT implemented.**

Before using this in any real environment:

- You **MUST change all security-related settings**, including:
  - API keys
  - secret keys
  - authentication settings
- You **MUST review and harden security configurations**.

> Any damage, data loss, or security incidents caused by using this configuration without proper modifications are entirely your own responsibility.

---

## 🖥 Requirements

- Docker & Docker Compose
- NVIDIA GPU (recommended) or DGX Spark
- NVIDIA Container Toolkit

CPU-only mode may work but performance will be limited.

---

## 🌐 Network / Host Configuration

- Hostnames, IP addresses, and endpoints in this repository are **examples only**.
- You **must replace them** with values appropriate for your own environment.

---

## 🧩 Architecture Overview

This setup provides a **full-featured AI stack** with the following capabilities:

- **GPU + CPU hybrid inference**
  - GPU: primary inference (Ollama GPU)
  - CPU: fallback / pipeline processing (Ollama CPU via pipelines)
- **OpenWebUI frontend**
- **RAG (Retrieval-Augmented Generation)**
  - Vector DB: Qdrant (GPU-enabled)
  - Embeddings via Ollama
  - Reranking enabled
- **Image Generation**
  - ComfyUI integration
- **Web Search**
  - SearXNG
- **MCP Tooling**
  - memory, fetch, filesystem, etc.
- **Audio**
  - Whisper (STT)
  - Edge-TTS (TTS)
  
---

## 📁 Directory Structure

```
openwebui-fullstack/
├── compose.yml
├── data/
│   └── searxng/
│       └── settings.yml
├── mcpo/
│   └── config.json
├── pipelines/
│   └── ollama-lmstudio_manifold.py
└── tika-ja-full/
    ├── Dockerfile
    └── tika-config.xml
```

### Description

| Path | Description |
|------|------------|
| `compose.yml` | Main Docker Compose configuration |
| `data/searxng/settings.yml` | SearXNG search configuration |
| `mcpo/config.json` | MCP server configuration |
| `pipelines/` | Custom pipeline scripts |
| `tika-ja-full/` | Custom Apache Tika image |

---

## 🐳 Container Images Overview

### Core AI

- **ollama (GPU)** – Main LLM inference engine
- **ollama-cpu** – CPU fallback inference
- **pipeline** – Routing / integration layer

### UI / API

- **open-webui** – Main interface

### Data / RAG

- **qdrant** – Vector database
- **tika** – Document parser

### Search

- **searxng** – Meta search engine

### Tooling

- **mcpo** – MCP tool server

### Supporting

- **valkey** – Redis-compatible store
- **openai-edge-tts** – TTS engine
- **open-terminal / terminals** – Terminal integration

---

## 🚀 Usage

### 1. Clone

```bash
git clone https://github.com/your-repo/openwebui-fullstack.git
cd openwebui-fullstack
```

---

### 2. Build (Required)

This setup includes a **custom Apache Tika image**.

```bash
docker compose build tika
```

Or build everything:

```bash
docker compose build
```

---

### 3. Start

```bash
docker compose up -d
```

---

### 4. Access

http://localhost:3000

---

## ⚙️ First Startup Notes

- Initial startup may take several minutes.
- Models may be downloaded automatically.
- Vector database and embeddings may be initialized.

Please wait until all containers are healthy.

---

## ⚙️ Notes

- First startup may take time
- Ensure GPU is properly configured
- Replace all placeholder values before use

---

## 📌 Disclaimer

This configuration is intended for:

- learning
- testing
- local environments

**DO NOT use as-is in production.**
