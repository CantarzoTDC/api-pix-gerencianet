
import base64
import requests
import json

from utils.constants import CLIENT_ID, CLIENT_SECRET, CERTIFICADO, URL_ROOT_PROD


class PixService():
    # inicializa headers com token de auth para utilizar a API da GerenciaNet 
    def __init__(self, ):
        self.headers = {
            'Authorization': f'Bearer {self.get_token()}',
            'Content-Type': 'application/json'
        }
    # Chamada na API para pegar o Token de auth
    def get_token(self, ):
        auth = base64.b64encode(
            (f"{CLIENT_ID}:{CLIENT_SECRET}").encode()).decode()

        headers = {
            'Authorization': f'Basic {auth}',
            'Content-Type': 'application/json'
        }

        payload = {"grant_type": "client_credentials"}

        response = requests.post(
            f'{URL_ROOT_PROD}/oauth/token',
            headers=headers,
            data=json.dumps(payload),
            cert=CERTIFICADO
        )

        return json.loads(response.content)['access_token']

    # Cria QRCode 
    def create_qrcode(self, location_id):
        response = requests.get(
            f'{URL_ROOT_PROD}/v2/loc/{location_id}/qrcode', headers=self.headers, cert=CERTIFICADO)

        return json.loads(response.content)

    def get_saldo(self,):
        response = requests.get(
            f'{URL_ROOT_PROD}/v2/gn/saldo', headers=self.headers, cert=CERTIFICADO)

        return json.loads(response.content)

    # Gera QRCode para o Front
    def qrcode_generator(self, location_id):
        qrcode = self.create_qrcode(location_id)

        return qrcode

    # Gera uma cobrança para conseguir criar um QRCode
    def create_order(self, txid, payload):

        response = requests.put(f'{URL_ROOT_PROD}/v2/cob/{txid}',
                                data=json.dumps(payload), headers=self.headers, cert=CERTIFICADO)

        if response.status_code == 201:
            return json.loads(response.content)

        return {}

    # Cria cobrança e retorno o QRCode
    def create_cobranca(self, txid, payload):
        location_id = self.create_order(txid, payload).get('loc').get('id')
        qrcode = self.qrcode_generator(location_id)
        return qrcode
