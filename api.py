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
    
    # parametro fixo para fins do teste em si
    moedas_desejadas = "BRL,USD,EUR,INR"
    cotacoes = getConversion(country, moedas_desejadas)
        
    # como a moeda base gratuita é o EURO precisaremos calcular aqui os novos valores
    rates = cotacoes["rates"]
    valores_convertidos = {}
    for moeda in rates:
        valores_convertidos[moeda] = format( ( 1 / float(rates[country]) * float(rates[moeda]) ) * float(value) * float(rates["EUR"]) , ".2f")

    if error == False:
        return jsonify(valores_convertidos)
    else:
        return jsonify({"error": True, "message": message})


@app.errorhandler(404)  
def not_found(e):
    return jsonify({"error": True, "messages": [
        "How to use:",
        "Warning: This API need to use an active internet connection to get the data.",
        "Use URL like "+request.base_url+"api/convert/<Country>/<Value>",
        "Ex.: "+request.base_url+"api/convert/BRL/123",
        "All country currencies needs to respect a international convention and came from this open sourced list: https://openexchangerates.org/api/currencies.json"
    ]
    })
  
def getConversion( _from, _to ): # _to aceita multiplos valores separados por virgula pela doc da API
    
    # DOC: https://exchangeratesapi.io/documentation/
        # Ex.:
        # https://api.exchangeratesapi.io/v1/latest
        # ? access_key = API_KEY
        # & base = USD
        # & symbols = GBP,JPY,EUR
        
    apikey = "7f235b16baee45c0c1c046f3f79bd04d" # TODO: colocar num .env
    url = "http://api.exchangeratesapi.io/v1/latest?access_key="+apikey  # TODO: colocar num .env
    # url += "&base="+_from # plano gratuito nao suborta moeda de base
    url += "&symbols="+_to+","+_from    
    response = urlopen(url)
    data_json = json.loads(response.read())
    return data_json
    

def getCurrencies(_ini=False):
    url = "https://openexchangerates.org/api/currencies.json"  # TODO: colocar num .env
    response = urlopen(url)
    data_json = json.loads(response.read())
    if _ini != False and _ini in data_json:
        return data_json[_ini]
    else:
        return data_json

  
if __name__ == "__main__":
    app.run()