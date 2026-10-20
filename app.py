import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Block Blast", page_icon="🧩", layout="centered")

st.markdown(
    """
    <style>
    .block-container {padding-top: 1rem; padding-bottom: 0rem; max-width: 520px;}
    header, footer {visibility: hidden;}
    h1 {text-align: center; margin-bottom: 0;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🧩 Block Blast")
st.caption("Kéo thả khối vào bảng 8×8. Lấp đầy hàng hoặc cột để xóa và ghi điểm!")

GAME_HTML = r"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=no">
<style>
*{box-sizing:border-box}
html,body{margin:0;background:transparent;color:#fff;font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;
  -webkit-user-select:none;user-select:none;touch-action:none;overflow:hidden}
#app{max-width:440px;margin:0 auto;padding:6px 10px}
.top{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;gap:8px}
.box{background:#22264d;border-radius:12px;padding:6px 14px;text-align:center;min-width:92px}
.box small{display:block;font-size:10px;opacity:.7;letter-spacing:1.5px}
.box b{font-size:22px}
button.btn{background:#4a5bff;color:#fff;border:0;border-radius:12px;padding:10px 16px;font-size:14px;font-weight:600;cursor:pointer}
button.btn:active{transform:scale(.96)}
#board{display:grid;gap:var(--g);background:#2c3163;padding:var(--g);border-radius:12px;
  width:max-content;margin:0 auto;position:relative;
  grid-template-columns:repeat(8,var(--c));grid-template-rows:repeat(8,var(--c))}
.cell{width:var(--c);height:var(--c);background:#1a1d3d;border-radius:6px;transition:background .08s}
.cell.ghost{background:rgba(255,255,255,.35)!important}
.cell.flash{animation:flash .26s ease-out forwards}
@keyframes flash{0%{transform:scale(1);filter:brightness(1)}50%{transform:scale(1.12);filter:brightness(2.2)}100%{transform:scale(0);opacity:0}}
#tray{display:flex;justify-content:space-around;align-items:center;margin-top:14px;height:calc(var(--c)*3 + 24px)}
.slot{flex:1;height:100%;display:flex;justify-content:center;align-items:center;touch-action:none;cursor:grab}
.mini,.float{display:grid}
.float{position:fixed;z-index:99;pointer-events:none;filter:drop-shadow(0 6px 8px rgba(0,0,0,.45))}
.blk{border-radius:6px;box-shadow:inset 0 -3px 0 rgba(0,0,0,.25),inset 0 2px 0 rgba(255,255,255,.3)}
.toast{position:absolute;left:50%;top:38%;transform:translate(-50%,-50%);font-weight:800;font-size:26px;
  text-shadow:0 2px 6px #000;pointer-events:none;animation:rise .9s ease-out forwards;text-align:center;white-space:nowrap}
@keyframes rise{0%{opacity:0;transform:translate(-50%,-30%) scale(.6)}20%{opacity:1;transform:translate(-50%,-50%) scale(1.15)}100%{opacity:0;transform:translate(-50%,-140%) scale(1)}}
#over{position:fixed;inset:0;background:rgba(10,12,30,.85);display:none;flex-direction:column;align-items:center;justify-content:center;z-index:200;gap:10px}
#over h2{margin:0;font-size:32px}
#over p{margin:0;font-size:18px;opacity:.9}
</style>
</head>
<body>
<div id="app">
  <div class="top">
    <div class="box"><small>ĐIỂM</small><b id="score">0</b></div>
    <button class="btn" id="restart">🔄 Chơi lại</button>
    <div class="box"><small>KỶ LỤC</small><b id="best">0</b></div>
  </div>
  <div id="board"></div>
  <div id="tray"></div>
</div>
<div id="over">
  <h2>Hết nước đi!</h2>
  <p id="final"></p>
  <button class="btn" id="again">Chơi lại</button>
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

let board, pieces, score, best = 0, combo, busy = false, dragging = null;
let cs = 44, gap = 3;
const boardEl = document.getElementById('board');
const trayEl = document.getElementById('tray');
const cells = [];

try { best = parseInt(localStorage.getItem('blockblast_best') || '0') || 0; } catch (e) {}

function layout(){
  const avail = Math.min(window.innerWidth, 440) - 20 - 6;
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
    if (set.has(r + ',' + c)) { d.className = 'blk'; d.style.background = COLORS[p.color]; }
    el.appendChild(d);
  }
  return el;
}

function render(){
  for (let r = 0; r < N; r++) for (let c = 0; c < N; c++) {
    const el = cells[r*N + c], v = board[r][c];
    el.className = 'cell' + (v ? ' blk' : '');
    el.style.background = v ? COLORS[v] : '';
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
  document.getElementById('score').textContent = score;
  document.getElementById('best').textContent = best;
}

function toast(text){
  const t = document.createElement('div');
  t.className = 'toast';
  t.innerHTML = text;
  boardEl.appendChild(t);
  setTimeout(() => t.remove(), 900);
}

function clearGhost(){ cells.forEach(el => el.classList.remove('ghost')); }

function startDrag(e, idx){
  if (busy || !pieces[idx]) return;
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
  d.c = Math.round((left - br.left - gap) / step);
  d.r = Math.round((top - br.top - gap) / step);
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

  if (lines) {
    combo++;
    const bonus = 10 * lines * lines + (combo > 1 ? 10 * combo : 0);
    gain += bonus;
    rows.forEach(rr => { for (let cc = 0; cc < N; cc++) cells[rr*N + cc].classList.add('flash'); });
    cols.forEach(cc => { for (let rr = 0; rr < N; rr++) cells[rr*N + cc].classList.add('flash'); });
    toast('+' + bonus + (combo > 1 ? '<br><span style="font-size:18px">Combo x' + combo + '🔥</span>' : ''));
    setTimeout(() => {
      rows.forEach(rr => board[rr].fill(0));
      cols.forEach(cc => board.forEach(row => row[cc] = 0));
      finish();
    }, 260);
  } else {
    combo = 0;
    finish();
  }
  score += gain;
  if (score > best) {
    best = score;
    try { localStorage.setItem('blockblast_best', best); } catch (e) {}
  }
  document.getElementById('score').textContent = score;
  document.getElementById('best').textContent = best;
}

function finish(){
  if (pieces.every(x => !x)) deal();
  render();
  busy = false;
  if (!pieces.some(p => p && fitsAnywhere(p))) gameOver();
}

function gameOver(){
  document.getElementById('final').textContent = 'Điểm của bạn: ' + score + '  |  Kỷ lục: ' + best;
  document.getElementById('over').style.display = 'flex';
}

function newGame(){
  board = Array.from({length: N}, () => Array(N).fill(0));
  score = 0; combo = 0; busy = false;
  document.getElementById('over').style.display = 'none';
  deal();
  render();
}

document.getElementById('restart').addEventListener('click', newGame);
document.getElementById('again').addEventListener('click', newGame);
window.addEventListener('resize', () => { layout(); render(); });

layout();
buildBoard();
newGame();
</script>
</body>
</html>
"""

components.html(GAME_HTML, height=700, scrolling=False)
