function renderBoard(board) {
    const chessboard = document.getElementById('chessboard');
    chessboard.innerHTML = '';  // clear

    for (let r = 0; r < 8; r++) {
    const rowDiv = document.createElement('div');
    rowDiv.classList.add('row');

    for (let c = 0; c < 8; c++) {
        const squareDiv = document.createElement('div');
        squareDiv.classList.add('square');
        if ((r + c) % 2 === 0) {
        squareDiv.classList.add('white');
        } else {
        squareDiv.classList.add('black');
        }

        const piece = board[r][c];
        if (piece !== '') {
        const img = document.createElement('img');
        img.src = `/static/images/${piece}.png`;
        img.width = 60;
        squareDiv.appendChild(img);
        } else {
        squareDiv.innerHTML = '&nbsp;';
        }
        rowDiv.appendChild(squareDiv);
    }
    chessboard.appendChild(rowDiv);
    }
}

document.getElementById('moveBtn').addEventListener('click', () => {
    fetch('/update_board', { method: 'POST' })
    .then(res => res.json())
    .then(data => {
        renderBoard(data.board);
    });
});