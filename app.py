<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Block Blast Clone</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #1a1a2e;
            color: #fff;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
            overflow: hidden;
        }
        h1 { margin: 5px 0; color: #e94560; font-size: 24px; }
        .score-board { font-size: 18px; margin-bottom: 10px; }
        
        /* Bảng lưới 8x8 */
        .grid {
            display: grid;
            grid-template-columns: repeat(8, 40px);
            grid-template-rows: repeat(8, 40px);
            gap: 3px;
            background-color: #16213e;
            padding: 6px;
            border-radius: 8px;
            box-shadow: 0 8px 16px rgba(0,0,0,0.3);
        }
        .cell {
            width: 40px;
            height: 40px;
            background-color: #0f3460;
            border-radius: 4px;
            transition: background-color 0.2s;
        }
        .cell.filled {
            background-color: #e94560;
        }

        /* Khay chứa khối bên dưới */
        .tray {
            display: flex;
            justify-content: space-around;
            align-items: center;
            width: 350px;
            margin-top: 20px;
            background: #16213e;
            padding: 15px;
            border-radius: 8px;
            min-height: 90px;
        }
        .block-container {
            display: grid;
            gap: 2px;
            cursor: grab;
            transform: scale(0.7);
            transform-origin: center;
        }
        .mini-cell {
            width: 30px;
            height: 30px;
            border-radius: 3px;
        }
        .mini-cell.filled {
            background-color: #0f3460;
        }
        .mini-cell.empty {
            background: transparent;
        }

        #game-over {
            display: none;
            position: absolute;
            top: 50%; left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0,0,0,0.9);
            padding: 30px;
            border-radius: 12px;
            text-align: center;
        }
        #game-over button {
            background: #e94560;
            border: none;
            color: white;
            padding: 10px 20px;
            font-size: 16px;
            border-radius: 5px;
            cursor: pointer;
            margin-top: 15px;
        }
    </style>
</head>
<body>

    <h1>BLOCK BLAST</h1>
    <div class="score-board">Điểm: <span id="score">0</span></div>

    <!-- Bảng chính -->
    <div class="grid" id="grid"></div>

    <!-- Khay chứa 3 khối ngẫu nhiên -->
    <div class="tray" id="tray"></div>

    <!-- Bảng Game Over -->
    <div id="game-over">
        <h2>Thua mất rồi!</h2>
        <p>Điểm số của bạn: <span id="final-score">0</span></p>
        <button onclick="resetGame()">Chơi lại</button>
    </div>

<script>
    const GRID_SIZE = 8;
    let score = 0;
    let board = Array(GRID_SIZE).fill(0).map(() => Array(GRID_SIZE).fill(0));
    
    // Các hình dạng khối cơ bản
    const SHAPES = [
        [[1]], // Khối đơn 1x1
        [[1, 1]], // Thanh ngang 2
        [[1], [1]], // Thanh dọc 2
        [[1, 1], [1, 1]], // Vuông 2x2
        [[1, 1, 1]], // Thanh ngang 3
        [[1], [1], [1]], // Thanh dọc 3
        [[1, 1], [1, 0]], // Góc L nhỏ
    ];

    let currentTray = [null, null, null];

    const gridEl = document.getElementById('grid');
    const trayEl = document.getElementById('tray');
    const scoreEl = document.getElementById('score');
    const gameOverEl = document.getElementById('game-over');

    function initGame() {
        createGridDOM();
        generateNewTray();
    }

    function createGridDOM() {
        gridEl.innerHTML = '';
        for (let r = 0; r < GRID_SIZE; r++) {
            for (let c = 0; c < GRID_SIZE; c++) {
                const cell = document.createElement('div');
                cell.classList.add('cell');
                cell.dataset.row = r;
                cell.dataset.col = c;
                gridEl.appendChild(cell);
            }
        }
    }

    function renderBoard() {
        const cells = gridEl.children;
        for (let r = 0; r < GRID_SIZE; r++) {
            for (let c = 0; c < GRID_SIZE; c++) {
                const index = r * GRID_SIZE + c;
                if (board[r][c] === 1) {
                    cells[index].classList.add('filled');
                } else {
                    cells[index].classList.remove('filled');
                }
            }
        }
    }

    function getRandomShape() {
        return SHAPES[Math.floor(Math.random() * SHAPES.length)];
    }

    function generateNewTray() {
        currentTray = [getRandomShape(), getRandomShape(), getRandomShape()];
        renderTray();
        checkGameOver();
    }

    function renderTray() {
        trayEl.innerHTML = '';
        currentTray.forEach((shape, index) => {
            if (!shape) return;
            const container = document.createElement('div');
            container.classList.add('block-container');
            container.draggable = true;
            container.dataset.index = index;

            const rows = shape.length;
            const cols = shape[0].length;
            container.style.gridTemplateColumns = `repeat(${cols}, 30px)`;
            container.style.gridTemplateRows = `repeat(${rows}, 30px)`;

            shape.forEach(row => {
                row.forEach(val => {
                    const blockCell = document.createElement('div');
                    blockCell.classList.add('mini-cell');
                    if (val === 1) blockCell.classList.add('filled');
                    else blockCell.classList.add('empty');
                    container.appendChild(blockCell);
                });
            });

            // Xử lý sự kiện kéo thả đơn giản cho Desktop/Web
            container.addEventListener('dragstart', (e) => {
                e.dataTransfer.setData('text/plain', index);
            });

            trayEl.appendChild(container);
        });
    }

    // Sự kiện thả khối vào lưới
    gridEl.addEventListener('dragover', (e) => e.preventDefault());
    gridEl.addEventListener('drop', (e) => {
        e.preventDefault();
        const shapeIndex = e.dataTransfer.getData('text/plain');
        const shape = currentTray[shapeIndex];
        if (!shape) return;

        // Lấy ô mục tiêu trên lưới khi thả chuột
        const target = e.target.closest('.cell');
        if (!target) return;

        const startR = parseInt(target.dataset.row);
        const startC = parseInt(target.dataset.col);

        if (canPlace(shape, startR, startC)) {
            placeShape(shape, startR, startC);
            currentTray[shapeIndex] = null;
            renderBoard();
            renderTray();
            checkClear();

            // Nếu đã dùng hết 3 khối trong khay -> tạo khay mới
            if (currentTray.every(s => s === null)) {
                generateNewTray();
            } else {
                checkGameOver();
            }
        }
    });

    function canPlace(shape, r, c) {
        for (let i = 0; i < shape.length; i++) {
            for (let j = 0; j < shape[i].length; j++) {
                if (shape[i][j] === 1) {
                    let targetR = r + i;
                    let targetC = c + j;
                    if (targetR >= GRID_SIZE || targetC >= GRID_SIZE || board[targetR][targetC] === 1) {
                        return false;
                    }
                }
            }
        }
        return true;
    }

    function placeShape(shape, r, c) {
        for (let i = 0; i < shape.length; i++) {
            for (let j = 0; j < shape[i].length; j++) {
                if (shape[i][j] === 1) {
                    board[r + i][c + j] = 1;
                    score += 10;
                }
            }
        }
        scoreEl.innerText = score;
    }

    function checkClear() {
        let rowsToClear = [];
        let colsToClear = [];

        // Kiểm tra hàng ngang
        for (let r = 0; r < GRID_SIZE; r++) {
            if (board[r].every(cell => cell === 1)) rowsToClear.push(r);
        }
        // Kiểm tra hàng dọc
        for (let c = 0; c < GRID_SIZE; c++) {
            let colFull = true;
            for (let r = 0; r < GRID_SIZE; r++) {
                if (board[r][c] === 0) colFull = false;
            }
            if (colFull) colsToClear.push(c);
        }

        // Thực hiện xóa và cộng điểm thưởng combo
        rowsToClear.forEach(r => {
            for (let c = 0; c < GRID_SIZE; c++) board[r][c] = 0;
            score += 100;
        });
        colsToClear.forEach(c => {
            for (let r = 0; r < GRID_SIZE; r++) board[r][c] = 0;
            score += 100;
        });

        scoreEl.innerText = score;
        renderBoard();
    }

    function checkGameOver() {
        // Kiểm tra xem còn khối nào trong khay đặt được lên
