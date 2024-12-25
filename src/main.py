from flask import Flask
from services.audio import AudioService

app = Flask(__name__)

audioService = AudioService()

@app.route("/")
def hello_world():
    return "Hello, World!"

@app.route("/audio/start")
def startAudio():
    try:
        audioService.start()
        return "", 200
    except:
        return "", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
