from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Hello Page</title>
    </head>
    <body style="text-align:center; margin-top: 50px;">
        <h1>Hello, World!</h1>
        <p>This is served using Python + HTML + CSS</p>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(debug=True)




