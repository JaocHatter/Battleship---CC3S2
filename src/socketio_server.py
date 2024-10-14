from flask import Flask, render_template, Blueprint
from flask_socketio import SocketIO, emit, join_room, leave_room
from nanoid import generate

app = Flask(__name__)
app.config['SECRET_KEY'] = 'CC3S2 -  Grupo 3'

socketio = SocketIO(app)

roomBp = Blueprint('sala', __name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game/<id>')
def game_room(id):
    print('id: ', id)
    return render_template('gameRoom.html', id=id)    

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('new_game')
def create_game():
    id= generate(size=5)
    print('new game created')
    socketio.emit('new game', id)




@socketio.on('message')
def handle_message(data):
    print('Received message:', data)
    socketio.emit('response', 'Server received your message: ' + data)
    

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)