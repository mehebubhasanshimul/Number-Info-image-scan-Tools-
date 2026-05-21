import os
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
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
        
        /* Ultra Glowing Neon Effects */
        .neon-title {
            color: #00ffcc;
            text-shadow: 0 0 10px #00ffcc, 0 0 20px #00ffcc, 0 0 40px #00b3b3;
            animation: textGlow 1.5s infinite alternate;
        }
        .neon-credit {
            color: #ff0055;
            text-shadow: 0 0 8px #ff0055, 0 0 15px #ff0055;
        }
        
        /* Futuristic Interface Borders */
        .cyber-panel {
            background: rgba(6, 10, 26, 0.9);
            border: 2px solid #00ffcc;
            box-shadow: 0 0 25px rgba(0, 255, 204, 0.25), inset 0 0 20px rgba(0, 255, 204, 0.1);
        }
        .result-panel {
            border: 2px solid #ff0055;
            box-shadow: 0 0 20px rgba(255, 0, 85, 0.2), inset 0 0 15px rgba(255, 0, 85, 0.05);
        }
        
        /* Animated Matrix Background */
        .matrix-bg {
            background-image: linear-gradient(rgba(0, 255, 204, 0.04) 1px, transparent 1px),
                              linear-gradient(90deg, rgba(0, 255, 204, 0.04) 1px, transparent 1px);
            background-size: 25px 25px;
        }
        
        /* Running Cyber Laser Line */
        .laser-line {
            width: 100%;
            height: 3px;
            background: linear-gradient(90deg, transparent, #ff0055, #00ffcc, transparent);
            position: absolute;
            animation: laserMove 4s linear infinite;
        }

        @keyframes laserMove {
            0% { top: 0%; }
            100% { top: 100%; }
        }
        @keyframes textGlow {
            0% { text-shadow: 0 0 8px #00ffcc, 0 0 15px #00ffcc; }
            100% { text-shadow: 0 0 15px #00ffcc, 0 0 30px #00ffcc; }
        }
    </style>
</head>
<body class="matrix-bg flex items-center justify-center p-3 w-full h-full relative">

    <div class="absolute w-[300px] h-[300px] bg-cyan-500/10 blur-[120px] top-10 left-10 rounded-full pointer-events-none"></div>
    <div class="absolute w-[300px] h-[300px] bg-pink-500/10 blur-[120px] bottom-10 right-10 rounded-full pointer-events-none"></div>

    <div class="w-full max-w-md h-[92vh] cyber-panel rounded-xl relative p-5 flex flex-col justify-between overflow-hidden">
        <div class="laser-line"></div>
        
        <div>
            <div class="flex justify-between items-center text-[10px] text-cyan-400/70 mb-3 font-mono border-b border-cyan-500/20 pb-1">
                <span>MAIN_FRAME: v3.4_LIVE</span>
                <span class="animate-pulse text-emerald-400"><i class="fa-solid fa-circle"></i> OSINT_ONLINE</span>
            </div>

            <div class="text-center mb-4">
                <h1 class="text-xl md:text-2xl font-black cyber-font neon-title tracking-widest uppercase">
                    Cyber Team Help
                </h1>
                <p class="text-[10px] text-pink-400 cyber-font font-bold tracking-widest mt-1 uppercase">
                    [ Automated Intel Extraction ]
                </p>
            </div>

            <div class="space-y-3">
                <div class="relative">
                    <span class="absolute left-3 top-3.5 text-cyan-400 font-bold font-mono">></span>
                    <input type="tel" id="phoneNumber" placeholder="ENTER TARGET NUMBER (01XXXXXXXXX)" 
                           class="w-full pl-8 pr-4 py-3 bg-black/90 border border-cyan-500/40 rounded text-cyan-400 font-mono text-sm focus:outline-none focus:border-pink-500 focus:shadow-[0_0_15px_rgba(255,0,85,0.4)] transition-all placeholder-cyan-800">
                </div>
                <button onclick="executeHackingSequence()" class="w-full bg-gradient-to-r from-cyan-600 to-emerald-600 hover:from-cyan-500 hover:to-emerald-500 text-black font-black py-3 rounded cyber-font tracking-widest text-xs transition-all shadow-[0_0_15px_rgba(0,255,204,0.3)] flex items-center justify-center gap-2 cursor-pointer uppercase border border-cyan-300">
                    <i class="fa-solid fa-bolt animate-bounce"></i> Start Extractor
                </button>
            </div>
        </div>

        <div id="loaderBox" class="hidden flex-1 flex flex-col items-center justify-center space-y-3 my-4">
            <div class="w-20 h-20 border-2 border-pink-500 rounded-lg flex items-center justify-center bg-black/80 shadow-[0_0_25px_rgba(255,0,85,0.3)] relative">
                <div class="absolute inset-0 border-2 border-cyan-400 animate-ping rounded-lg opacity-40"></div>
                <i class="fa-solid fa-mask text-3xl text-pink-500 animate-pulse"></i>
            </div>
            <p class="text-xs text-pink-400 font-mono tracking-widest uppercase animate-pulse">Bypassing Firewall...</p>
        </div>

        <div id="resultBox" class="hidden flex-1 flex flex-col justify-between my-3 overflow-hidden">
            <div class="flex-1 flex flex-col space-y-3 overflow-y-auto pr-1">
                <div class="text-[11px] font-bold text-pink-400 cyber-font flex items-center gap-2 mt-1">
                    <span class="w-2 h-2 bg-pink-500 rounded-full animate-ping"></span> SECURE_DECODING_COMPLETE:
                </div>
                
                <div class="w-full h-56 bg-black border-2 border-cyan-400/50 rounded-lg overflow-hidden relative shadow-[0_0_15px_rgba(0,255,204,0.15)]">
                    <div class="absolute top-0 left-0 w-full bg-cyan-950/80 border-b border-cyan-500/30 px-2 py-1 text-[9px] text-cyan-400 flex justify-between font-mono z-10">
                        <span>LIVE TARGET VIEWER</span>
                        <span class="text-emerald-400 font-bold">DECODED_DATA</span>
                    </div>
                    
                    <iframe id="liveSandboxFrame" src="" class="w-full h-full pt-5 border-none scale-100 origin-top"></iframe>
                </div>

                <div class="bg-black/90 p-3 border border-pink-500/30 rounded space-y-2 text-xs font-mono result-panel">
                    <div class="flex items-center justify-between border-b border-pink-500/10 pb-1.5">
                        <span class="text-gray-500">TARGET:</span>
                        <span id="resPhone" class="font-bold text-cyan-400 tracking-wider"></span>
                    </div>
                    <div class="flex items-center justify-between border-b border-pink-500/10 pb-1.5">
                        <span class="text-gray-500">PROVIDER_ID:</span>
                        <span class="text-emerald-400 font-bold">WHATSAPP_NODE_BD</span>
                    </div>
                    <div class="flex items-center justify-between">
                        <span class="text-gray-500">EXPLOIT_LOG:</span>
                        <span class="text-yellow-400 font-bold">LIVE_STREAM_LOADED</span>
                    </div>
                </div>
            </div>
        </div>

        <div class="border-t border-cyan-500/20 pt-2 text-center">
            <div class="text-[9px] tracking-widest text-gray-600 font-mono uppercase">POWERED BY:</div>
            <div class="cyber-font font-black text-sm neon-credit tracking-widest animate-pulse">
                SHADOW JOKER
            </div>
        </div>

    </div>

    <script>
        function executeHackingSequence() {
            const phoneInput = document.getElementById('phoneNumber').value.trim();
            const loader = document.getElementById('loaderBox');
            const results = document.getElementById('resultBox');

            if (!phoneInput) {
                alert('CRITICAL_ERR: Access Denied. Phone Number Required!');
                return;
            }

            results.classList.add('hidden');
            loader.classList.remove('hidden');

            setTimeout(() => {
                fetch(`/api/track?phone=${encodeURIComponent(phoneInput)}`)
                    .then(response => response.json())
                    .then(data => {
                        loader.classList.add('hidden');
                        if(data.status === "success") {
                            document.getElementById('resPhone').innerText = data.formatted_phone;
                            
                            // সরাসরি এই পেজের ফ্রেমের ভেতর লাইভ নাম ও ছবি লোড হবে
                            document.getElementById('liveSandboxFrame').src = data.links.live_view;
                            
                            results.classList.remove('hidden');
                        } else {
                            alert('EXPLOIT_FAILED: ' + data.message);
                        }
                    })
                    .catch(err => {
                        loader.classList.add('hidden');
                        alert('CRITICAL_CRASH: Data Extraction Network Failure.');
                    });
            }, 2000); // হ্যাকার লোডিং টাইম
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

    links = {
        "live_view": f"https://api.whatsapp.com/send/?phone={clean_phone}&text&type=phone_number&app_absent=0"
    }

    return jsonify({
        "status": "success",
        "formatted_phone": "+" + clean_phone,
        "links": links
    })
