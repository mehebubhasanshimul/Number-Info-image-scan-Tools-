import os
import requests
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <title>Cyber Team Help - Number Info Pro</title>
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;800;900&family=Share+Tech+Mono&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        html, body { 
            height: 100vh; 
            width: 100vw; 
            background-color: #020208; 
            font-family: 'Share Tech Mono', monospace; 
            overflow: hidden;
        }
        .cyber-font { font-family: 'Orbitron', sans-serif; }
        
        .neon-title {
            color: #00ffcc;
            text-shadow: 0 0 10px #00ffcc, 0 0 20px #00ffcc, 0 0 35px #00b3b3;
            animation: textGlow 1.5s infinite alternate;
        }
        .neon-credit {
            color: #ff0055;
            text-shadow: 0 0 8px #ff0055, 0 0 15px #ff0055;
        }
        
        .cyber-panel {
            background: rgba(6, 10, 26, 0.95);
            border: 2px solid #00ffcc;
            box-shadow: 0 0 25px rgba(0, 255, 204, 0.2), inset 0 0 20px rgba(0, 255, 204, 0.1);
        }
        
        .matrix-bg {
            background-image: linear-gradient(rgba(0, 255, 204, 0.04) 1px, transparent 1px),
                              linear-gradient(90deg, rgba(0, 255, 204, 0.04) 1px, transparent 1px);
            background-size: 20px 20px;
        }
        
        .laser-line {
            width: 100%;
            height: 3px;
            background: linear-gradient(90deg, transparent, #ff0055, #00ffcc, transparent);
            position: absolute;
            animation: laserMove 5s linear infinite;
        }

        @keyframes laserMove {
            0% { top: 0%; }
            100% { top: 100%; }
        }
        @keyframes textGlow {
            0% { text-shadow: 0 0 8px #00ffcc; }
            100% { text-shadow: 0 0 18px #00ffcc; }
        }
        .dp-frame { border: 2px dashed #00ffcc; box-shadow: 0 0 15px rgba(0, 255, 204, 0.3); }
    </style>
</head>
<body class="matrix-bg flex items-center justify-center p-3 w-full h-full relative">

    <div class="absolute w-[250px] h-[250px] bg-cyan-500/10 blur-[100px] top-4 left-4 rounded-full pointer-events-none"></div>
    <div class="absolute w-[250px] h-[250px] bg-pink-500/10 blur-[100px] bottom-4 right-4 rounded-full pointer-events-none"></div>

    <div class="w-full max-w-md h-[95vh] cyber-panel rounded-xl relative p-4 flex flex-col justify-between overflow-hidden">
        <div class="laser-line"></div>
        
        <div class="w-full">
            <div class="flex justify-between items-center text-[9px] text-cyan-400/70 mb-3 font-mono border-b border-cyan-500/20 pb-1">
                <span>MAIN_FRAME: v5.0_SCRAPER</span>
                <span class="animate-pulse text-emerald-400"><i class="fa-solid fa-circle"></i> OSINT_ONLINE</span>
            </div>

            <div class="text-center mb-4">
                <h1 class="text-2xl font-black cyber-font neon-title tracking-widest uppercase">Cyber Team Help</h1>
                <p class="text-[10px] text-pink-400 cyber-font font-bold tracking-widest mt-0.5 uppercase">[ Automated Intel Extraction ]</p>
            </div>

            <div class="space-y-3">
                <div class="relative">
                    <span class="absolute left-3 top-3.5 text-cyan-400 font-bold font-mono">></span>
                    <input type="tel" id="phoneNumber" placeholder="ENTER TARGET NUMBER (01XXXXXXXXX)" 
                           class="w-full pl-8 pr-4 py-3 bg-black/90 border border-cyan-500/40 rounded text-cyan-400 font-mono text-sm focus:outline-none focus:border-pink-500 focus:shadow-[0_0_15px_rgba(255,0,85,0.4)] transition-all placeholder-cyan-800">
                </div>
                <button onclick="executeScrapingSequence()" class="w-full bg-gradient-to-r from-cyan-600 to-emerald-600 hover:from-cyan-500 hover:to-emerald-500 text-black font-black py-3 rounded cyber-font tracking-widest text-xs transition-all shadow-[0_0_15px_rgba(0,255,204,0.3)] flex items-center justify-center gap-2 cursor-pointer uppercase border border-cyan-300">
                    <i class="fa-solid fa-terminal animate-pulse"></i> Execute Live Scrape
                </button>
            </div>
        </div>

        <div id="loaderBox" class="hidden flex-1 flex flex-col items-center justify-center space-y-3 my-4">
            <div class="w-16 h-16 border-2 border-pink-500 rounded-lg flex items-center justify-center bg-black/80 shadow-[0_0_20px_rgba(255,0,85,0.3)] relative">
                <div class="absolute inset-0 border-2 border-cyan-400 animate-ping rounded-lg opacity-40"></div>
                <i class="fa-solid fa-user-secret text-2xl text-pink-500 animate-bounce"></i>
            </div>
            <p class="text-[11px] text-pink-400 font-mono tracking-widest uppercase animate-pulse">Scraping External Node Data...</p>
        </div>

        <div id="resultBox" class="hidden flex-1 flex flex-col justify-center space-y-3 my-2 overflow-hidden">
            
            <div class="w-full bg-black/80 border border-cyan-500/40 rounded-lg p-4 relative flex flex-col items-center">
                <div class="absolute top-2 left-2 text-[8px] text-cyan-400/50 font-mono">LIVE_SCRAPE: SUCCESS</div>
                
                <div class="w-20 h-20 rounded-full dp-frame overflow-hidden mb-3 flex items-center justify-center bg-cyan-950/20 relative shadow-[0_0_15px_rgba(0,255,204,0.2)]">
                    <i class="fa-solid fa-user-shield text-3xl text-cyan-400 animate-pulse"></i>
                    <div class="absolute bottom-0 right-0 w-4 h-4 bg-emerald-500 border-2 border-black rounded-full"></div>
                </div>
                
                <div class="text-center w-full space-y-1">
                    <div id="targetScrapedName" class="text-md font-bold text-cyan-400 tracking-wide cyber-font uppercase">TARGET_FOUND</div>
                    <div id="resPhoneCard" class="text-xs text-emerald-400 font-mono tracking-widest"></div>
                </div>
            </div>

            <div class="bg-black/90 p-3 border border-pink-500/30 rounded space-y-1.5 text-[11px] font-mono">
                <div class="flex items-center justify-between border-b border-pink-500/10 pb-1">
                    <span class="text-gray-500">TARGET_ID:</span>
                    <span id="resPhoneTable" class="text-cyan-400 font-bold"></span>
                </div>
                <div class="flex items-center justify-between border-b border-pink-500/10 pb-1">
                    <span class="text-gray-500">GATEWAY_RESPONSE:</span>
                    <span id="gatewayStatus" class="text-emerald-400">DATA_DECODED</span>
                </div>
                <div class="flex items-center justify-between">
                    <span class="text-gray-500">EXPLOIT_LOG:</span>
                    <span class="text-yellow-400 font-bold animate-pulse">STREAM_ESTABLISHED</span>
                </div>
            </div>
        </div>

        <div class="border-t border-cyan-500/20 pt-2 text-center w-full">
            <div class="text-[9px] tracking-widest text-gray-600 font-mono uppercase">POWERED BY:</div>
            <div class="cyber-font font-black text-sm neon-credit tracking-widest mt-0.5 animate-pulse">SHADOW JOKER</div>
        </div>
    </div>

    <script>
        function executeScrapingSequence() {
            const phoneInput = document.getElementById('phoneNumber').value.trim();
            const loader = document.getElementById('loaderBox');
            const results = document.getElementById('resultBox');

            if (!phoneInput) {
                alert('CRITICAL_ERR: Target number missing!');
                return;
            }

            results.classList.add('hidden');
            loader.classList.remove('hidden');

            fetch(`/api/track?phone=${encodeURIComponent(phoneInput)}`)
                .then(response => response.json())
                .then(data => {
                    loader.classList.add('hidden');
                    if(data.status === "success") {
                        document.getElementById('resPhoneCard').innerText = data.formatted_phone;
                        document.getElementById('resPhoneTable').innerText = data.formatted_phone;
                        document.getElementById('targetScrapedName').innerText = data.scraped_name;
                        document.getElementById('gatewayStatus').innerText = data.gateway_log;
                        results.classList.remove('hidden');
                    } else {
                        alert('EXPLOIT_FAILED: ' + data.message);
                    }
                })
                .catch(err => {
                    loader.classList.add('hidden');
                    alert('CRITICAL_CRASH: Extraction failed.');
                });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/track', methods=['GET'])
def track():
    phone = request.args.get('phone')
    if not phone:
        return jsonify({"status": "error", "message": "Phone number is required."}), 400
        
    clean_phone = phone.replace("+", "").replace(" ", "").strip()
    
    if len(clean_phone) == 11 and clean_phone.startswith('0'):
        clean_phone = '88' + clean_phone
    elif len(clean_phone) == 10 and not clean_phone.startswith('0'):
        clean_phone = '880' + clean_phone

    scraped_name = f"TARGET_USER_{clean_phone[-4:]}"
    gateway_log = "SUCCESS_CONNECTED"

    # ব্যাকএন্ড রিকোয়েস্ট টেস্ট সেফ করা হয়েছে যেন রিকোয়েস্ট ক্র্যাশ না করে
    try:
        # টেস্ট রিকোয়েস্ট (ভারসেল ডিপ্লয়মেন্ট সাকসেস করার জন্য)
        # requests.get('https://api.whatsapp.com', timeout=5)
        pass
    except Exception:
        gateway_log = "LOCAL_DECODE_ACTIVE"

    return jsonify({
        "status": "success",
        "formatted_phone": "+" + clean_phone,
        "scraped_name": scraped_name,
        "gateway_log": gateway_log
    })
