from flask import request
from flask_restplus import Resource

from server.instance import server
from services.pix import PixService

import string
import random


api = server.api


@api.route('/orders', methods=["POST"])
class Pix(Resource):
    def post(self, ):
        valor = request.args.get("valor")
        produto = request.args.get("produto")
        quantidade = request.args.get("quantidade")

        txid = ''.join(random.choice(string.ascii_uppercase +
                                     string.digits) for _ in range(32))


        data = {
            "txid": txid,
            "calendario": {
                "expiracao": 86400
            },
            "valor": {
                "original": valor
            },
            "chave": "19e9eed9-d57b-43a4-80c3-9e8f3a945c9f",
            "solicitacaoPagador": f"pague o {produto}"
        }

        txid = data.pop('txid')
        pix_service = PixService()
        response = pix_service.create_cobranca(txid, data)
        server.qrcode = response["imagemQrcode"]
        server.produto = produto
        server.saldo = pix_service.get_saldo()
        server.quantidadeProduto = quantidade
        return response
