from flask import Flask, render_template, Blueprint, session
from flask_socketio import SocketIO, emit, join_room, leave_room
from nanoid import generate

app = Flask(__name__)
app.config['SECRET_KEY'] = 'CC3S2 -  Grupo 3'

socketio = SocketIO(app)
games = {}  # Diccionario para almacenar las instancias de juego

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

# Lado del servidor
@socketio.on('new_game')
def create_game():
    id= generate(size=5)
    join_room(id)
    print('El juego ha sido generado con el id: '+id)
    socketio.emit('juego_actual', id, room=id)

@socketio.on('connect_game')
def join_game(data):
    room_id = data['room_id']  # Obtén el ID de la sala del cliente
    print(f'Usuario unido a la sala {room_id}')
    join_room(room_id)  
    print(f'Usuario unido a la sala {room_id}')
    socketio.emit('juego_actual', room_id, room=room_id)

@socketio.on('message')
def handle_message(data):
    print('Received message:', data)
    socketio.emit('response', 'Server received your message: ' + data)
    



