# NovaCart AI Support Engine

This project consists of a FastAPI backend using LangGraph, Gemini, and Local Voice (Faster-Whisper + Edge-TTS) and an Angular frontend.

## Prerequisites

Before you begin, ensure you have the following installed:
- **Python 3.13+**
- **Node.js** (latest LTS recommended)
- **Git**

---

## Project Structure

- `Backend/`: FastAPI application, AI agent logic, and database.
- `Frontend/`: Angular application for the user interface.

---

## Backend Setup

1. **Navigate to the Backend directory:**
   ```bash
   cd Backend
   ```

2. **Create a virtual environment:**
   We recommend using `uv` for faster dependency management, but standard `venv` works too.

   **Using `uv` (Recommended):**
   ```bash
   # Install uv if you haven't: https://github.com/astral-sh/uv
   uv venv
   uv sync
   ```

   **Using `venv`:**
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # macOS/Linux:
   source .venv/bin/activate
   
   pip install -r req.txt
   ```

3. **Configure Environment Variables:**
   - Copy the example environment file:
     ```bash
     cp .env.example .env
     ```
   - Open `.env` and add your `GEMINI_API_KEY`.

4. **Initialize the Database:**
   ```bash
   python db/create_db.py
   ```

5. **Run the Backend:**
   ```bash
   python main.py
   ```
   The backend will start at `http://localhost:8000`.

---

## Frontend Setup

1. **Navigate to the Frontend directory:**
   ```bash
   cd Frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Run the Frontend:**
   ```bash
   npm start
   ```
   Open your browser and navigate to `http://localhost:4200/`.

---

## Troubleshooting

- **Python Version:** Ensure you are using Python 3.13 or higher as specified in `pyproject.toml`.
- **Port Conflicts:** Ensure ports `8000` (Backend) and `4200` (Frontend) are available.
- **Microphone Access:** The application requires microphone access for audio input features.
- **API Keys:** Ensure your Gemini API key is valid and has sufficient quota.

---
