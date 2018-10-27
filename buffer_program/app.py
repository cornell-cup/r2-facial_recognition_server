from flask import Flask

app = Flask(__name__)

@app.route("/")
def root():
    return "hello"

if (__name__ == "__main"):
    app.debug = True
    app.run()

