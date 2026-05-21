import os
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cyber Team Help - Number Info Pro</title>
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;800;900&family=Share+Tech+Mono&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <style>
        body { 
            background-color: #020208; 
            font-family: 'Share Tech Mono', monospace; 
            min-height: 100vh;
        }
        .cyber-font { font-family: 'Orbitron', sans-serif; }
        
        /* Ultra Glowing Neon Effects */
        .neon-title {
            color: #00ffcc;
            text-shadow: 0 0 10px #00ffcc, 0 0 20px #00ffcc, 0 0 35px #00b3b3;
            animation: textGlow 1.5s infinite alternate;
        }
        .neon-credit {
            color: #ff0055;
            text-shadow: 0 0 8px #ff0055, 0 0 15px #ff0055;
        }
        
        /* Futuristic Interface Borders */
        .cyber-panel {
            background: rgba(6, 10, 26, 0.95);
            border: 2px solid #00ffcc;
            box-shadow: 0 0 25px rgba(0, 255, 204, 0.2), inset 0 0 20px rgba(0, 255, 204, 0.1);
        }
        
        /* Animated Matrix Background */
        .matrix-bg {
            background-image: linear-gradient(rgba(0, 255, 204, 0.04) 1px, transparent 1px),
                              linear-gradient(90deg, rgba(0, 255, 204, 0.04) 1px, transparent 1px);
            background-size: 20px 20px;
        }
        
        /* Running Cyber Laser Line */
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
<body class="matrix-bg flex flex-col items-center justify-center p-4 relative">

    <div class="absolute w-[250px] h-[250px] bg-cyan-500/10 blur-[100px] top-4 left-4 rounded-full pointer-events-none z-0"></div>
    <div class="absolute w-[250px] h-[250px] bg-pink-500/10 blur-[100px] bottom-4 right-4 rounded-full pointer-events-none z-0"></div>

    <div class="w-full max-w-md cyber-panel rounded-xl relative p-5 space-y-6 overflow-hidden z-10 my-6">
        <div class="laser-line"></div>
        
        <div class="w-full">
            <div class="flex justify-between items-center text-[9px] text-cyan-400/70 mb-3 font-mono border-b border-cyan-500/20 pb-1">
                <span>MAIN_FRAME: v6.0_POPUP</span>
                <span class="animate-pulse text-emerald-400"><i class="fa-solid fa-circle"></i> OSINT_READY</span>
            </div>

            <div class="text-center mb-5">
                <h1 class="text-2xl font-black cyber-font neon-title tracking-widest uppercase">
                    Cyber Team Help
                </h1>
                <p class="text-[10px] text-pink-400 cyber-font font-bold tracking-widest mt-0.5 uppercase">
                    [ Automated Intel Extraction ]
                </p>
            </div>

            <div class="space-y-3">
                <div class="relative">
                    <span class="absolute left-3 top-3.5 text-cyan-400 font-bold font-mono">></span>
                    <input type="tel" id="phoneNumber" placeholder="ENTER TARGET NUMBER (01XXXXXXXXX)" 
                           class="w-full pl-8 pr-4 py-3 bg-black/90 border border-cyan-500/40 rounded text-cyan-400 font-mono text-sm focus:outline-none focus:border-pink-500 focus:shadow-[0_0_15px_rgba(255,0,55,0.4)] transition-all placeholder-cyan-800">
                </div>
                <button onclick="executeHackingSequence()" class="w-full bg-gradient-to-r from-cyan-600 to-emerald-600 hover:from-cyan-500 hover:to-emerald-500 text-black font-black py-3 rounded cyber-font tracking-widest text-xs transition-all shadow-[0_0_15px_rgba(0,255,204,0.3)] flex items-center justify-center gap-2 cursor-pointer uppercase border border-cyan-300">
                    <i class="fa-solid fa-bolt animate-bounce"></i> Start Extractor
                </button>
            </div>
        </div>

        <div id="loaderBox" class="hidden flex flex-col items-center justify-center space-y-3 py-6">
            <div class="w-16 h-16 border-2 border-pink-500 rounded-lg flex items-center justify-center bg-black/80 shadow-[0_0_20px_rgba(255,0,85,0.3)] relative">
                <div class="absolute inset-0 border-2 border-cyan-400 animate-ping rounded-lg opacity-40"></div>
                <i class="fa-solid fa-mask text-2xl text-pink-500 animate-pulse"></i>
            </div>
            <p class="text-[11px] text-pink-400 font-mono tracking-widest uppercase animate-pulse">Decoding Signal Node...</p>
        </div>

        <div id="resultBox" class="hidden space-y-4">
            
            <div class="w-full bg-black/70 border border-cyan-500/40 rounded-lg p-4 relative shadow-[0_0_15px_rgba(0,255,204,0.1)] flex flex-col items-center">
                <div class="absolute top-2 left-2 text-[8px] text-cyan-400/50 font-mono">NODE_DECRYPT: SUCCESS</div>
                
                <div class="w-20 h-20 rounded-full border-2 border-dashed border-cyan-400 flex items-center justify-center bg-cyan-950/20 mb-3 relative shadow-[0_0_15px_rgba(0,255,204,0.2)]">
                    <i class="fa-solid fa-user-secret text-3xl text-cyan-400 animate-pulse"></i>
                    <div class="absolute bottom-0 right-0 w-4 h-4 bg-emerald-500 border-2 border-black rounded-full"></div>
                </div>
                
                <div class="text-center w-full space-y-1 mb-2">
                    <div id="resPhoneCard" class="text-md font-bold text-emerald-400 tracking-widest font-mono"></div>
                    <div class="text-[10px] text-pink-400 cyber-font uppercase tracking-wider">[ WhatsApp Target Found ]</div>
                </div>

                <a id="waLiveActionBtn" href="#" target="_blank" class="w-full mt-2 bg-gradient-to-r from-emerald-600 to-cyan-600 hover:from-emerald-500 hover:to-cyan-500 text-black font-black py-2.5 rounded text-center text-xs font-bold tracking-widest transition-all shadow-[0_0_10px_rgba(0,255,102,0.2)] uppercase block">
                    <i class="fa-brands fa-whatsapp text-sm mr-1"></i> Open Profile (Name & Picture)
                </a>
            </div>

            <div class="bg-black/90 p-3 border border-pink-500/30 rounded space-y-1.5 text-[11px] font-mono">
                <div class="flex items-center justify-between border-b border-pink-500/10 pb-1">
                    <span class="text-gray-500">TARGET_ID:</span>
                    <span id="resPhoneTable" class="text-cyan-400 font-bold"></span>
                </div>
                <div class="flex items-center justify-between border-b border-pink-500/10 pb-1">
                    <span class="text-gray-500">DATA_GATEWAY:</span>
                    <span class="text-emerald-400">WHATSAPP_API_BD</span>
                </div>
                <div class="flex items-center justify-between">
                    <span class="text-gray-500">EXPLOIT_LOG:</span>
                    <span class="text-yellow-400 font-bold animate-pulse">STREAM_ESTABLISHED</span>
                </div>
            </div>
        </div>

        <div class="border-t border-cyan-500/20 pt-3 text-center w-full">
            <div class="text-[9px] tracking-widest text-gray-600 font-mono uppercase">POWERED BY:</div>
            <div class="cyber-font font-black text-sm neon-credit tracking-widest mt-0.5 animate-pulse">
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
                alert('CRITICAL_ERR: Phone number field cannot be empty!');
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
                            // কার্ড ও টেবিল আপডেট
                            document.getElementById('resPhoneCard').innerText = data.formatted_phone;
                            document.getElementById('resPhoneTable').innerText = data.formatted_phone;
                            
                            // নতুন ট্যাবে/পপ-আপে ওপেন করার জন্য লিংক সেট
                            document.getElementById('waLiveActionBtn').href = data.links.click_to_chat;
                            
                            results.classList.remove('hidden');
                        } else {
                            alert('EXPLOIT_FAILED: ' + data.message);
                        }
                    })
                    .catch(err => {
                        loader.classList.add('hidden');
                        alert('CRITICAL_CRASH: Server node response error.');
                    });
            }, 1500); // স্মুথ লোডিং ট্র্যাকার টাইম
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

    # target="_blank" এর সাথে মিল রেখে ব্রাউজার সাপোর্টেড অফিশিয়াল ওপেনিং পপআপ লিংক
    links = {
        "click_to_chat": f"https://api.whatsapp.com/send/?phone={clean_phone}&text&type=phone_number&app_absent=0"
    }

    return jsonify({
        "status": "success",
        "formatted_phone": "+" + clean_phone,
        "links": links
    })
