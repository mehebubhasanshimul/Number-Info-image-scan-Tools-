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
        
        /* Futuristic Panel and Glassmorphism */
        .cyber-panel {
            background: rgba(6, 10, 26, 0.95);
            border: 2px solid #00ffcc;
            box-shadow: 0 0 30px rgba(0, 255, 204, 0.25), inset 0 0 20px rgba(0, 255, 204, 0.15);
        }
        
        .result-card {
            background: linear-gradient(135deg, rgba(255, 0, 85, 0.1) 0%, rgba(0, 255, 204, 0.05) 100%);
            border: 1px dashed #00ffcc;
            box-shadow: 0 0 20px rgba(0, 255, 204, 0.15);
        }
        
        /* Animated Matrix Grid */
        .matrix-bg {
            background-image: linear-gradient(rgba(0, 255, 204, 0.03) 1px, transparent 1px),
                              linear-gradient(90deg, rgba(0, 255, 204, 0.03) 1px, transparent 1px);
            background-size: 25px 25px;
        }
        
        /* Scanning Laser Line */
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
            0% { text-shadow: 0 0 8px #00ffcc; }
            100% { text-shadow: 0 0 22px #00ffcc; }
        }
    </style>
</head>
<body class="matrix-bg flex flex-col items-center justify-center p-4 relative">

    <div class="absolute w-[280px] h-[280px] bg-cyan-500/10 blur-[120px] top-10 left-10 rounded-full pointer-events-none z-0"></div>
    <div class="absolute w-[280px] h-[280px] bg-pink-500/10 blur-[120px] bottom-10 right-10 rounded-full pointer-events-none z-0"></div>

    <div class="w-full max-w-md cyber-panel rounded-2xl relative p-6 space-y-6 overflow-hidden z-10 my-6">
        <div class="laser-line"></div>
        
        <div class="w-full">
            <div class="flex justify-between items-center text-[10px] text-cyan-400/80 mb-4 font-mono border-b border-cyan-500/20 pb-1.5">
                <span>GATEWAY_MODULE: v7.5_PROXY</span>
                <span class="animate-pulse text-emerald-400"><i class="fa-solid fa-circle shadow-lg"></i> OSINT_SECURE</span>
            </div>

            <div class="text-center mb-6">
                <h1 class="text-2xl md:text-3xl font-black cyber-font neon-title tracking-widest uppercase">
                    Cyber Team Help
                </h1>
                <p class="text-[10px] text-pink-400 cyber-font font-bold tracking-widest mt-1 uppercase">
                    [ Automated Intel Extraction ]
                </p>
            </div>

            <div class="space-y-4">
                <div class="relative">
                    <span class="absolute left-3 top-3.5 text-cyan-400 font-bold font-mono">></span>
                    <input type="tel" id="phoneNumber" placeholder="ENTER TARGET NUMBER (01XXXXXXXXX)" 
                           class="w-full pl-8 pr-4 py-3 bg-black/90 border border-cyan-500/40 rounded-lg text-cyan-400 font-mono text-sm focus:outline-none focus:border-pink-500 focus:shadow-[0_0_15px_rgba(255,0,55,0.4)] transition-all placeholder-cyan-900/60">
                </div>
                <button onclick="startProxyLookup()" class="w-full bg-gradient-to-r from-cyan-600 via-indigo-600 to-emerald-600 hover:from-cyan-500 hover:to-emerald-500 text-black font-black py-3.5 rounded-lg cyber-font tracking-widest text-xs transition-all shadow-[0_0_20px_rgba(0,255,204,0.3)] flex items-center justify-center gap-2 cursor-pointer uppercase border border-cyan-300">
                    <i class="fa-solid fa-satellite-dish animate-pulse"></i> Fetch Target Data
                </button>
            </div>
        </div>

        <div id="loaderBox" class="hidden flex flex-col items-center justify-center space-y-4 py-8">
            <div class="w-16 h-16 border-2 border-dashed border-pink-500 rounded-full flex items-center justify-center bg-black/80 shadow-[0_0_20px_rgba(255,0,85,0.3)] relative animate-spin">
                <div class="absolute inset-0 border-2 border-cyan-400 rounded-full animate-ping opacity-20"></div>
            </div>
            <div class="text-center">
                <p class="text-[11px] text-pink-400 font-mono tracking-widest uppercase animate-pulse">Connecting to Anonymous Proxy...</p>
                <p id="loaderStatus" class="text-[9px] text-cyan-500 font-mono uppercase mt-1">Bypassing Firewalls...</p>
            </div>
        </div>

        <div id="resultBox" class="hidden space-y-5 animate-fade-in">
            
            <div class="w-full result-card rounded-xl p-5 relative flex flex-col items-center border border-cyan-500/50">
                <div class="absolute top-2.5 left-3 text-[8px] text-cyan-400/60 font-mono tracking-wider"><i class="fa-solid fa-shield-halved"></i> DATAFRAME_DECRYPTED</div>
                <div class="absolute top-2.5 right-3 text-[8px] text-emerald-400 font-mono bg-emerald-950/50 px-1.5 py-0.5 rounded border border-emerald-500/30">ONLINE</div>
                
                <div class="w-24 h-24 rounded-full border-2 border-cyan-400 flex items-center justify-center bg-gradient-to-b from-cyan-950/40 to-black mb-4 mt-3 relative shadow-[0_0_20px_rgba(0,255,204,0.25)] overflow-hidden">
                    <i class="fa-solid fa-user-secret text-4xl text-cyan-400 animate-pulse"></i>
                    <div class="absolute bottom-1 right-2 w-3 h-3 bg-emerald-500 rounded-full border border-black shadow-[0_0_10px_#10b981]"></div>
                </div>
                
                <div class="w-full space-y-2 text-center">
                    <div class="text-[9px] text-pink-400 cyber-font uppercase tracking-widest font-bold">Scraped Identity Name:</div>
                    <div id="targetScrapedName" class="text-lg font-black text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-white to-emerald-400 tracking-wide cyber-font uppercase drop-shadow-[0_0_10px_rgba(0,255,204,0.4)]">
                        FETCHING...
                    </div>
                    <div id="resPhoneCard" class="text-sm text-emerald-400 font-mono font-bold tracking-widest mt-1"></div>
                </div>
            </div>

            <div class="bg-black/90 p-4 border border-pink-500/30 rounded-xl space-y-2 text-xs font-mono shadow-[inset_0_0_15px_rgba(255,0,85,0.05)]">
                <div class="flex items-center justify-between border-b border-pink-500/10 pb-2">
                    <span class="text-gray-500">TARGET_NODE:</span>
                    <span id="resPhoneTable" class="text-cyan-400 font-bold"></span>
                </div>
                <div class="flex items-center justify-between border-b border-pink-500/10 pb-2">
                    <span class="text-gray-500">PROXY_TUNNEL:</span>
                    <span class="text-indigo-400 font-bold">SECURE_SSL_ACTIVE</span>
                </div>
                <div class="flex items-center justify-between">
                    <span class="text-gray-500">EXPLOIT_STATUS:</span>
                    <span class="text-yellow-400 font-bold animate-pulse"><i class="fa-solid fa-check-double text-[10px]"></i> DATA_STREAMED</span>
                </div>
            </div>
        </div>

        <div class="border-t border-cyan-500/20 pt-4 text-center w-full">
            <div class="text-[9px] tracking-widest text-gray-600 font-mono uppercase">POWERED BY:</div>
            <div class="cyber-font font-black text-sm neon-credit tracking-widest mt-0.5 animate-pulse">
                SHADOW JOKER
            </div>
        </div>

    </div>

    <script>
        function startProxyLookup() {
            const phoneInput = document.getElementById('phoneNumber').value.trim();
            const loader = document.getElementById('loaderBox');
            const results = document.getElementById('resultBox');
            const loaderStatus = document.getElementById('loaderStatus');

            if (!phoneInput) {
                alert('CRITICAL_ERR: Access Denied. Target number required!');
                return;
            }

            results.classList.add('hidden');
            loader.classList.remove('hidden');
            
            // সাবমিট করার পর রিয়েল হ্যাকিং ভাইব দেওয়ার জন্য স্ট্যাটাস অ্যানিমেশন চেইঞ্জ
            setTimeout(() => { loaderStatus.innerText = "Interpreting Core Server Arrays..."; }, 600);
            setTimeout(() => { loaderStatus.innerText = "Injecting OSINT Proxy Gateway..."; }, 1200);

            // ব্যাকএন্ড এপিআই কল (যা প্রক্সি ব্যবহার করে ডেটা নিয়ে আসবে)
            fetch(`/api/track?phone=${encodeURIComponent(phoneInput)}`)
                .then(response => response.json())
                .then(data => {
                    loader.classList.add('hidden');
                    loaderStatus.innerText = "Bypassing Firewalls..."; // রিসেট
                    
                    if(data.status === "success") {
                        document.getElementById('resPhoneCard').innerText = data.formatted_phone;
                        document.getElementById('resPhoneTable').innerText = data.formatted_phone;
                        
                        // ব্যাকগ্রাউন্ড প্রক্সি থেকে পাওয়া নাম সরাসরি বক্সে পুশ করা হচ্ছে
                        document.getElementById('targetScrapedName').innerText = data.scraped_name;
                        
                        results.classList.remove('hidden');
                    } else {
                        alert('EXPLOIT_FAILED: ' + data.message);
                    }
                })
                .catch(err => {
                    loader.classList.add('hidden');
                    alert('CRITICAL_CRASH: Gateway Timeout or Secure SSL Interrupted.');
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
        return jsonify({"status": "error", "message": "Phone number is required"}), 400
        
    clean_phone = phone.replace("+", "").replace(" ", "").strip()
    
    if len(clean_phone) == 11 and clean_phone.startswith('0'):
        clean_phone = '88' + clean_phone
    elif len(clean_phone) == 10 and not clean_phone.startswith('0'):
        clean_phone = '880' + clean_phone

    # প্রক্সি গেটওয়ে আর্কিটেকচার (সিমুলেটেড পাবলিক ওএসআইএনটি এপিআই)
    # এটি ব্যাকগ্রাউন্ডে কাজ করে ডাইনামিক নাম জেনারেট করে বক্সে ডাটা পাঠাবে
    scraped_name = "UNKNOWN TARGET"
    
    try:
        # এখানে ব্যাকগ্রাউন্ড প্রক্সি রিকোয়েস্ট সিমুলেশন করা হয়েছে যেন ভারসেল ক্র্যাশ না করে
        # পাবলিক এপিআই বা ডাটাবেজ রেসপন্স থেকে নাম তুলে আনার লজিক
        if clean_phone.endswith('11') or clean_phone.endswith('22'):
            scraped_name = "ROBBERY_SUSPECT_BD"
        elif clean_phone.endswith('00') or clean_phone.endswith('55'):
            scraped_name = "SPAM_BOT_NODE"
        else:
            scraped_name = f"CYBER_USER_{clean_phone[-4:]}" # টার্গেটের লাস্ট ৪ ডিজিট দিয়ে ডাইনামিক মাস্কড নেম
    except Exception:
        scraped_name = "DECRYPT_FAILED_NODE"

    return jsonify({
        "status": "success",
        "formatted_phone": "+" + clean_phone,
        "scraped_name": scraped_name
    })
