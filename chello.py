from flask import Flask

app = Flask(__name__)

@app.route('/')
def run():
    return """
    <html>
        <head>
            <style>
                p.bold {
                    font-weight: bold;
                }
                .blåfarge {
                    color: green}
                h1 {
                    font_family
                }

            </style>
        </head>
        <body>
            <h2>Mausund nettside yeah</h2>
            <h2>dette blir bra</h2>
            <h1>Sensor greier</h1>
            <p>Noen bilder kanskje<p>
            <p class="blåfarge">Grafer her? Eller på en ny side muligens?</p>

        </body>
    </html>
"""
