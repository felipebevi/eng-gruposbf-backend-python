from flask import Flask, jsonify, request
from urllib.request import urlopen
import json

app = Flask(__name__)

@app.route("/api/convert/<country>/<value>")
def inicio(country,value):
    error = False
    message = ""
    currencies = getCurrencies()
    if country not in currencies:
        error = True
        message = "All country currencies needs to respect a international convention and came from this open sourced list: https://openexchangerates.org/api/currencies.json"
    
    
    
    if error == False:
        return jsonify({"error": False, "message": "API inicial - country: "+country+" - value: "+value})
    else:
        return jsonify({"error": True, "message": message})


@app.errorhandler(404)  
def not_found(e):
    return jsonify({"error": True, "messages": [
        "How to use:",
        "Use URL like "+request.base_url+"api/convert/<Country>/<Value>",
        "Ex.: "+request.base_url+"api/convert/BRL/123",
        "All country currencies needs to respect a international convention and came from this open sourced list: https://openexchangerates.org/api/currencies.json"
    ]
    })
  

def getCurrencies(ini=False):
    url = "https://openexchangerates.org/api/currencies.json"
    response = urlopen(url)
    data_json = json.loads(response.read())
    if ini != False and ini in data_json:
        return data_json[ini]
    else:
        return data_json

  
if __name__ == "__main__":
    app.run()