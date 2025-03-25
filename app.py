from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Defina o token como variável de ambiente (melhor prática de segurança)
TOKEN = os.getenv("PUSHINPAY_TOKEN", "21679|j3SZXmqR26Iy5ZCmOYeWJitptYoQBsbCqXqgw2kK53c6ac98")
API_URL = "https://api.pushinpay.com.br/pix/charge"

# Função para gerar QR Code Pix
def gerar_qr_code_pix(valor, descricao, txid):
    if valor not in [19.90, 29.90, 69.90]:
        return None, "Erro: Valor inválido"
    
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "value": valor,
        "description": descricao,
        "txid": txid
    }
    
    response = requests.post(API_URL, json=payload, headers=headers)
    
    if response.status_code == 201:
        link_pix = response.json()["pix_link"]
        return link_pix, None  # Retorna o link de pagamento
    else:
        return None, f"Erro: {response.text}"

# Rota para gerar pagamento e redirecionar
@app.route("/pagar", methods=["GET"])
def pagar():
    try:
        valor = float(request.args.get("valor"))
        descricao = "Pagamento pelo site"
        txid = f"pedido_{int(valor * 100)}"
        
        link_pix, erro = gerar_qr_code_pix(valor, descricao, txid)
        if erro:
            return jsonify({"erro": erro}), 400
        
        return jsonify({"pix_link": link_pix})  # Retorna o link Pix para o usuário
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
