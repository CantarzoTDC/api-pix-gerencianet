from flask import Flask
from flask_restplus import Api


class Server(object):
    qrcode = {}
    quantidadeProduto = 0
    produto = ""
    saldo = 0

    def __init__(self):
        self.app = Flask(__name__, template_folder="../templates")
        self.api = Api(self.app,
                       version='1.0',
                       title='API PIX Gerencianet',
                       description='API para gerar pagamentos dinamicos.',
                       doc='/docs'
                       )

    def run(self):
        self.app.run(
            debug=True,
        )


server = Server()
