console.log("Js conectado")

let socket = io.connect('http://' + document.domain + ':' + location.port);

// Lado del server
socket.on('connect', function () {
    socket.emit('join_game', data='hola');
    console.log('Connected to the server');
});

socket.on('juego_actual', function(id) {
    console.log('Te has unido al juego con ID:', id);
    window.location.href = "http://localhost:5000/game/" + id;
});

socket.on('response', function (data) {
    console.log('Server says: ' + data);
});

// FUNCIONES LLAMADAS POR EL CLIENTE
function newGame(){
    var name = document.getElementById('player_name').value
    socket.emit('new_game',{player_name: name})
}

// Falta corregir
function joinGame(){
    var name = document.getElementById('player_name').value
    var id = document.getElementById('room_id').value
    if(id){ // Verifica que se haya ingresado un ID
        socket.emit('connect_game', { room_id: id , player_name: name}); // Envía el ID al servidor
    }else{
        alert('Por favor, ingresa un ID válido de sala.');
    }
}



