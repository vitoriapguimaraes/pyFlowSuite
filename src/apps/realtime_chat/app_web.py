# HashZap - Web Chat (Flask + SocketIO)

import logging
from flask import Flask, render_template
from flask_socketio import SocketIO, send

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

app = Flask(__name__)
# In production, use a secure secret key and move it to environment variables
app.config["SECRET_KEY"] = "dev_secret_key_12345"
app.config["DEBUG"] = True

# CORS allowed for local dev
socketio = SocketIO(app, cors_allowed_origins="*")


@socketio.on("message")
def gerenciar_mensagens(mensagem):
    logging.info(f"Message received: {mensagem}")
    send(mensagem, broadcast=True)


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    logging.info("Starting HashZap Web Server...")
    # Allow 0.0.0.0 for access within local network
    socketio.run(app, host="0.0.0.0", port=5000)
