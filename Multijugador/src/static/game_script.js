// Conectar con el servidor Socket.IO
let socket = io.connect('http://' + document.domain + ':' + location.port);

// Variables globales
let room_id = "{{id}}";
let player_name = sessionStorage.getItem('player_name');
let ships_placed = 0;
let max_ships = 5;
let is_turn = false;
let ownBoard = [];
let enemyBoard = [];

// Mostrar el nombre del jugador
document.getElementById('player-name').innerText = player_name;

// Inicializar los tableros
function initializeBoards() {
    for (let i = 0; i < 5; i++) {
        ownBoard[i] = [];
        enemyBoard[i] = [];
        let ownRow = document.createElement('tr');
        let enemyRow = document.createElement('tr');
        for (let j = 0; j < 5; j++) {
            // Tablero propio
            ownBoard[i][j] = 0;
            let ownCell = document.createElement('td');
            ownCell.dataset.x = i;
            ownCell.dataset.y = j;
            ownCell.addEventListener('click', placeShip);
            ownRow.appendChild(ownCell);

            // Tablero enemigo
            enemyBoard[i][j] = 0;
            let enemyCell = document.createElement('td');
            enemyCell.dataset.x = i;
            enemyCell.dataset.y = j;
            enemyCell.addEventListener('click', fireShot);
            enemyCell.classList.add('enemy-cell');
            enemyRow.appendChild(enemyCell);
        }
        document.getElementById('own-board').appendChild(ownRow);
        document.getElementById('enemy-board').appendChild(enemyRow);
    }
}

function placeShip(event) {
    if (ships_placed >= max_ships) {
        alert('Ya has colocado todos tus barcos.');
        return;
    }
    let x = event.target.dataset.x;
    let y = event.target.dataset.y;
    socket.emit('place_ship', { room_id: room_id, x: parseInt(x), y: parseInt(y) });
}

socket.on('ship_placed', function(data) {
    if (data.success) {
        ships_placed++;
        let cell = document.querySelector(`#own-board td[data-x='${data.x}'][data-y='${data.y}']`);
        cell.classList.add('ship');
        if (ships_placed === max_ships) {
            socket.emit('ships_ready', { room_id: room_id });
            document.getElementById('status').innerText = 'Esperando al oponente...';
        }
    } else {
        alert('Ya hay un barco en esa posición.');
    }
});

socket.on('both_ready', function() {
    document.getElementById('status').innerText = '¡El juego ha comenzado!';
});

function fireShot(event) {
    if (!is_turn) {
        alert('No es tu turno.');
        return;
    }
    let x = event.target.dataset.x;
    let y = event.target.dataset.y;
    socket.emit('make_move', { room_id: room_id, x: parseInt(x), y: parseInt(y) });
}

socket.on('move_result', function(data) {
    is_turn = false;
    let cell = document.querySelector(`#enemy-board td[data-x='${data.x}'][data-y='${data.y}']`);
    if (data.hit) {
        cell.classList.add('hit');
        alert('¡Acertaste!');
    } else {
        cell.classList.add('miss');
        alert('Fallaste.');
    }
});

socket.on('opponent_moved', function(data) {
    let cell = document.querySelector(`#own-board td[data-x='${data.x}'][data-y='${data.y}']`);
    if (data.hit) {
        cell.classList.add('hit');
        alert('¡El oponente acertó en tus barcos!');
    } else {
        cell.classList.add('miss');
        alert('El oponente falló.');
    }
    is_turn = true;
    document.getElementById('status').innerText = 'Es tu turno.';
});

socket.on('game_over', function(data) {
    if (data.winner === player_name) {
        alert('¡Has ganado!');
    } else {
        alert('Has perdido.');
    }
    // Reiniciar o redirigir si es necesario
});

socket.on('start_turn', function() {
    is_turn = true;
    document.getElementById('status').innerText = 'Es tu turno.';
});

// Inicializar los tableros al cargar la página
initializeBoards();
