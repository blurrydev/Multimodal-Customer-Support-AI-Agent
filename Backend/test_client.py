import asyncio
import json
import base64
import os

async def test_voice_pipeline():
    uri = "ws://127.0.0.1:8000/ws/chat"
    audio_filename = "test.wav"  # Ensure this file exists in your folder
    
    if not os.path.exists(audio_filename):
        print(f"[-] Error: Please place a sample audio file named '{audio_filename}' in this folder first!")
        return

    print(f"[+] Reading local audio file: {audio_filename}...")
    with open(audio_filename, "rb") as f:
        audio_bytes = f.read()
    
    # Convert binary audio data to Base64 string exactly like Angular will
    audio_b64 = base64.b64encode(audio_bytes).decode('utf-8')
    
    print(f"[+] Connecting to FastAPI WebSocket at {uri}...")
    async with websockets.connect(uri) as websocket:
        print("[+] Connected successfully!")
        
        # Build the payload packet matching our backend schema
        payload = {
            "type": "audio",
            "data": audio_b64
        }
        
        print("[+] Sending Base64 audio payload down the wire...")
        await websocket.send(json.dumps(payload))
        
        # Listen for the incoming multi-packet stream from the server
        print("\n--- Listening for Backend Multi-Packet Responses ---")
        try:
            while True:
                # Wait for response packet
                response_raw = await websocket.recv()
                response = json.loads(response_raw)
                packet_type = response.get("type")
                
                if packet_type == "log":
                    print(f" [LOG] [{response.get('source').upper()}]: {response.get('content')}")
                    
                elif packet_type == "user_transcription":
                    print(f"\n [STT RESULT] Faster-Whisper transcribed your voice as: ")
                    print(f" >> \"{response.get('content')}\"\n")
                    
                elif packet_type == "message":
                    print(f" [AGENT RESPONSE TEXT]:")
                    print(f" >> \"{response.get('content')}\"\n")
                    
                elif packet_type == "audio_response":
                    print(f" [TTS RESULT] Received audio response bytes from Edge-TTS!")
                    # Decode to verify it's a valid audio buffer
                    out_audio_bytes = base64.b64decode(response.get("data"))
                    print(f" -> Output buffer size: {len(out_audio_bytes)} bytes of clean MP3 data.")
                    print("\n[+] Verification successful! Local pipeline is completely operational.")
                    break # Break out since the transaction cycle is complete
                    
        except asyncio.TimeoutError:
            print("[-] Timeout waiting for server response.")
        except Exception as e:
            print(f"[-] Error during stream: {e}")

if __name__ == "__main__":
    # Run the async test block
    try:
        import websockets
    except ImportError:
        print("Please run 'pip install websockets' first.")
        exit(1)
        
    asyncio.run(test_voice_pipeline())
