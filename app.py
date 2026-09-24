import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import urllib.request
import json

app = FastAPI(title="LYRA AI - Local Permanent Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    message: str

def query_local_ollama(user_prompt: str) -> str:
    """Direct Local Ollama Llama-3 Engine (100% Permanent & Free)"""
    try:
        url = "http://127.0.0.1:11434/api/generate"
        payload = json.dumps({
            "model": "llama3.2:1b",  # Fast, lightweight & accurate model
            "prompt": f"System: You are Lyra, a fact-checked AI assistant. Always provide historically and geographically accurate details. Do not invent non-existent ethnic groups or languages. If uncertain, state that you don't know.\nUser: {user_prompt}\nLyra:",
            "stream": False
        }).encode('utf-8')
        
        req = urllib.request.Request(
            url, 
            data=payload, 
            headers={'Content-Type': 'application/json'}
        )
        
        with urllib.request.urlopen(req, timeout=60) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            return res_data.get("response", "No response generated.")
    except Exception as e:
        return f"Local Engine Error: {str(e)}"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LYRA AI - Permanent Local Llama</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Plus Jakarta Sans', sans-serif; }
        .glass { background: rgba(18, 18, 24, 0.7); backdrop-filter: blur(16px); border: 1px solid rgba(255, 255, 255, 0.08); }
        .glow { box-shadow: 0 0 50px -10px rgba(99, 102, 241, 0.25); }
    </style>
</head>
<body class="bg-[#09090b] text-slate-100 h-screen flex flex-col justify-between overflow-hidden">
    
    <!-- Top Header -->
    <header class="glass mx-4 mt-4 px-6 py-4 rounded-2xl flex items-center justify-between border-b border-white/5">
        <div class="flex items-center gap-3">
            <div class="w-3 h-3 rounded-full bg-indigo-500 animate-pulse"></div>
            <h1 class="text-xl font-bold tracking-wider bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">LYRA AI</h1>
        </div>
        <div class="flex items-center gap-2">
            <span class="text-xs font-semibold px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-300 border border-emerald-500/20">
                100% Local Permanent Model
            </span>
            <span class="text-xs font-semibold px-3 py-1 rounded-full bg-indigo-500/10 text-indigo-300 border border-indigo-500/20">
                Created by Muhammad Taqi
            </span>
        </div>
    </header>

    <!-- Chat Box -->
    <main id="chat-box" class="flex-1 overflow-y-auto p-4 md:p-6 space-y-4 max-w-4xl w-full mx-auto">
        <div class="glass p-5 rounded-2xl max-w-[85%] border border-indigo-500/20 glow">
            <p class="text-xs text-indigo-400 font-semibold mb-1">LYRA</p>
            <p class="text-sm md:text-base leading-relaxed text-slate-200">
                Hello! Main **Lyra** hoon. Mera AI model ab bilkul local chal raha hai bina kisi external API key ya rate limit ke. Aap kitni bhi chahein unlimited chatting kar sakte hain!
            </p>
        </div>
    </main>

    <!-- Input -->
    <footer class="p-4 max-w-4xl w-full mx-auto">
        <div class="glass p-2 rounded-2xl flex items-center gap-2 border border-white/10 glow">
            <input id="user-input" type="text" placeholder="Ask Lyra anything..." 
                   class="flex-1 bg-transparent px-4 py-3 text-sm md:text-base outline-none text-slate-100 placeholder-slate-500"
                   onkeydown="if(event.key === 'Enter') sendMessage()">
            <button onclick="sendMessage()" 
                    class="bg-indigo-600 hover:bg-indigo-500 text-white px-5 py-3 rounded-xl font-medium text-sm transition-all duration-200 shadow-lg shadow-indigo-600/30">
                Send
            </button>
        </div>
    </footer>

    <script>
        async function sendMessage() {
            const input = document.getElementById('user-input');
            const msg = input.value.trim();
            if (!msg) return;

            const chatBox = document.getElementById('chat-box');
            
            chatBox.innerHTML += `
                <div class="flex justify-end">
                    <div class="bg-indigo-600/30 border border-indigo-500/30 p-4 rounded-2xl max-w-[85%]">
                        <p class="text-xs text-indigo-300 font-semibold mb-1">YOU</p>
                        <p class="text-sm md:text-base text-slate-100">${msg}</p>
                    </div>
                </div>
            `;
            
            input.value = '';
            chatBox.scrollTop = chatBox.scrollHeight;

            const loadingId = 'load-' + Date.now();
            chatBox.innerHTML += `
                <div id="${loadingId}" class="glass p-4 rounded-2xl max-w-[85%] border border-white/5">
                    <p class="text-xs text-purple-400 font-semibold mb-1">LYRA</p>
                    <p class="text-sm text-slate-400 animate-pulse">Lyra local engine is thinking...</p>
                </div>
            `;
            chatBox.scrollTop = chatBox.scrollHeight;

            try {
                const res = await fetch('/api/ask', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ message: msg })
                });
                const data = await res.json();
                
                document.getElementById(loadingId).remove();
                chatBox.innerHTML += `
                    <div class="glass p-5 rounded-2xl max-w-[85%] border border-indigo-500/20 glow">
                        <p class="text-xs text-indigo-400 font-semibold mb-1">LYRA</p>
                        <p class="text-sm md:text-base leading-relaxed text-slate-200">${data.response}</p>
                    </div>
                `;
            } catch (err) {
                document.getElementById(loadingId).remove();
                chatBox.innerHTML += `
                    <div class="glass p-4 rounded-2xl max-w-[85%] border border-red-500/20">
                        <p class="text-xs text-red-400 font-semibold mb-1">ERROR</p>
                        <p class="text-sm text-slate-300">Local model response error.</p>
                    </div>
                `;
            }
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def get_ui():
    return HTML_TEMPLATE

@app.post("/api/ask")
async def ask_lyra(req: QueryRequest):
    try:
        response = await asyncio.to_thread(query_local_ollama, req.message)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
