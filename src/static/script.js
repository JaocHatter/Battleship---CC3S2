console.log("Js conectado")

let socket = io.connect('http://' + document.domain + ':' + location.port);


        socket.on('connect', function () {
            socket.emit('join', data='hola');
            console.log('Connected to the server');
        });

        socket.on('response', function (data) {
            console.log('Server says: ' + data);
        });

        socket.on('new game', function(id){
            console.log('game id: ', id);
            window.location.href = "http://localhost:5000/game/"+id;
        })

        function sendMessage() {
            var message = document.getElementById('message').value;
            socket.emit('message', message);
        }



function newGame(){
    console.log("new game")
    socket.emit('new_game')

}

