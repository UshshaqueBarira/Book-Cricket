import streamlit as st
import streamlit.components.v1 as components
import time

# Configure page settings for full width
st.set_page_config(
    page_title="Nostalgia Book Cricket", page_icon="📖", layout="wide"
)

# Hide Streamlit UI chrome
st.markdown(
    """
    <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        .block-container {
            padding: 0px !important;
            margin: 0px !important;
            max-width: 100% !important;
            overflow: hidden;
        }
    </style>
""",
    unsafe_allow_html=True,
)

# Unique timestamp to prevent browser component caching
version_id = int(time.time())

html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nostalgia Book Cricket</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;900&display=swap" rel="stylesheet">
    <style>
        * { box-sizing: border-box; }
        body {
            font-family: 'Poppins', sans-serif;
            background: radial-gradient(circle at center, #0f172a 0%, #020617 100%);
            min-height: 100vh;
            width: 100vw;
            margin: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: space-between;
            padding: 1.2rem;
            color: white;
            overflow-x: hidden;
        }
        .perspective-container {
            perspective: 1400px;
        }
        .book {
            width: 280px;
            height: 180px;
            position: relative;
            transform-style: preserve-3d;
            transition: transform 0.6s ease;
        }
        .page {
            position: absolute;
            width: 100%;
            height: 100%;
            background: var(--book-bg, #fffdf9);
            border-radius: 6px 16px 16px 6px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.5);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            color: var(--book-text, #1e3a8a);
            transform-origin: left center;
            transition: transform 0.8s cubic-bezier(0.645, 0.045, 0.355, 1);
            backface-visibility: hidden;
            border-left: 6px solid rgba(0,0,0,0.15);
        }
        .flipping {
            transform: rotateY(-180deg);
        }
        @keyframes popIn {
            0% { transform: scale(0.2); opacity: 0; }
            70% { transform: scale(1.15); opacity: 1; }
            100% { transform: scale(1); opacity: 1; }
        }
        .animate-pop {
            animation: popIn 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
        }
        @keyframes confettiDrop {
            0% { transform: translateY(-20px) rotate(0deg); opacity: 1; }
            100% { transform: translateY(500px) rotate(720deg); opacity: 0; }
        }
        .confetti {
            position: absolute;
            width: 10px;
            height: 10px;
            background-color: #facc15;
            animation: confettiDrop 2.5s linear infinite;
        }
    </style>
</head>
<body>

    <!-- Header -->
    <header class="text-center">
        <h1 class="text-2xl md:text-3xl font-black tracking-wider text-yellow-300 drop-shadow-[0_4px_10px_rgba(234,179,8,0.4)]">📖 Childhood Book Cricket Championship</h1>
        <p class="text-xs text-blue-200 mt-0.5">Multiplayer Nostalgia • Sound FX • Out Rules • Winning Celebrations</p>
    </header>

    <!-- Top Stats / Leaderboard Bar -->
    <div id="top-stats-bar" class="w-full max-w-4xl flex flex-wrap justify-center gap-3 hidden"></div>

    <!-- Centered Main Game Arena -->
    <main class="w-full max-w-lg bg-slate-800/50 backdrop-blur-xl rounded-3xl p-5 md:p-6 shadow-2xl border border-slate-700/60 flex flex-col items-center justify-center relative my-2">
        
        <!-- SETUP SCREEN -->
        <div id="setup-screen" class="w-full">
            <h2 class="text-xl font-bold mb-3 text-center text-yellow-300">⚙️ Match Settings</h2>
            <div class="space-y-3 text-sm">
                <div>
                    <label class="block text-xs font-semibold mb-1 text-slate-300">Select Book Theme:</label>
                    <select id="book-theme" class="w-full p-2.5 rounded-xl bg-slate-900/90 border border-slate-600 text-white font-semibold focus:outline-none focus:ring-2 focus:ring-yellow-400">
                        <option value="math">📐 Math Textbook (Balanced)</option>
                        <option value="comic">🦸‍♂️ Comic Book (High Action)</option>
                        <option value="novel">📚 Classic Novel (Vintage Vibe)</option>
                    </select>
                </div>

                <div>
                    <label class="block text-xs font-semibold mb-1 text-slate-300">Classic "OUT" Rule (If page ends in 0):</label>
                    <select id="out-rule" class="w-full p-2.5 rounded-xl bg-slate-900/90 border border-slate-600 text-white font-semibold focus:outline-none focus:ring-2 focus:ring-yellow-400">
                        <option value="off">Disabled (Runs = 0)</option>
                        <option value="on">Enabled (Player is OUT! Score freezes)</option>
                    </select>
                </div>

                <div>
                    <label class="block text-xs font-semibold mb-1 text-slate-300">Number of Players (2 to 4):</label>
                    <select id="num-players" class="w-full p-2.5 rounded-xl bg-slate-900/90 border border-slate-600 text-white font-semibold focus:outline-none focus:ring-2 focus:ring-yellow-400" onchange="renderPlayerInputs()">
                        <option value="2">2 Players</option>
                        <option value="3">3 Players</option>
                        <option value="4">4 Players</option>
                    </select>
                </div>
                
                <div id="player-inputs-container" class="space-y-2"></div>

                <div>
                    <label class="block text-xs font-semibold mb-1 text-slate-300">Rounds per Player: <span id="round-val" class="font-bold text-yellow-300">10</span></label>
                    <input type="range" id="num-rounds" min="10" max="20" value="10" class="w-full accent-yellow-400 cursor-pointer" oninput="document.getElementById('round-val').textContent=this.value">
                </div>

                <button onclick="startMatch()" class="w-full py-3.5 mt-2 bg-gradient-to-r from-yellow-400 to-amber-500 hover:from-yellow-500 hover:to-amber-600 text-slate-950 font-black text-base rounded-2xl shadow-xl transition transform active:scale-95">
                    Start Match 🚀
                </button>
            </div>
        </div>

        <!-- PLAYING SCREEN -->
        <div id="game-screen" class="w-full flex flex-col items-center justify-center hidden">
            <div class="flex justify-between w-full mb-3 px-2 text-xs font-bold text-blue-200">
                <span id="round-indicator" class="bg-slate-900/80 px-3 py-1 rounded-xl border border-slate-700">Round 1 / 10</span>
                <span id="turn-indicator" class="text-yellow-300 bg-slate-900/80 px-3.5 py-1 rounded-xl border border-slate-700">Player's Turn</span>
            </div>

            <!-- 3D Book Animation Container -->
            <div class="perspective-container my-4">
                <div id="book-element" class="book">
                    <div class="page text-xl shadow-2xl" id="book-page-front">
                        <span class="text-[10px] uppercase tracking-widest opacity-60 mb-1">Childhood Book</span>
                        <span>Flip Me!</span>
                    </div>
                </div>
            </div>

            <!-- Flip Button -->
            <button id="flip-btn" onclick="flipBook()" class="px-8 py-3 bg-gradient-to-r from-emerald-400 to-teal-500 hover:from-emerald-500 hover:to-teal-600 text-slate-950 font-black text-lg rounded-2xl shadow-2xl transition transform active:scale-95 tracking-wide">
                📖 Flip the Book!
            </button>

            <!-- Giant Number Popup Modal/Overlay -->
            <div id="score-overlay" class="absolute inset-0 bg-slate-950/95 backdrop-blur-lg flex flex-col items-center justify-center hidden z-50 rounded-3xl transition-opacity">
                <p class="text-slate-400 text-base mb-1" id="overlay-page-text">Page 247</p>
                <h2 class="text-8xl font-black text-yellow-400 animate-pop" id="overlay-runs">6</h2>
                <p class="text-2xl font-extrabold mt-2" id="overlay-msg">Runs Scored!</p>
            </div>
        </div>

        <!-- GAME OVER SCREEN -->
        <div id="game-over-screen" class="w-full text-center hidden relative overflow-hidden py-2">
            <!-- Confetti container -->
            <div id="confetti-box" class="absolute inset-0 pointer-events-none overflow-hidden"></div>
            
            <h2 class="text-2xl font-black text-yellow-300 mb-2 animate-bounce">🏆 CHAMPIONSHIP CELEBRATION! 🏆</h2>
            <div id="winner-banner" class="bg-gradient-to-r from-amber-500 to-yellow-400 text-slate-950 p-3 rounded-2xl font-black text-base mb-4 shadow-xl"></div>
            <div id="final-leaderboard" class="space-y-2 mb-4 text-left max-w-md mx-auto text-xs relative z-10"></div>
            <button onclick="resetMatch()" class="px-6 py-3 bg-white text-slate-900 font-extrabold rounded-xl shadow-lg hover:bg-yellow-300 transition text-sm relative z-10">
                🔄 Play Again
            </button>
        </div>

    </main>

    <!-- Footer -->
    <footer class="text-center text-[11px] text-slate-400">
        Nostalgia Book Cricket • Enjoy with friends & family!
    </footer>

    <script>
        const avatars = ["👦🏽", "🧑🏼", "👧🏾", "👩🏻"];
        const themes = {
            math: { bg: "#f8fafc", text: "#1e3a8a" },
            comic: { bg: "#fef08a", text: "#b45309" },
            novel: { bg: "#fef3c7", text: "#78350f" }
        };

        let game = {
            players: [],
            rounds: 10,
            currentRound: 1,
            turnIndex: 0,
            scores: {},
            outStatus: {},
            isFlipping: false,
            theme: 'math',
            outRule: false
        };

        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        function playSound(type) {
            if (audioCtx.state === 'suspended') audioCtx.resume();
            const now = audioCtx.currentTime;

            if (type === 'flip') {
                const osc = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
                osc.connect(gain); gain.connect(audioCtx.destination);
                osc.type = 'triangle';
                osc.frequency.setValueAtTime(150, now);
                osc.frequency.exponentialRampToValueAtTime(400, now + 0.15);
                gain.gain.setValueAtTime(0.3, now);
                gain.gain.exponentialRampToValueAtTime(0.01, now + 0.15);
                osc.start(now); osc.stop(now + 0.15);
            } else if (type === 'cheer') {
                const osc = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
                osc.connect(gain); gain.connect(audioCtx.destination);
                osc.type = 'sine';
                osc.frequency.setValueAtTime(300, now);
                osc.frequency.setValueAtTime(500, now + 0.1);
                osc.frequency.setValueAtTime(700, now + 0.2);
                gain.gain.setValueAtTime(0.4, now);
                gain.gain.exponentialRampToValueAtTime(0.01, now + 0.4);
                osc.start(now); osc.stop(now + 0.4);
            } else if (type === 'out') {
                const osc = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
                osc.connect(gain); gain.connect(audioCtx.destination);
                osc.type = 'sawtooth';
                osc.frequency.setValueAtTime(200, now);
                osc.frequency.exponentialRampToValueAtTime(80, now + 0.4);
                gain.gain.setValueAtTime(0.5, now);
                gain.gain.exponentialRampToValueAtTime(0.01, now + 0.4);
                osc.start(now); osc.stop(now + 0.4);
            } else if (type === 'victory') {
                for (let i = 0; i < 15; i++) {
                    setTimeout(() => {
                        if (audioCtx.state === 'suspended') return;
                        const whiteNoise = audioCtx.createBufferSource();
                        const bufferSize = audioCtx.sampleRate * 0.3;
                        const buffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
                        const output = buffer.getChannelData(0);
                        for (let j = 0; j < bufferSize; j++) {
                            output[j] = Math.random() * 2 - 1;
                        }
                        whiteNoise.buffer = buffer;
                        const filter = audioCtx.createBiquadFilter();
                        filter.type = 'bandpass';
                        filter.frequency.value = 1000 + Math.random() * 500;
                        
                        const gainNode = audioCtx.createGain();
                        gainNode.gain.setValueAtTime(0.15, audioCtx.currentTime);
                        gainNode.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.3);

                        whiteNoise.connect(filter);
                        filter.connect(gainNode);
                        gainNode.connect(audioCtx.destination);
                        whiteNoise.start();
                    }, i * 150);
                }

                [400, 550, 700, 850].forEach((freq, idx) => {
                    setTimeout(() => {
                        const osc = audioCtx.createOscillator();
                        const gain = audioCtx.createGain();
                        osc.connect(gain); gain.connect(audioCtx.destination);
                        osc.type = 'sine';
                        osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
                        gain.gain.setValueAtTime(0.3, audioCtx.currentTime);
                        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.8);
                        osc.start(); osc.stop(audioCtx.currentTime + 0.8);
                    }, idx * 120);
                });
            }
        }

        function renderPlayerInputs() {
            const count = parseInt(document.getElementById('num-players').value);
            const container = document.getElementById('player-inputs-container');
            container.innerHTML = '';
            for (let i = 0; i < count; i++) {
                container.innerHTML += `
                    <div>
                        <label class="block text-[11px] font-semibold mb-0.5 text-slate-300">Player ${i+1} Name:</label>
                        <input type="text" id="p-name-${i}" value="Player ${i+1}" class="w-full p-2.5 rounded-xl bg-slate-900/90 border border-slate-600 text-white font-semibold text-xs focus:outline-none focus:ring-2 focus:ring-yellow-400">
                    </div>
                `;
            }
        }

        renderPlayerInputs();

        function startMatch() {
            const count = parseInt(document.getElementById('num-players').value);
            game.rounds = parseInt(document.getElementById('num-rounds').value);
            game.theme = document.getElementById('book-theme').value;
            game.outRule = document.getElementById('out-rule').value === 'on';
            
            game.players = [];
            game.scores = {};
            game.outStatus = {};

            const tConfig = themes[game.theme];
            document.documentElement.style.setProperty('--book-bg', tConfig.bg);
            document.documentElement.style.setProperty('--book-text', tConfig.text);

            for (let i = 0; i < count; i++) {
                const inputEl = document.getElementById(`p-name-${i}`);
                const name = inputEl ? inputEl.value.trim() || `Player ${i+1}` : `Player ${i+1}`;
                game.players.push(name);
                game.scores[name] = [];
                game.outStatus[name] = false;
            }

            game.currentRound = 1;
            game.turnIndex = 0;

            document.getElementById('setup-screen').classList.add('hidden');
            document.getElementById('game-screen').classList.remove('hidden');
            document.getElementById('top-stats-bar').classList.remove('hidden');
            updateTopBar();
        }

        function updateTopBar() {
            const activePlayer = game.players[game.turnIndex];
            document.getElementById('round-indicator').textContent = `Round ${game.currentRound} / ${game.rounds}`;
            document.getElementById('turn-indicator').textContent = game.outStatus[activePlayer] ? `${activePlayer} is OUT!` : `${activePlayer}'s Turn!`;

            let html = '';
            game.players.forEach((name, idx) => {
                const runsArr = game.scores[name] || [];
                const totalRuns = runsArr.reduce((a, b) => a + b, 0);
                const isCurrent = idx === game.turnIndex;
                const emoji = avatars[idx % avatars.length];
                const isOut = game.outStatus[name];
                
                html += `
                    <div class="bg-slate-800/90 px-3.5 py-2 rounded-2xl border-2 ${isCurrent ? 'border-yellow-300 shadow-md shadow-yellow-500/30' : 'border-slate-700 opacity-80'} flex items-center gap-2.5">
                        <span class="text-xl">${emoji}</span>
                        <div>
                            <p class="font-bold text-xs text-white">${name} ${isOut ? '❌' : ''}</p>
                            <p class="text-yellow-300 text-xs font-black">Total: ${totalRuns} runs</p>
                        </div>
                    </div>
                `;
            });
            document.getElementById('top-stats-bar').innerHTML = html;
        }

        function flipBook() {
            if (game.isFlipping) return;
            const activePlayer = game.players[game.turnIndex];

            if (game.outStatus[activePlayer]) {
                nextTurn();
                return;
            }

            game.isFlipping = true;
            playSound('flip');
            
            const bookEl = document.getElementById('book-element');
            bookEl.classList.add('flipping');

            setTimeout(() => {
                const pageNum = Math.floor(Math.random() * 450) + 1;
                let runs = pageNum % 10;
                let isOut = false;

                if (game.outRule && pageNum % 10 === 0) {
                    isOut = true;
                    runs = 0;
                    game.outStatus[activePlayer] = true;
                    playSound('out');
                } else {
                    if (runs > 6) runs = runs % 7;
                    game.scores[activePlayer].push(runs);
                    if (runs >= 4) playSound('cheer');
                }

                document.getElementById('overlay-page-text').textContent = `Page Number: ${pageNum}`;
                const runsEl = document.getElementById('overlay-runs');
                const msgEl = document.getElementById('overlay-msg');

                if (isOut) {
                    runsEl.textContent = "OUT!";
                    runsEl.className = "text-5xl font-black text-red-500 animate-pop";
                    msgEl.textContent = "Hit a 0-ending page! Innings closed.";
                    msgEl.className = "text-lg font-bold text-red-400 mt-2";
                } else {
                    runsEl.textContent = runs;
                    runsEl.className = "text-8xl font-black text-yellow-400 animate-pop";
                    msgEl.textContent = `${runs} Runs Scored!`;
                    msgEl.className = "text-xl font-bold text-emerald-400 mt-2";
                }

                document.getElementById('score-overlay').classList.remove('hidden');

                setTimeout(() => {
                    document.getElementById('score-overlay').classList.add('hidden');
                    bookEl.classList.remove('flipping');
                    nextTurn();
                }, 2000);

            }, 400);
        }

        function nextTurn() {
            game.turnIndex++;
            if (game.turnIndex >= game.players.length) {
                game.turnIndex = 0;
                game.currentRound++;
            }

            const allOut = game.players.every(name => game.outStatus[name]);
            if (game.currentRound > game.rounds || allOut) {
                showGameOver();
            } else {
                updateTopBar();
                game.isFlipping = false;
            }
        }

        function showGameOver() {
            document.getElementById('game-screen').classList.add('hidden');
            document.getElementById('top-stats-bar').classList.add('hidden');
            document.getElementById('game-over-screen').classList.remove('hidden');

            playSound('victory');

            const confettiBox = document.getElementById('confetti-box');
            confettiBox.innerHTML = '';
            for (let i = 0; i < 35; i++) {
                const conf = document.createElement('div');
                conf.className = 'confetti';
                conf.style.left = `${Math.random() * 100}%`;
                conf.style.backgroundColor = ['#facc15', '#4ade80', '#60a5fa', '#f472b6', '#fb923c'][Math.floor(Math.random() * 5)];
                conf.style.animationDelay = `${Math.random() * 1.5}s`;
                confettiBox.appendChild(conf);
            }

            let totals = game.players.map(name => ({
                name,
                total: game.scores[name].reduce((a, b) => a + b, 0)
            }));

            totals.sort((a, b) => b.total - a.total);

            document.getElementById('winner-banner').textContent = `🥇 Champion: ${totals[0].name} with a massive ${totals[0].total} runs!`;

            let finalHTML = '';
            totals.forEach((p, idx) => {
                finalHTML += `
                    <div class="bg-slate-900/90 p-2.5 rounded-xl flex justify-between items-center font-bold text-xs border border-slate-700">
                        <span>#${idx + 1} ${p.name}</span>
                        <span class="text-yellow-400 text-sm">${p.total} runs</span>
                    </div>
                `;
            });
            document.getElementById('final-leaderboard').innerHTML = finalHTML;
        }

        function resetMatch() {
            document.getElementById('game-over-screen').classList.add('hidden');
            document.getElementById('setup-screen').classList.remove('hidden');
            renderPlayerInputs();
        }
    </script>
</body>
</html>
"""

# Render component filling the viewport neatly
components.html(html_code, height=750, scrolling=False)