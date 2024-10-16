console.log("Js conectado");

let socket = io.connect('http://' + document.domain + ':' + location.port);

let playerBoard = [];
let opponentBoard = [];
let isMyTurn = false;
let shipsPlaced = false;
let waitingForOpponent = false;

let currentLocation = window.location.href;
const playerNum = currentLocation.includes("player1") ? "player1" : "player2";
const room_id = currentLocation.match(/\/game\/([^\/]+)\/player/) ? currentLocation.match(/\/game\/([^\/]+)\/player/)[1] : null;

socket.on('connect', function () {
    socket.emit('join_game', data = 'hola');
    console.log('Connected to the server');
});

socket.on('juego_actual', function (data) {
    console.log('Te has unido al juego con ID:', data.id);
    console.log("You are ", data.player);
    window.location.href = "http://localhost:5000/game/" + data.id + "/" + data.player;
});

socket.on('response', function (data) {
    console.log('Server says: ' + data);
});

document.addEventListener('DOMContentLoaded', () => {
    createBoard('player_board', playerBoard, true);
    createBoard('opponent_board', opponentBoard, false);
});

function createBoard(elementId, board, isPlayerBoard) {
    let table = document.getElementById(elementId);
    for (let i = 0; i < 5; i++) {
        board[i] = [];
        let row = document.createElement('tr');
        for (let j = 0; j < 5; j++) {
            board[i][j] = 0;
            let cell = document.createElement('td');
            cell.classList.add('cell');
            cell.dataset.x = i;
            cell.dataset.y = j;

            if (isPlayerBoard) {
                cell.addEventListener('click', placeShip);
            } else {
                cell.addEventListener('click', attackCell);
            }

            row.appendChild(cell);
        }
        table.appendChild(row);
    }
}

function placeShip(event) {
    if (shipsPlaced) return;

    let x = event.target.dataset.x;
    let y = event.target.dataset.y;

    if (playerBoard[x][y] === 0) {
        playerBoard[x][y] = 1;
        event.target.classList.add('ship');
    } else {
        playerBoard[x][y] = 0;
        event.target.classList.remove('ship');
    }
}

function finalizeShipPlacement() {
    if (shipsPlaced) return;

    shipsPlaced = true;
    console.log({ 'board': playerBoard, 'room_id': room_id, 'player': playerNum });
    socket.emit('place_ships', { 'board': playerBoard, 'room_id': room_id, 'player': playerNum });
    document.getElementById('status').innerText = "Waiting for opponent...";
    waitingForOpponent = true;
}

socket.on('start_game', function (data) {
    console.log("game starts on ", data.room_id);
    document.getElementById('status').innerText = "Both players are ready. Let's start!";
    isMyTurn = true;
    updateStatus();
    waitingForOpponent = false;
});

function attackCell(event) {
    if (!isMyTurn || waitingForOpponent) return;

    let x = event.target.dataset.x;
    let y = event.target.dataset.y;

    document.getElementById('status').innerText = "Waiting for opponent";
    socket.emit('attack', { x: x, y: y, 'room_id': room_id, 'player': playerNum });
}

socket.on('attack_result', function (data) {
    if (data.player === 'opponent') {
        updateBoard(playerBoard, data.x, data.y, data.result);
    } else {
        updateBoard(opponentBoard, data.x, data.y, data.result);
    }

    isMyTurn = !isMyTurn;
    updateStatus();
});

socket.on('recieve_Attack', function (data) {
    updateBoard(playerBoard, data.x, data.y, data.result);
    document.getElementById('status').innerText = "It's your turn";
    isMyTurn = true;
    waitingForOpponent = false;
});

function updateBoard(board, x, y, result) {
    let table = (board === playerBoard) ? 'player_board' : 'opponent_board';
    let cells = document.querySelectorAll(`#${table} .cell`);
    let index = x * 5 + parseInt(y);
    let cell = cells[index];

    if (result === 'Hit') {
        cell.classList.add('hit');
    } else {
        cell.classList.add('miss');
    }
}

function updateStatus() {
    let status = isMyTurn ? "It's your turn!" : "Waiting for opponent...";
    document.getElementById('status').innerText = status;
}

function newGame() {
    console.log('Creando un nuevo juego...');
    socket.emit('new_game');
}

function joinGame() {
    let id = document.getElementById('room_id').value;
    if (id) {
        socket.emit('connect_game', { room_id: id });
        console.log(`Intentando unirse a la sala con ID: ${id}`);
    } else {
        alert('Por favor, ingresa un ID válido de sala.');
    }
}

function sendMessage() {
    let message = document.getElementById('message').value;
    socket.emit('message', message);
    console.log('Mensaje enviado al servidor:', message);
}

function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i].trim();
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

socket.on('game_over', function (data) {
    window.alert("Winner Is " + data.winner);
});