import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Block Blast", page_icon="🧩", layout="centered")

st.markdown(
    """
    <style>
    .stApp {background: #070914;}
    .block-container {padding: 0.5rem 0 0 0; max-width: 520px;}
    header, footer, #MainMenu {visibility: hidden; height: 0;}
    iframe {border: 0 !important; border-radius: 28px;}
    </style>
    """,
    unsafe_allow_html=True,
)

GAME_HTML = r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=no">
<style>
*{box-sizing:border-box}
:root{
  --glass-bg:linear-gradient(135deg,rgba(255,255,255,.20),rgba(255,255,255,.05));
  --glass-border:rgba(255,255,255,.24);
}
html,body{margin:0;height:100%;color:#fff;font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
  -webkit-user-select:none;user-select:none;touch-action:none;overflow:hidden;background:#0a0c1f}

/* ---------- Nền động ---------- */
#bg{position:fixed;inset:0;overflow:hidden;background:
  radial-gradient(120% 90% at 10% 0%,#1c1f5e 0%,transparent 60%),
  radial-gradient(100% 80% at 100% 100%,#3a1160 0%,transparent 60%),#090b1f}
.orb{position:absolute;border-radius:50%;filter:blur(55px);opacity:.75;animation:float 14s ease-in-out infinite}
.o1{width:260px;height:260px;background:#3e6bff;left:-70px;top:40px}
.o2{width:240px;height:240px;background:#c04bff;right:-80px;top:260px;animation-delay:-4s}
.o3{width:220px;height:220px;background:#19d5c0;left:30%;bottom:-80px;animation-delay:-8s}
.o4{width:150px;height:150px;background:#ff5d8f;right:10%;top:-40px;animation-delay:-2s}
@keyframes float{0%,100%{transform:translate(0,0) scale(1)}33%{transform:translate(30px,-26px) scale(1.12)}66%{transform:translate(-26px,24px) scale(.92)}}

/* ---------- Liquid glass ---------- */
.glass{position:relative;background:var(--glass-bg);
  -webkit-backdrop-filter:blur(20px) saturate(190%);backdrop-filter:blur(20px) saturate(190%);
  border:1px solid var(--glass-border);
  box-shadow:inset 0 1.5px 0 rgba(255,255,255,.55),inset 0 -1.5px 0 rgba(255,255,255,.08),
    inset 0 0 22px rgba(255,255,255,.06),0 14px 36px rgba(0,0,0,.38);overflow:hidden}
.glass::before{content:"";position:absolute;left:-20%;top:-60%;width:140%;height:100%;
  background:radial-gradient(ellipse at 50% 100%,rgba(255,255,255,.22),transparent 65%);pointer-events:none;border-radius:50%}
.glass::after{content:"";position:absolute;inset:0;border-radius:inherit;pointer-events:none;
  background:linear-gradient(115deg,transparent 35%,rgba(255,255,255,.10) 48%,transparent 60%);
  background-size:250% 100%;animation:sheen 7s linear infinite}
@keyframes sheen{0%{background-position:150% 0}100%{background-position:-100% 0}}

#app{position:relative;z-index:1;max-width:460px;margin:0 auto;padding:12px 12px 8px}
.top{display:grid;grid-template-columns:1fr auto 1fr;align-items:center;gap:10px;margin-bottom:12px}
.box{border-radius:18px;padding:7px 14px;text-align:center}
.box small{display:block;font-size:10px;opacity:.75;letter-spacing:2px;font-weight:600}
.box b{font-size:24px;font-weight:800;display:inline-block;letter-spacing:.5px}
.box b.pop{animation:pop .3s ease-out}
@keyframes pop{0%{transform:scale(1)}40%{transform:scale(1.25)}100%{transform:scale(1)}}
.round{width:52px;height:52px;border-radius:50%;display:flex;align-items:center;justify-content:center;
  font-size:20px;cursor:pointer;color:#fff;padding:0}
.round:active{transform:scale(.92)}

#frame{border-radius:24px;padding:10px;width:max-content;margin:0 auto}
#board{display:grid;gap:var(--g);width:max-content;position:relative;
  grid-template-columns:repeat(8,var(--c));grid-template-rows:repeat(8,var(--c))}
.cell{width:var(--c);height:var(--c);border-radius:8px;background:rgba(255,255,255,.07);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.10),inset 0 -2px 4px rgba(0,0,0,.25);transition:background .08s}
.cell.ghost{background:rgba(255,255,255,.42)!important;box-shadow:0 0 14px rgba(255,255,255,.5),inset 0 1px 0 rgba(255,255,255,.6)}
.cell.flash{animation:flash .28s ease-out forwards}
.cell.drop{animation:drop .22s ease-out}
@keyframes drop{0%{transform:scale(1.25)}100%{transform:scale(1)}}
@keyframes flash{0%{transform:scale(1);filter:brightness(1)}50%{transform:scale(1.14);filter:brightness(2.4)}100%{transform:scale(0);opacity:0}}
.blk{border-radius:8px;box-shadow:inset 0 2px 1px rgba(255,255,255,.6),inset 0 -4px 5px rgba(0,0,0,.28),0 2px 6px rgba(0,0,0,.3)}

#tray{display:flex;justify-content:space-around;align-items:center;margin-top:14px;border-radius:24px;
  height:calc(var(--c)*3 + 30px);padding:6px}
.slot{flex:1;height:100%;display:flex;justify-content:center;align-items:center;touch-action:none;cursor:grab;position:relative;z-index:1}
.slot > .mini{transition:transform .15s}
.slot:hover > .mini{transform:scale(1.07)}
.mini,.float{display:grid}
.float{position:fixed;z-index:99;pointer-events:none;filter:drop-shadow(0 10px 12px rgba(0,0,0,.5))}

.toast{position:absolute;left:50%;top:38%;transform:translate(-50%,-50%);font-weight:900;font-size:30px;
  text-shadow:0 2px 10px rgba(0,0,0,.8),0 0 24px rgba(120,160,255,.9);pointer-events:none;
  animation:rise 1s ease-out forwards;text-align:center;white-space:nowrap;z-index:5}
@keyframes rise{0%{opacity:0;transform:translate(-50%,-30%) scale(.6)}20%{opacity:1;transform:translate(-50%,-50%) scale(1.15)}100%{opacity:0;transform:translate(-50%,-150%) scale(1)}}

/* ---------- Nút ---------- */
.btn{position:relative;display:block;width:100%;border:1px solid rgba(255,255,255,.3);border-radius:18px;padding:14px 18px;
  font-size:16px;font-weight:700;color:#fff;cursor:pointer;margin-top:12px;letter-spacing:.3px;
  background:linear-gradient(135deg,rgba(255,255,255,.22),rgba(255,255,255,.06));
  -webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px);
  box-shadow:inset 0 1.5px 0 rgba(255,255,255,.55),0 8px 20px rgba(0,0,0,.3);transition:transform .12s,filter .12s}
.btn:hover{filter:brightness(1.18)}
.btn:active{transform:scale(.97)}
.btn.primary{background:linear-gradient(135deg,rgba(90,120,255,.85),rgba(170,80,255,.75));
  border-color:rgba(255,255,255,.45);font-size:18px;padding:16px 18px;box-shadow:inset 0 1.5px 0 rgba(255,255,255,.7),0 10px 28px rgba(110,90,255,.55)}
.row2{display:flex;gap:10px}
.row2 .btn{margin-top:12px}

/* ---------- Lớp phủ / menu ---------- */
.screen{position:fixed;inset:0;z-index:150;display:none;align-items:center;justify-content:center;padding:18px;
  background:rgba(8,10,28,.35);-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px)}
.screen.show{display:flex;animation:fade .3s ease-out}
@keyframes fade{from{opacity:0}to{opacity:1}}
.card{width:100%;max-width:370px;border-radius:32px;padding:26px 22px 22px;text-align:center;animation:cardin .45s cubic-bezier(.2,1.2,.4,1)}
@keyframes cardin{from{opacity:0;transform:translateY(26px) scale(.94)}to{opacity:1;transform:none}}
.card > *{position:relative;z-index:1}
.logo{display:grid;grid-template-columns:repeat(4,30px);gap:4px;justify-content:center;margin:0 auto 14px;animation:bob 3.6s ease-in-out infinite}
@keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}
.logo i{width:30px;height:30px;border-radius:9px;display:block}
.title{margin:0;font-size:38px;font-weight:900;letter-spacing:1px;line-height:1;
  background:linear-gradient(90deg,#8fd3ff,#c8a2ff,#ff9ac8,#ffd27a);-webkit-background-clip:text;background-clip:text;color:transparent;
  filter:drop-shadow(0 4px 14px rgba(150,130,255,.5))}
.sub{margin:8px 0 6px;font-size:13px;opacity:.8;letter-spacing:.5px}
.bestline{display:inline-block;margin:10px 0 4px;padding:6px 16px;border-radius:999px;font-size:13px;font-weight:700}
.snd{margin-top:14px;font-size:13px;opacity:.85;cursor:pointer;display:inline-block;padding:6px 12px;border-radius:12px}
.snd:hover{background:rgba(255,255,255,.1)}
h2.h{margin:0 0 4px;font-size:28px;font-weight:900}
#final{margin:6px 0 2px;font-size:16px;opacity:.95;line-height:1.6}
#final b{font-size:36px;display:block;margin:4px 0}

/* ---------- Hướng dẫn ---------- */
.slide{display:none;animation:fade .35s}
.slide.on{display:block}
.slide h3{margin:12px 0 6px;font-size:22px}
.slide p{margin:0;font-size:14px;line-height:1.55;opacity:.9;min-height:66px}
.demo{height:150px;display:flex;align-items:center;justify-content:center;border-radius:20px;margin-top:4px;
  background:rgba(0,0,0,.22);box-shadow:inset 0 2px 8px rgba(0,0,0,.4)}
.mg{display:grid;gap:3px;position:relative}
.mg i{width:28px;height:28px;border-radius:7px;background:rgba(255,255,255,.08);display:block}
.mg i.x{box-shadow:inset 0 2px 1px rgba(255,255,255,.55),inset 0 -3px 4px rgba(0,0,0,.28)}
.c1{background:linear-gradient(145deg,#ff9aa9,#ff5d73 55%,#c93a52)}
.c2{background:linear-gradient(145deg,#8fe4ff,#3ec5ff 55%,#2088c4)}
.c3{background:linear-gradient(145deg,#a8ffd0,#4cd98a 55%,#2c9d62)}
.c4{background:linear-gradient(145deg,#d6a8ff,#9b6bff 55%,#6a3fc0)}
.mg i.g{animation:mg 2.6s infinite}
.mg i.r{animation:mr 2.6s infinite}
.mg i.g.r{animation:mg 2.6s infinite,mr 2.6s infinite}
@keyframes mg{0%,30%{background:rgba(255,255,255,.4);box-shadow:0 0 12px rgba(255,255,255,.6)}36%,100%{background:linear-gradient(145deg,#8fe4ff,#3ec5ff 55%,#2088c4)}}
@keyframes mr{0%,62%{transform:scale(1);opacity:1;filter:brightness(1)}74%{transform:scale(1.15);filter:brightness(2.2)}88%,100%{transform:scale(0);opacity:0}}
.pc{position:absolute;display:grid;grid-template-columns:repeat(2,28px);gap:3px;animation:dm 2.8s ease-in-out infinite;
  filter:drop-shadow(0 8px 8px rgba(0,0,0,.5))}
.pc i{background:linear-gradient(145deg,#ffe58a,#ffd93d 55%,#d1a40a)!important;opacity:1!important}
@keyframes dm{0%{transform:translate(100px,60px);opacity:0}15%{opacity:1}60%,85%{transform:translate(0,0);opacity:1}100%{transform:translate(0,0);opacity:0}}
.tbl{display:grid;gap:6px;width:80%;font-size:14px}
.tbl div{display:flex;justify-content:space-between;padding:6px 12px;border-radius:12px;background:rgba(255,255,255,.1)}
.tbl b{color:#ffd93d}
.dots{display:flex;justify-content:center;gap:7px;margin:12px 0 2px}
.dots span{width:8px;height:8px;border-radius:50%;background:rgba(255,255,255,.3);transition:.2s}
.dots span.on{background:#fff;width:22px;border-radius:6px}
.navrow{display:flex;gap:10px}
.navrow .btn{margin-top:10px;padding:12px}
</style>
</head>
<body>
<div id="bg"><div class="orb o1"></div><div class="orb o2"></div><div class="orb o3"></div><div class="orb o4"></div></div>

<div id="app">
  <div class="top">
    <div class="box glass"><small>ĐIỂM</small><b id="score">0</b></div>
    <button class="round glass" id="pauseBtn" title="Tạm dừng">⏸</button>
    <div class="box glass"><small>KỶ LỤC</small><b id="best">0</b></div>
  </div>
  <div id="frame" class="glass"><div id="board"></div></div>
  <div id="tray" class="glass"></div>
</div>

<!-- MENU CHÍNH -->
<div class="screen show" id="menu">
  <div class="card glass">
    <div class="logo" id="logo"></div>
    <h1 class="title">BLOCK BLAST</h1>
    <div class="sub">Xếp khối · Xóa hàng · Phá kỷ lục</div>
    <div class="bestline glass">🏆 Kỷ lục: <span id="menuBest">0</span></div>
    <button class="btn primary" id="playBtn">▶  Chơi ngay</button>
    <button class="btn" id="resumeBtn" style="display:none">⏯  Tiếp tục ván đang chơi</button>
    <button class="btn" id="howBtn">📖  Hướng dẫn</button>
    <div class="snd" id="sndBtn">🔊 Âm thanh: Bật</div>
  </div>
</div>

<!-- TẠM DỪNG -->
<div class="screen" id="pause">
  <div class="card glass">
    <h2 class="h">⏸ Tạm dừng</h2>
    <div class="sub">Điểm hiện tại: <b id="pauseScore">0</b></div>
    <button class="btn primary" id="pResume">▶  Tiếp tục</button>
    <div class="row2">
      <button class="btn" id="pRestart">🔄 Chơi lại</button>
      <button class="btn" id="pHow">📖 Hướng dẫn</button>
    </div>
    <button class="btn" id="pHome">🏠  Về menu chính</button>
  </div>
</div>

<!-- HƯỚNG DẪN -->
<div class="screen" id="how">
  <div class="card glass">
    <div id="slides"></div>
    <div class="dots" id="dots"></div>
    <div class="navrow">
      <button class="btn" id="hPrev">‹ Trước</button>
      <button class="btn primary" id="hNext" style="font-size:16px">Tiếp ›</button>
    </div>
  </div>
</div>

<!-- HẾT NƯỚC ĐI -->
<div class="screen" id="over">
  <div class="card glass">
    <h2 class="h">Hết nước đi!</h2>
    <div id="final"></div>
    <div id="newrec" style="color:#ffd93d;font-weight:800;margin-top:4px"></div>
    <button class="btn primary" id="again">🔄  Chơi lại</button>
    <button class="btn" id="oHome">🏠  Về menu chính</button>
  </div>
</div>

<script>
const N = 8;
const COLORS = ['', '#ff5d73', '#ffa23a', '#ffd93d', '#4cd98a', '#3ec5ff', '#7a7bff', '#c86bff'];
const BASE = [
  [[0,0]],
  [[0,0],[0,1]],
  [[0,0],[0,1],[0,2]],
  [[0,0],[0,1],[0,2],[0,3]],
  [[0,0],[0,1],[0,2],[0,3],[0,4]],
  [[0,0],[0,1],[1,0],[1,1]],
  [[0,0],[0,1],[0,2],[1,0],[1,1],[1,2]],
  [[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2]],
  [[0,0],[1,0],[1,1]],
  [[0,0],[1,0],[2,0],[2,1],[2,2]],
  [[0,0],[0,1],[0,2],[1,1]],
  [[0,1],[0,2],[1,0],[1,1]],
  [[0,0],[0,1],[1,1],[1,2]],
  [[0,0],[1,0],[2,0],[2,1]],
  [[0,1],[1,1],[2,1],[2,0]]
];
function norm(s){
  const mr = Math.min(...s.map(x => x[0])), mc = Math.min(...s.map(x => x[1]));
  return s.map(([r,c]) => [r-mr, c-mc]).sort((a,b) => a[0]-b[0] || a[1]-b[1]);
}
function rot(s){ return norm(s.map(([r,c]) => [c, -r])); }
const SHAPES = [], seen = new Set();
BASE.forEach(b => {
  let s = norm(b);
  for (let i = 0; i < 4; i++) {
    const k = JSON.stringify(s);
    if (!seen.has(k)) { seen.add(k); SHAPES.push(s); }
    s = rot(s);
  }
});

/* ----- màu bóng kính ----- */
function mix(hex, t){ // t>0 trộn trắng, t<0 trộn đen
  const n = parseInt(hex.slice(1), 16);
  let r = n >> 16, g = (n >> 8) & 255, b = n & 255;
  const f = t >= 0 ? 255 : 0, a = Math.abs(t);
  r = Math.round(r + (f - r) * a); g = Math.round(g + (f - g) * a); b = Math.round(b + (f - b) * a);
  return `rgb(${r},${g},${b})`;
}
const GRAD = COLORS.map(c => c ? `linear-gradient(145deg,${mix(c,.45)} 0%,${c} 55%,${mix(c,-.3)} 100%)` : '');

let board, pieces, score, best = 0, combo, busy = false, dragging = null, inProgress = false;
let soundOn = true, cs = 44, gap = 3;
const boardEl = document.getElementById('board');
const trayEl = document.getElementById('tray');
const cells = [];
const $ = id => document.getElementById(id);

try { best = parseInt(localStorage.getItem('blockblast_best') || '0') || 0; } catch (e) {}
try { soundOn = localStorage.getItem('blockblast_sound') !== '0'; } catch (e) {}

/* ----- âm thanh ----- */
let actx = null;
function tone(freq, t0, dur, type, vol){
  const o = actx.createOscillator(), g = actx.createGain();
  o.type = type || 'sine'; o.frequency.value = freq;
  g.gain.setValueAtTime(vol || .12, actx.currentTime + t0);
  g.gain.exponentialRampToValueAtTime(.0001, actx.currentTime + t0 + dur);
  o.connect(g); g.connect(actx.destination);
  o.start(actx.currentTime + t0); o.stop(actx.currentTime + t0 + dur + .02);
}
function sfx(kind, n){
  if (!soundOn) return;
  try {
    actx = actx || new (window.AudioContext || window.webkitAudioContext)();
    if (actx.state === 'suspended') actx.resume();
    if (kind === 'place') { tone(320, 0, .12, 'triangle', .14); }
    else if (kind === 'clear') { for (let i = 0; i < 3 + Math.min(n, 3); i++) tone(520 * Math.pow(1.122, i * 2), i * .07, .2, 'sine', .13); }
    else if (kind === 'over') { [400, 330, 260, 190].forEach((f, i) => tone(f, i * .16, .3, 'sawtooth', .08)); }
    else if (kind === 'click') { tone(660, 0, .07, 'sine', .08); }
  } catch (e) {}
}

/* ----- bố cục ----- */
function layout(){
  const avail = Math.min(window.innerWidth, 460) - 24 - 20;
  cs = Math.max(26, Math.min(46, Math.floor((avail - 9*gap) / 8)));
  document.documentElement.style.setProperty('--c', cs + 'px');
  document.documentElement.style.setProperty('--g', gap + 'px');
}

function buildBoard(){
  boardEl.innerHTML = '';
  cells.length = 0;
  for (let i = 0; i < N*N; i++) {
    const d = document.createElement('div');
    d.className = 'cell';
    boardEl.appendChild(d);
    cells.push(d);
  }
}

function randPiece(){
  const cellsArr = SHAPES[Math.floor(Math.random() * SHAPES.length)];
  return {
    cells: cellsArr,
    color: 1 + Math.floor(Math.random() * 7),
    rows: Math.max(...cellsArr.map(x => x[0])) + 1,
    cols: Math.max(...cellsArr.map(x => x[1])) + 1
  };
}

function canPlace(shape, r, c){
  return shape.every(([dr,dc]) => {
    const rr = r + dr, cc = c + dc;
    return rr >= 0 && rr < N && cc >= 0 && cc < N && board[rr][cc] === 0;
  });
}
function fitsAnywhere(p){
  for (let r = 0; r < N; r++) for (let c = 0; c < N; c++) if (canPlace(p.cells, r, c)) return true;
  return false;
}

function deal(){
  let tries = 0, ps;
  do {
    ps = [randPiece(), randPiece(), randPiece()];
    tries++;
  } while (tries < 40 && !ps.some(fitsAnywhere));
  pieces = ps;
}

function pieceGrid(p, size, g, cls){
  const el = document.createElement('div');
  el.className = cls;
  el.style.gridTemplateColumns = `repeat(${p.cols}, ${size}px)`;
  el.style.gridTemplateRows = `repeat(${p.rows}, ${size}px)`;
  el.style.gap = g + 'px';
  const set = new Set(p.cells.map(x => x[0] + ',' + x[1]));
  for (let r = 0; r < p.rows; r++) for (let c = 0; c < p.cols; c++) {
    const d = document.createElement('div');
    if (set.has(r + ',' + c)) { d.className = 'blk'; d.style.background = GRAD[p.color]; }
    el.appendChild(d);
  }
  return el;
}

function render(){
  for (let r = 0; r < N; r++) for (let c = 0; c < N; c++) {
    const el = cells[r*N + c], v = board[r][c];
    el.className = 'cell' + (v ? ' blk' : '');
    el.style.background = v ? GRAD[v] : '';
  }
  trayEl.innerHTML = '';
  pieces.forEach((p, i) => {
    const slot = document.createElement('div');
    slot.className = 'slot';
    if (p) {
      slot.appendChild(pieceGrid(p, Math.round(cs * 0.6), 2, 'mini'));
      slot.addEventListener('pointerdown', e => startDrag(e, i));
    }
    trayEl.appendChild(slot);
  });
  $('score').textContent = score;
  $('best').textContent = best;
}

function popScore(){
  const s = $('score'); s.classList.remove('pop'); void s.offsetWidth; s.classList.add('pop');
}

function toast(text){
  const t = document.createElement('div');
  t.className = 'toast';
  t.innerHTML = text;
  boardEl.appendChild(t);
  setTimeout(() => t.remove(), 950);
}

function clearGhost(){ cells.forEach(el => el.classList.remove('ghost')); }

/* ----- kéo thả ----- */
function startDrag(e, idx){
  if (busy || !pieces[idx] || !inProgress) return;
  e.preventDefault();
  const p = pieces[idx];
  const el = pieceGrid(p, cs, gap, 'float');
  document.body.appendChild(el);
  dragging = {
    idx, el, p, valid: false, r: 0, c: 0,
    w: p.cols * cs + (p.cols - 1) * gap,
    h: p.rows * cs + (p.rows - 1) * gap
  };
  moveDrag(e);
  window.addEventListener('pointermove', moveDrag);
  window.addEventListener('pointerup', endDrag);
  window.addEventListener('pointercancel', endDrag);
}

function moveDrag(e){
  const d = dragging;
  if (!d) return;
  const lift = e.pointerType === 'mouse' ? 0 : 70;
  const left = e.clientX - d.w / 2, top = e.clientY - d.h / 2 - lift;
  d.el.style.left = left + 'px';
  d.el.style.top = top + 'px';
  const br = boardEl.getBoundingClientRect(), step = cs + gap;
  d.c = Math.round((left - br.left) / step);
  d.r = Math.round((top - br.top) / step);
  clearGhost();
  d.valid = canPlace(d.p.cells, d.r, d.c);
  if (d.valid) d.p.cells.forEach(([dr,dc]) => cells[(d.r+dr)*N + (d.c+dc)].classList.add('ghost'));
}

function endDrag(){
  const d = dragging;
  if (!d) return;
  window.removeEventListener('pointermove', moveDrag);
  window.removeEventListener('pointerup', endDrag);
  window.removeEventListener('pointercancel', endDrag);
  d.el.remove();
  clearGhost();
  dragging = null;
  if (d.valid) place(d.idx, d.r, d.c);
}

/* ----- đặt khối ----- */
function place(idx, r, c){
  busy = true;
  const p = pieces[idx];
  p.cells.forEach(([dr,dc]) => board[r+dr][c+dc] = p.color);
  let gain = p.cells.length;
  pieces[idx] = null;

  const rows = [], cols = [];
  for (let i = 0; i < N; i++) {
    if (board[i].every(v => v)) rows.push(i);
    if (board.every(row => row[i])) cols.push(i);
  }
  const lines = rows.length + cols.length;
  render();
  p.cells.forEach(([dr,dc]) => cells[(r+dr)*N + (c+dc)].classList.add('drop'));

  if (lines) {
    combo++;
    const bonus = 10 * lines * lines + (combo > 1 ? 10 * combo : 0);
    gain += bonus;
    sfx('clear', lines);
    rows.forEach(rr => { for (let cc = 0; cc < N; cc++) cells[rr*N + cc].classList.add('flash'); });
    cols.forEach(cc => { for (let rr = 0; rr < N; rr++) cells[rr*N + cc].classList.add('flash'); });
    toast('+' + bonus + (combo > 1 ? '<br><span style="font-size:18px">Combo x' + combo + ' 🔥</span>' : ''));
    setTimeout(() => {
      rows.forEach(rr => board[rr].fill(0));
      cols.forEach(cc => board.forEach(row => row[cc] = 0));
      finish();
    }, 280);
  } else {
    combo = 0;
    sfx('place');
    finish();
  }
  score += gain;
  if (score > best) {
    best = score;
    try { localStorage.setItem('blockblast_best', best); } catch (e) {}
  }
  $('score').textContent = score;
  $('best').textContent = best;
  popScore();
}

function finish(){
  if (pieces.every(x => !x)) deal();
  render();
  busy = false;
  if (!pieces.some(p => p && fitsAnywhere(p))) gameOver();
}

function gameOver(){
  inProgress = false;
  sfx('over');
  const isRecord = score > 0 && score >= best && score > startBest;
  $('final').innerHTML = 'Điểm của bạn<b>' + score + '</b>Kỷ lục: ' + best;
  $('newrec').textContent = isRecord ? '🎉 Kỷ lục mới!' : '';
  setTimeout(() => show('over'), 350);
}

let startBest = 0;
function newGame(){
  board = Array.from({length: N}, () => Array(N).fill(0));
  score = 0; combo = 0; busy = false; inProgress = true; startBest = best;
  deal();
  render();
}

/* ----- điều hướng màn hình ----- */
const screens = ['menu', 'pause', 'how', 'over'];
function show(name){
  screens.forEach(s => $(s).classList.toggle('show', s === name));
  if (name === 'menu') {
    $('menuBest').textContent = best;
    $('resumeBtn').style.display = inProgress ? 'block' : 'none';
  }
  if (name === 'pause') $('pauseScore').textContent = score;
}
function hideAll(){ screens.forEach(s => $(s).classList.remove('show')); }

let howFrom = 'menu';
function openHow(from){ howFrom = from; slideIdx = 0; renderSlides(); show('how'); }

function startPlay(){ sfx('click'); newGame(); hideAll(); }

$('playBtn').onclick = startPlay;
$('again').onclick = startPlay;
$('resumeBtn').onclick = () => { sfx('click'); hideAll(); };
$('howBtn').onclick = () => { sfx('click'); openHow('menu'); };
$('pauseBtn').onclick = () => { if (busy || dragging) return; sfx('click'); show('pause'); };
$('pResume').onclick = () => { sfx('click'); hideAll(); };
$('pRestart').onclick = startPlay;
$('pHow').onclick = () => { sfx('click'); openHow('pause'); };
$('pHome').onclick = () => { sfx('click'); show('menu'); };
$('oHome').onclick = () => { sfx('click'); show('menu'); };
function updSnd(){ $('sndBtn').textContent = '🔊 Âm thanh: ' + (soundOn ? 'Bật' : 'Tắt'); if(!soundOn) $('sndBtn').textContent = '🔇 Âm thanh: Tắt'; }
$('sndBtn').onclick = () => {
  soundOn = !soundOn; updSnd();
  try { localStorage.setItem('blockblast_sound', soundOn ? '1' : '0'); } catch (e) {}
  sfx('click');
};

/* ----- logo ----- */
(function(){
  const pat = [1,1,0,3, 1,0,5,5, 0,2,5,4, 6,2,2,4];
  const lg = $('logo');
  pat.forEach((v, i) => {
    const d = document.createElement('i');
    if (v) { d.className = 'blk'; d.style.background = GRAD[v]; d.style.animation = `bob ${2.6 + (i % 4) * .4}s ease-in-out ${(i % 5) * -.5}s infinite`; }
    lg.appendChild(d);
  });
})();

/* ----- hướng dẫn ----- */
function mg(rows, extra){
  let h = '<div class="mg" style="grid-template-columns:repeat(' + rows[0].length + ',28px)">';
  rows.forEach(r => [...r].forEach(ch => {
    const cls = { '.': '', 'x': 'x c1', 'y': 'x c3', 'z': 'x c4', 'g': 'g', 'G': 'g r', 'R': 'x c2 r' }[ch];
    h += '<i class="' + cls + '"></i>';
  }));
  return h + (extra || '') + '</div>';
}
const SLIDES = [
  { t: '1 · Kéo & thả khối', d: 'Chạm giữ một khối ở khay bên dưới rồi kéo vào bảng 8×8. Vùng sáng mờ cho biết vị trí sẽ đặt. Khối không được xoay!',
    demo: mg(['y....', 'y....', 'yz...', 'yz...'],
      '<div class="pc" style="left:62px;top:31px"><i></i><i></i><i></i><i></i></div>') },
  { t: '2 · Lấp đầy để xóa', d: 'Lấp kín một hàng ngang hoặc cột dọc để xóa nó và nhận điểm. Xóa nhiều đường cùng lúc sẽ nhận thưởng lớn hơn!',
    demo: mg(['.....', 'RRRRG', '.....', '.....']) },
  { t: '3 · Combo & điểm thưởng', d: 'Xóa hàng liên tiếp qua nhiều lượt đặt khối để tăng combo. Càng nhiều đường một lúc, điểm càng cao.',
    demo: '<div class="tbl"><div><span>1 đường</span><b>+10</b></div><div><span>2 đường</span><b>+40</b></div><div><span>3 đường</span><b>+90</b></div><div><span>Combo ×n</span><b>+10×n 🔥</b></div></div>' },
  { t: '4 · Mẹo chơi hay', d: 'Chừa chỗ cho khối dài, đừng để các ô trống rời rạc. Trò chơi kết thúc khi không khối nào còn đặt vừa. Chúc bạn phá kỷ lục!',
    demo: '<div style="font-size:54px;filter:drop-shadow(0 6px 14px rgba(255,200,80,.6))">🏆</div>' }
];
let slideIdx = 0;
function renderSlides(){
  $('slides').innerHTML = SLIDES.map((s, i) =>
    '<div class="slide' + (i === slideIdx ? ' on' : '') + '"><div class="demo">' + s.demo + '</div><h3>' + s.t + '</h3><p>' + s.d + '</p></div>'
  ).join('');
  $('dots').innerHTML = SLIDES.map((_, i) => '<span class="' + (i === slideIdx ? 'on' : '') + '"></span>').join('');
  $('hPrev').style.visibility = slideIdx === 0 ? 'hidden' : 'visible';
  $('hNext').textContent = slideIdx === SLIDES.length - 1 ? '✓ Đã hiểu' : 'Tiếp ›';
}
$('hPrev').onclick = () => { if (slideIdx > 0) { slideIdx--; sfx('click'); renderSlides(); } };
$('hNext').onclick = () => {
  sfx('click');
  if (slideIdx < SLIDES.length - 1) { slideIdx++; renderSlides(); }
  else show(howFrom);
};

window.addEventListener('resize', () => { layout(); if (board) render(); });

layout();
buildBoard();
newGame();
inProgress = false;   // chưa chơi cho tới khi bấm "Chơi ngay"
updSnd();
show('menu');
</script>
</body>
</html>
"""

components.html(GAME_HTML, height=760, scrolling=False)
