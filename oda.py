from flask import Flask


app = Flask(__name__)

@app.route('/')
def run():
    return """
    <html>
        <head>
            <style>
                body {
                    background-color: lightblue;
                }
                .pink {
                    color: hotpink;
                    text-align: center;
                }
                h1 {
                    color: darkblue;
                    text-align: right;
                }
                img{
                    width: 400px;
                    position: absolute;
                    top: 200px;
                    left: 200px;
                }
            </style>
            
        </head>
        <body>
            <h2>Hello, Oda er best!</h2>
            <h1 class="pink">Yooooo</h1>
            <h1>Korleis går det</h1>
            <img src="/static/IMG_1727copy.JPG" alt="Det har oppstått en feil">
        </body>
    </html>
"""