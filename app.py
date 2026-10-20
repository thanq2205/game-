<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Block Blast Game</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #0d1b2a;
            color: #ffffff;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            overflow: hidden;
        }

        /* Màn hình bắt đầu: Nền xanh dương, nút xanh lá */
        .start-screen {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: #1b4965;
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 20;
        }

        .menu-content {
            text-align: center;
        }

        .menu-content h1 {
            font-size: 52px;
            margin-bottom: 30px;
            letter-spacing: 3px;
            color: #ffffff;
        }

        .start-btn {
            background-color: #2ec4b6;
            color: white;
            font-size: 24px;
            font-weight: bold;
            padding: 15px 45px;
            border: none;
            border-radius: 50px;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(46, 196, 182, 0.4);
            transition: all 0.2s ease;
        }

        .start-btn:hover {
            background-color: #25a194;
            transform: scale(1.05);
        }

        /* Màn hình chơi chính: Nền xanh đậm */
        .game-container {
            text-align: center;
            background-color: #111827;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.5);
        }

        .header-info h1 {
            margin: 0 0 10px 0;
            font-size: 24px;
            color: #60a5fa;
        }

        .score-board {
            font-size: 20px;
            margin-bottom: 15px;
            font-weight: bold;
            color: #34d399;
        }

        .game-board-wrapper {
            position: relative;
            width: fit-content;
            margin: 0 auto;
        }

        /* Vạch giới hạn ở trên */
        .limit-line {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 3px;
            background-color: #ef4444;
            z-index: 5;
            box-shadow: 0 0 8px #ef4444;
        }

        /* Lưới chơi (12 hàng x 8 cột) */
        .grid {
            display: grid;
            grid-template-columns: repeat(8, 35px);
            grid-template-rows: repeat(12, 35px);
            gap: 2px;
            background-color: #1f2937;
            padding: 5px;
            border-radius: 6px;
        }

        .cell {
            width: 35px;
            height: 35px;
            background-color: #374151;
            border-radius: 3px;
        }

        .instructions {
            margin-top: 15px;
            font-size: 13px;
            color: #9ca3af;
        }

        /* Màn hình Game Over */
        .game-over-screen {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(13, 27, 42, 0.9);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 30;
        }

        .game-over-screen h2 {
            font-size: 56px;
            color: #ef4444;
            margin-bottom: 10px;
        }

        .game-over-screen p {
            font-size: 24px;
            color: #ffffff;
        }

        .hidden {
            display: none !important;
        }
    </style>
</head>
<body>

    <!-- MÀN HÌNH BẮT ĐẦU -->
    <div id="start-screen" class="start-screen">
        <div class="menu-content">
            <h1>BLOCK BLAST</h1>
            <button id="start-btn" class="start-btn">Bắt đầu</button>
        </div>
    </div>

    <!-- MÀN HÌNH CHƠI GAME CHÍNH -->
    <div id="game-container" class="game-container hidden">
        <div class="header-info">
            <h1>BLOCK BLAST</h1>
            <div class="score-board">Điểm: <span id="score">0</span></div>
        </div>

        <div class="game-board-wrapper">
            <div class="limit-line"></div>
            <div id="grid" class="grid"></div>
        </div>

        <div class="instructions">
            Dùng phím mũi tên <b>Trái / Phải</b> để di chuyển, <b>Xuống</b> để rơi nhanh.
        </div>
    </div>

    <!-- MÀN HÌNH GAME OVER -->
    <div id="game-over-screen" class="game-over-screen hidden">
        <h2>GAME OVER</h2>
        <p>Điểm của bạn: <span id="final-score">0</span></p>
    </div>

    <script>
        const ROWS = 12;
        const COLS = 8;
        let grid = Array(ROWS).fill(null).map(() => Array(COLS).fill(0));
        let score = 0;
        let gameInterval = null;
        let isPlaying = false;

        const COLOR_PALETTES = [
            "#f97316", // Cam
            "#3b82f6", // Xanh dương sáng
            "#10b981", // Xanh lá
            "#8b5cf6", // Tím
            "#ec4899", // Hồng
            "#eab308"  // Vàng
        ];

        const SHAPES = [
            [[1, 1], [1, 1]],         
            [[1, 1, 1, 1]],           
            [[1, 1, 1], [0, 1, 0]],   
            [[1, 1, 0], [0, 1, 1]],   
            [[1, 1]]                  
        ];

        let currentPiece = {
            shape: [],
            row: 0,
            col: 0,
            color: "#f97316"
        };

        const gridElement = document.getElementById('grid');
        const scoreElement = document.getElementById('score');
        const startScreen = document.getElementById('start-screen');
        const startBtn = document.getElementById('start-btn');
        const gameContainer = document.getElementById('game-container');
        const gameOverScreen = document.getElementById('game-over-screen');
        const finalScoreElement = document.getElementById('final-score');

        function initGridDOM() {
            gridElement.innerHTML = '';
            for (let r = 0; r < ROWS; r++) {
                for (let c = 0; c < COLS; c++) {
                    const cell = document.createElement('div');
                    cell.classList.add('cell');
                    cell.dataset.row = r;
                    cell.dataset.col = c;
                    gridElement.appendChild(cell);
                }
            }
        }

        function getCurrentColor() {
            let index = Math.floor(score / 5) % COLOR_PALETTES.length;
            return COLOR_PALETTES[index];
        }

        function spawnPiece() {
            const randomShape = SHAPES[Math.floor(Math.random() * SHAPES.length)];
            currentPiece.shape = randomShape;
            currentPiece.row = 0;
            currentPiece.col = Math.floor((COLS - randomShape[0].length) / 2);
            currentPiece.color = getCurrentColor();

            if (checkCollision(currentPiece.row, currentPiece.col, currentPiece.shape)) {
                endGame();
            }
        }

        function checkCollision(targetRow, targetCol, shape) {
            for (let r = 0; r < shape.length; r++) {
                for (let c = 0; c < shape[r].length; c++) {
                    if (shape[r][c] === 1) {
                        let newR = targetRow + r;
                        let newC = targetCol + c;
                        if (newC < 0 || newC >= COLS || newR >= ROWS) return true;
                        if (newR >= 0 && grid[newR][newC] !== 0) return true;
                    }
                }
            }
            return false;
        }

        function lockPiece() {
            for (let r = 0; r < currentPiece.shape.length; r++) {
                for (let c = 0; c < currentPiece.shape[r].length; c++) {
                    if (currentPiece.shape[r][c] === 1) {
                        let boardR = currentPiece.row + r;
                        let boardC = currentPiece.col + c;
                        if (boardR >= 0 && boardR < ROWS && boardC >= 0 && boardC < COLS) {
                            grid[boardR][boardC] = currentPiece.color;
                        }
                    }
                }
            }
        }

        function clearLines() {
            let linesCleared = 0;
            for (let r = ROWS - 1; r >= 0; r--) {
                if (grid[r].every(cell => cell !== 0)) {
                    grid.splice(r, 1);
                    grid.unshift(Array(COLS).fill(0));
                    linesCleared++;
                    r++;
                }
            }
            if (linesCleared > 0) {
                score += linesCleared;
                scoreElement.innerText = score;
            }
        }

        function draw() {
            const cells = gridElement.children;
            
            for (let r = 0; r < ROWS; r++) {
                for (let c = 0; c < COLS; c++) {
                    const index = r * COLS + c;
                    const cell = cells[index];
                    if (grid[r][c] !== 0) {
                        cell.style.backgroundColor = grid[r][c];
                    } else {
                        cell.style.backgroundColor = '#374151';
                    }
                }
            }

            for (let r = 0; r < currentPiece.shape.length; r++) {
                for (let c = 0; c < currentPiece.shape[r].length; c++) {
                    if (currentPiece.shape[r][c] === 1) {
                        let boardR = currentPiece.row + r;
                        let boardC = currentPiece.col + c;
                        if (boardR >= 0 && boardR < ROWS && boardC >= 0 && boardC < COLS) {
                            const index = boardR * COLS + boardC;
                            cells[index].style.backgroundColor = currentPiece.color;
                        }
                    }
                }
            }
        }

        function updateGame() {
            if (!isPlaying) return;

            if (!checkCollision(currentPiece.row + 1, currentPiece.col, currentPiece.shape)) {
                currentPiece.row++;
            } else {
                lockPiece();
                clearLines();
                spawnPiece();
            }
            draw();
        }

        document.addEventListener('keydown', (e) => {
            if (!isPlaying) return;

            if (e.key === 'ArrowLeft') {
                if (!checkCollision(currentPiece.row, currentPiece.col - 1, currentPiece.shape)) {
                    currentPiece.col--;
                    draw();
                }
            } else if (e.key === 'ArrowRight') {
                if (!checkCollision(currentPiece.row, currentPiece.col + 1, currentPiece.shape)) {
                    currentPiece.col++;
                    draw();
                }
            } else if (e.key === 'ArrowDown') {
                if (!checkCollision(currentPiece.row + 1, currentPiece.col, currentPiece.shape)) {
                    currentPiece.row++;
                    draw();
                }
            }
        });

        function startGame() {
            startScreen.classList.add('hidden');
            gameOverScreen.classList.add('hidden');
            gameContainer.classList.remove('hidden');

            grid = Array(ROWS).fill(null).map(() => Array(COLS).fill(0));
            score = 0;
            scoreElement.innerText = score;
            isPlaying = true;

            initGridDOM();
            spawnPiece();
            draw();

            if (gameInterval) clearInterval(gameInterval);
            gameInterval = setInterval(updateGame, 500);
        }

        function endGame() {
            isPlaying = false;
            clearInterval(gameInterval);
            finalScoreElement.innerText = score;
            gameOverScreen.classList.remove('hidden');

            setTimeout(() => {
                gameOverScreen.classList.add('hidden');
                gameContainer.classList.add('hidden');
                startScreen.classList.remove('hidden');
            }, 3000);
        }

        startBtn.addEventListener('click', startGame);
    </script>
</body>
</html>
