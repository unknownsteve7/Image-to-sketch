from flask import Flask
from waitress import serve
app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Hello, this is a production server!</h1>"

if __name__ == "__main__":
    serve(app,host='0.0.0.0',port=8000)