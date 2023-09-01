from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/api/convert/<country>/<value>")
def inicio(country,value):
    error = False
    message = ""
    
    if error == False:
        return jsonify({"error": False, "message": "API inicial - country: "+country+" - value: "+value})
    else:
        return jsonify({"error": True, "message": message})


@app.errorhandler(404)  
def not_found(e):
    return jsonify({"error": True, "message": "Use URL like "+request.base_url+"api/convert/<Country>/<Value> Ex.: "+request.base_url+"api/convert/BRL/123"})
  
  
if __name__ == "__main__":
    app.run()