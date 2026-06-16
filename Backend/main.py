import json
import base64
import io
import ast
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.messages import HumanMessage
from agent import agent_executor
import edge_tts
from faster_whisper import WhisperModel

app = FastAPI(title="NovaCart AI Support Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("Loading Faster-Whisper model...")
whisper_model = WhisperModel("tiny.en", device="cpu", compute_type="int8")
print("Local audio model loaded successfully!")

def extract_clean_text(raw_content: str) -> str:
    """Safely extracts clear conversational text from raw string or structural payloads."""
    if not raw_content:
        return ""
        
    text_str = str(raw_content).strip()
    
    if text_str.startswith("[") and text_str.endswith("]"):
        try:
            parsed_data = ast.literal_eval(text_str)
            if isinstance(parsed_data, list) and len(parsed_data) > 0:
                item = parsed_data[0]
                if isinstance(item, dict) and "text" in item:
                    return item["text"]
        except Exception:
            pass 
            
    return text_str

async def text_to_speech_bytes(text: str) -> bytes:
    """Converts text into high-quality MP3 bytes using edge-tts."""
    clean_text = extract_clean_text(text)
    if not clean_text:
        clean_text = "I am processing your request."
        
    communicate = edge_tts.Communicate(clean_text, "en-US-AriaNeural")
    
    audio_buffer = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_buffer += chunk["data"]
    return audio_buffer

@app.websocket("/ws/chat")
async def chat_websocket(websocket: WebSocket):
    await websocket.accept()
    
    current_state = {"messages": []}
    
    try:
        while True:
            raw_data = await websocket.receive_text()
            payload = json.loads(raw_data)
            
            user_message = ""
            current_input_mode = "text" 
            
            if payload.get("type") == "audio":
                current_input_mode = "audio" 
                
                audio_bytes = base64.b64decode(payload["data"])
                audio_file = io.BytesIO(audio_bytes)
                
                segments, _ = whisper_model.transcribe(audio_file, beam_size=1)
                user_message = "".join([segment.text for segment in segments]).strip()
                
                await websocket.send_json({
                    "type": "user_transcription",
                    "content": user_message
                })
                
            elif payload.get("type") == "text":
                current_input_mode = "text" 
                user_message = payload.get("message", "")
                
            if not user_message:
                continue

            current_state["messages"].append(HumanMessage(content=user_message))
            
            for event in agent_executor.stream(current_state):
                for node_name, node_state in event.items():
                    latest_message = node_state["messages"][-1]
                    
                    if node_name == "tools":
                        await websocket.send_json({
                            "type": "log",
                            "source": "database_tool",
                            "content": latest_message.content
                        })
                    
                    elif node_name == "chatbot" and not latest_message.tool_calls:
                        raw_text = latest_message.content
                        clean_text = extract_clean_text(raw_text)
                        
                        await websocket.send_json({
                            "type": "message",
                            "role": "agent",
                            "content": clean_text
                        })
                        
                        if current_input_mode == "audio":
                            await websocket.send_json({
                                "type": "log",
                                "source": "tts_engine",
                                "content": f"Synthesizing voice response for text: \"{clean_text[:40]}...\""
                            })
                            
                            try:
                                audio_out_bytes = await text_to_speech_bytes(clean_text)
                                audio_b64 = base64.b64encode(audio_out_bytes).decode('utf-8')
                                
                                await websocket.send_json({
                                    "type": "audio_response",
                                    "data": audio_b64
                                })
                            except Exception as tts_err:
                                await websocket.send_json({
                                    "type": "log",
                                    "source": "tts_engine",
                                    "content": f"Warning: Voice synthesis bypassed due to error: {str(tts_err)}"
                                })
                        else:
                            await websocket.send_json({
                                "type": "log",
                                "source": "tts_engine",
                                "content": "Voice synthesis bypassed (user typed the input)."
                            })
                        
    except WebSocketDisconnect:
        print("Frontend client disconnected safely.")
    except Exception as e:
        print(f"Error encountered in core websocket loop: {e}")

@app.get("/health")
def health_check():
    return {"status": "Active", "engine": "LangGraph + Gemini + Local Voice"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8000)
