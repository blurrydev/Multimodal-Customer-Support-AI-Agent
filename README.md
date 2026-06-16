# NovaCart AI Support Agent

A full-stack web application featuring an autonomous customer support agent. The agent processes and evaluates e-commerce refund requests using a LangGraph state machine, Google Gemini, and a mock SQLite CRM database. 

It includes a real-time multimodal interface supporting both text input and local voice stream processing.

## Architecture & Tech Stack

* **Frontend:** Angular 19, Vanilla CSS
* **Backend:** FastAPI, WebSockets
* **Agent Orchestration:** LangGraph, LangChain
* **LLM:** Google Gemini
* **Speech-to-Text (STT):** `faster-whisper` (Local)
* **Text-to-Speech (TTS):** `edge-tts`
* **Database:** SQLite

## Core Features

* **Policy-Driven Tool Calling:** The LangGraph conditional routing forces the agent to query the SQLite order database to validate purchase dates against a strict 14-day refund policy before issuing a decision.
* **Multimodal WebSocket Gateway:** The FastAPI backend dynamically processes standard JSON text payloads and Base64-encoded audio chunks over a single WebSocket connection. 
* **Local Voice Processing:** Audio processing is handled locally via `faster-whisper` and `edge-tts` to reduce API latency and avoid sending raw audio streams to external third-party endpoints.
* **Reasoning Logs:** Internal LangGraph execution steps and tool-call events are exposed in real-time for debugging and admin tracking.

---

## Local Setup Instructions

### Prerequisites
* Python 3.10+
* Node.js v21+

### 1. Backend Setup (FastAPI + LangGraph)

Navigate to the `backend` directory:

```bash
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
