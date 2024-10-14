var socket = io.connect('http://' + document.domain + ':' + location.port);

        socket.on('connect', function () {
            console.log('Connected to the server');
        });

        socket.on('response', function (data) {
            console.log('Server says: ' + data);
        });

        function sendMessage() {
            var message = document.getElementById('message').value;
            socket.emit('message', message);
        }