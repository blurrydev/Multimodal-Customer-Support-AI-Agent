import { Component, OnInit, OnDestroy, ViewChild, ElementRef, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

interface Message { role: 'user' | 'agent'; content: string; }

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App implements OnInit, OnDestroy {
  messages: Message[] = [];
  inputText: string = '';
  isListening: boolean = false;
  
  private ws!: WebSocket;
  private mediaRecorder: MediaRecorder | null = null;
  private audioChunks: Blob[] = [];
  private globalStream: MediaStream | null = null; // Keeps the mic "warm"

  @ViewChild('chatScroll') private chatScrollContainer!: ElementRef;

  constructor(private cdr: ChangeDetectorRef) {}

  async ngOnInit() {
    this.initWebSocket();
    // Warm up the microphone instantly on page load
    try {
      this.globalStream = await navigator.mediaDevices.getUserMedia({ audio: true });
    } catch (err) {
      console.warn("Microphone access deferred or denied.", err);
    }
  }

  ngOnDestroy() {
    if (this.ws) this.ws.close();
    if (this.globalStream) {
      this.globalStream.getTracks().forEach(track => track.stop());
    }
  }

  private initWebSocket() {
    this.ws = new WebSocket('ws://127.0.0.1:8000/ws/chat');

    this.ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      
      if (data.type === 'message' || data.type === 'user_transcription') {
        this.messages.push({ 
          role: data.type === 'message' ? 'agent' : 'user', 
          content: data.content 
        });
        this.scrollToBottom();
      }
      else if (data.type === 'audio_response') {
        const audioSrc = 'data:audio/mp3;base64,' + data.data;
        const audio = new Audio(audioSrc);
        audio.play().catch(e => console.error("Audio playback failed:", e));
      }
      else if (data.type === 'log') {
        // Silently log admin events to the browser console instead of the UI
        console.log(`[Backend Log - ${data.source}]: ${data.content}`);
      }
      
      this.cdr.detectChanges();
    };
  }

  // --- ZERO-LATENCY VOICE CAPTURE ---
  async toggleMicrophone() {
    if (this.isListening) {
      this.stopRecording();
    } else {
      // Instantly update UI state
      this.isListening = true; 
      await this.startRecording();
    }
  }

  private async startRecording() {
    try {
      if (!this.globalStream) {
        this.globalStream = await navigator.mediaDevices.getUserMedia({ audio: true });
      }
      
      this.mediaRecorder = new MediaRecorder(this.globalStream);
      this.audioChunks = [];

      this.mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) this.audioChunks.push(event.data);
      };

      this.mediaRecorder.onstop = () => {
        const audioBlob = new Blob(this.audioChunks, { type: 'audio/webm' });
        const reader = new FileReader();
        
        reader.readAsDataURL(audioBlob);
        reader.onloadend = () => {
          const base64String = (reader.result as string).split(',')[1];
          this.ws.send(JSON.stringify({ type: 'audio', data: base64String }));
        };
        // We intentionally DO NOT stop the globalStream tracks here so it stays warm
      };

      this.mediaRecorder.start();
    } catch (error) {
      this.isListening = false;
      console.error('Microphone access failed:', error);
    }
  }

  private stopRecording() {
    if (this.mediaRecorder && this.mediaRecorder.state !== 'inactive') {
      this.mediaRecorder.stop();
      this.isListening = false;
    }
  }

  // --- TEXT CAPTURE ---
  sendMessage() {
    if (!this.inputText.trim() || !this.ws) return;

    this.messages.push({ role: 'user', content: this.inputText });
    this.ws.send(JSON.stringify({ type: 'text', message: this.inputText }));
    this.inputText = '';
    this.scrollToBottom();
  }

  private scrollToBottom() {
    setTimeout(() => {
      try {
        this.chatScrollContainer.nativeElement.scrollTop = this.chatScrollContainer.nativeElement.scrollHeight;
      } catch (err) {}
    }, 100);
  }
}