from flask_socketio import SocketIO

socketio = SocketIO()


@socketio.on("message")
def thing(data):
    print(data)
