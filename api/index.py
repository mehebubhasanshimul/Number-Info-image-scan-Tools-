import os
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cyber Team Help - Number Info</title>
    <!-- Tailwind CSS & Google Fonts -->
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <style>
        body {
            background-color: #050811;
            font-family: 'Share Tech Mono', 'Courier New', monospace;
            overflow-x: hidden;
        }
        .cyber-font {
            font-family: 'Orbitron', sans-serif;
        }
        /* Neon Animated Glow Text Effect */
        .neon-text-green {
            color: #00ff66;
            text-shadow: 0 0 5px #00ff66, 0 0 10px #00ff66, 0 0 20px #00cc52;
            animation: glitch 2s infinite alternate;
        }
        .neon-text-cyan {
            color: #00f0ff;
            text-shadow: 0 0 5px #00f0ff, 0 0 10px #00f0ff, 0 0 20px #00c8ff;
        }
        /* Cyber Terminal Box */
        .cyber-box {
            background: rgba(10, 15, 30, 0.85);
            border: 2px solid #00ff66;
            box-shadow: 0 0 15px rgba(0, 255, 102, 0.2), inset 0 0 15px rgba(0, 255, 102, 0.1);
            backdrop-filter: blur(8px);
        }
        /* Scanline Running Animation */
        .scanline {
            background: linear-gradient(
                to bottom,
                rgba(255,255,255,0) 0%,
                rgba(0, 255, 102, 0.1) 10%,
                rgba(255,255,255,0) 20%
            );
            background-size: 100% 20px;
            animation: scan 6s linear infinite;
        }
        /* Animations */
        @keyframes scan {
            0% { background-position: 0 0; }
            100% { background-position: 0 100%; }
        }
        @keyframes glitch {
            0% { text-shadow: 0 0 4px #00ff66, 0 0 10px #00ff66; }
            50% { text-shadow: 0 0 2px #00ff66, 0 0 7px #00ff66; }
            100% { text-shadow: 0 0 8px #00ff66, 0 0 15px #00cc52; }
        }
        /* Matrix Grid Background Simulation */
        .bg-matrix {
            background-image: linear-gradient(rgba(0, 255, 102, 0.03) 1px, transparent 1px),
                              linear-gradient(90deg, rgba(0, 255, 102, 0.03) 1px, transparent 1px);
            background-size: 20px 20px;
        }
    </style>
</head>
<body class="bg-matrix scanline flex flex-col min-h-screen items-center justify-center p-4">

    <!-- Main Container -->
    <div class="w-full max-w-xl cyber-box p-6 rounded-lg relative overflow-hidden">
        
        <!-- Top Tech Lines Decor -->
        <div class="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-emerald-500 to-transparent"></div>
        <div class="flex justify-between text-[10px] text-emerald-500/60 mb-4 font-mono">
            <span>SYS_STATUS: ACTIVE</span>
            <span>SECURE_NODE_ALPHA</span>
        </div>

        <!-- Branding Header -->
        <div class="text-center mb-6">
            <h1 class="text-2xl md:text-3xl font-black cyber-font neon-text-green tracking-widest uppercase mb-1">
                Cyber Team Help
            </h1>
            <div class="text-cyan-400 cyber-font font-bold text-xs tracking-wider uppercase mb-2">
                [ Number Info & OSINT Core ]
            </div>
            <div class="h-[1px] bg-emerald-500/30 w-3/4 mx-auto my-3"></div>
        </div>

        <!-- Input Terminal Section -->
        <div class="space-y-4 mb-6">
            <div class="relative">
                <span class="absolute left-3 top-3.5 text-emerald-500 font-bold font-mono">></span>
                <input type="tel" id="phoneNumber" placeholder="TARGET_PHONE_NUMBER (e.g. 019XXXXXXXX)" 
                       class="w-full pl-8 pr-4 py-3 bg-black/80 border border-emerald-500/40 rounded text-emerald-400 font-mono focus:outline-none focus:border-cyan-400 focus:shadow-[0_0_10px_rgba(0,240,255,0.3)] transition-all placeholder-emerald-700 text-sm">
            </div>
            <button onclick="startInvestigation()" class="w-full bg-emerald-600 hover:bg-emerald-500 border border-emerald-400 text-black font-black py-3 rounded cyber-font tracking-widest text-sm transition-all duration-300 shadow-[0_0_15px_rgba(0,255,102,0.3)] hover:shadow-[0_0_25px_rgba(0,255,102,0.6)] flex items-center justify-center gap-2 cursor-pointer uppercase">
                <i class="fa-solid fa-terminal animate-pulse"></i> Execute Intelligence Search
            </button>
        </div>

        <!-- Hacker Style GIF Loading System -->
        <div id="loaderBox" class="hidden flex flex-col items-center justify-center py-8 space-y-3">
            <!-- Neon Glowing Hacker Matrix GIF Matrix Style Simulator Loader -->
            <div class="w-24 h-24 border-2 border-cyan-500/30 rounded-lg flex items-center justify-center relative bg-black/60 shadow-[0_0_20px_rgba(0,240,255,0.15)]">
                <div class="absolute inset-1 border border-emerald-500/20 animate-ping rounded"></div>
                <i class="fa-solid fa-user-secret text-4xl text-emerald-400 animate-bounce"></i>
            </div>
            <div class="text-xs text-cyan-400 font-mono tracking-widest uppercase animate-pulse">
                Extracting Data From WhatsApp Node...
            </div>
        </div>

        <!-- Advanced OSINT Result Layout Box -->
        <div id="resultBox" class="hidden space-y-4">
            <div class="border-t-2 border-emerald-500/40 pt-4">
                <div class="text-xs font-bold text-emerald-400 mb-2 cyber-font flex items-center gap-2">
                    <span class="inline-block w-2 h-2 bg-emerald-500 animate-ping rounded-full"></span> 
                    INTEL_REPORT_GENERATED:
                </div>
                
                <!-- Main Grid Card Display Information Box -->
                <div class="bg-black/80 p-4 border border-emerald-500/20 rounded space-y-3 text-xs md:text-sm font-mono relative">
                    <div class="absolute top-2 right-2 text-[9px] text-emerald-500/30 font-bold">TYPE: WA_CORE</div>
                    
                    <div class="flex items-center justify-between border-b border-emerald-500/10 pb-2">
                        <span class="text-gray-500">TARGET_NUMBER:</span>
                        <span id="resPhone" class="font-bold text-cyan-400 tracking-wider"></span>
                    </div>
                    <div class="flex items-center justify-between border-b border-emerald-500/10 pb-2">
                        <span class="text-gray-500">REGION_ORIGIN:</span>
                        <span class="text-emerald-400">Bangladesh (BD)</span>
                    </div>
                    <div class="flex items-center justify-between border-b border-emerald-500/10 pb-2">
                        <span class="text-gray-500">OSINT_STATUS:</span>
                        <span class="text-yellow-400 animate-pulse font-bold">READY TO DECODE</span>
                    </div>
                </div>
            </div>

            <!-- Custom Cyber Actions Buttons Block -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-2 pt-2">
                <a id="waChat" href="#" target="_blank" class="bg-emerald-950/40 hover:bg-emerald-900/60 text-emerald-400 border border-emerald-500/40 py-3 rounded font-bold text-center text-xs transition-all cyber-font flex items-center justify-center gap-2 shadow-[0_0_10px_rgba(0,255,102,0.1)]">
                    <i class="fa-brands fa-whatsapp text-sm"></i> CHECK DP & REAL NAME
                </a>
                <a id="waWeb" href="#" target="_blank" class="bg-cyan-950/40 hover:bg-cyan-900/60 text-cyan-400 border border-cyan-500/40 py-3 rounded font-bold text-center text-xs transition-all cyber-font flex items-center justify-center gap-2 shadow-[0_0_10px_rgba(0,240,255,0.1)]">
                    <i class="fa-solid fa-network-wired text-sm"></i> EXTRACT METADATA
                </a>
            </div>
            
            <!-- Warning Banner Note System -->
            <div class="p-3 bg-red-950/30 border border-red-500/30 rounded text-[11px] text-red-400 leading-relaxed">
                <i class="fa-solid fa-triangle-exclamation animate-pulse"></i> <strong>CRITICAL NOTE:</strong> লিংকে ক্লিক করে কাস্টমারের চ্যাট প্যানেল ওপেন করুন। যদি সে প্রোফাইল নাম ও ছবি (DP) পাবলিক রেখে থাকে, তবে তা সাথে সাথেই দেখতে পাবেন। "Invalid Number" আসলে বুঝবেন নম্বরটি দিয়ে কোনো হোয়াটসঅ্যাপ খোলা হয়নি।
            </div>
        </div>

        <!-- Footer / Credits Section -->
        <div class="mt-8 border-t border-emerald-500/20 pt-3 text-center">
            <div class="text-[10px] tracking-widest text-gray-500 font-mono uppercase">
                SYSTEM DEVELOPED BY:
            </div>
            <div class="cyber-font font-black text-xs neon-text-cyan tracking-widest mt-0.5 animate-pulse">
                SHADOW JOKER
            </div>
        </div>

    </div>

    <!-- UI Logic Script Handling Module -->
    <script>
        function startInvestigation() {
            const phoneInput = document.getElementById('phoneNumber').value.trim();
            const loader = document.getElementById('loaderBox');
            const results = document.getElementById('resultBox');

            if (!phoneInput) {
                alert('CRITICAL_ERROR: Target number cannot be blank!');
                return;
            }

            // UI Reset States
            results.classList.add('hidden');
            loader.classList.remove('hidden');

            // Simulated Matrix Scanning Lag for UI Premium Feel
            setTimeout(() => {
                fetch(`/api/track?phone=${encodeURIComponent(phoneInput)}`)
                    .then(response => response.json())
                    .then(data => {
                        loader.classList.add('hidden');
                        if(data.status === "success") {
                            document.getElementById('resPhone').innerText = data.formatted_phone;
                            document.getElementById('waChat').href = data.links.click_to_chat;
                            document.getElementById('waWeb').href = data.links.web_wa_verify;
                            
                            results.classList.remove('hidden');
                        } else {
                            alert('OSINT_FAILED: ' + data.message);
                        }
                    })
                    .catch(err => {
                        loader.classList.add('hidden');
                        alert('NETWORK_CRASH: Server communication error.');
                    });
            }, 2000); // ২ সেকেন্ড হ্যাকার স্টাইল লোডিং অ্যানিমেশন চলবে
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
        "click_to_chat": f"https://wa.me/{clean_phone}",
        "web_wa_verify": f"https://web.whatsapp.com/send/?phone={clean_phone}&text&type=phone_number&app_absent=0"
    }

    return jsonify({
        "status": "success",
        "formatted_phone": "+" + clean_phone,
        "links": links
    })
