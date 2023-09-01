from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/api/convert/<pais>/<valor>")
def inicio(pais,valor):
    return jsonify({"message": "API inicial: "+pais+" - valor: "+valor})

if __name__ == "__main__":
    app.run()