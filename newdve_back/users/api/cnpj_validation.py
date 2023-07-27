import requests
import json

def cnpj_validation(cnpj):
    url = f"https://receitaws.com.br/v1/cnpj/{cnpj}"
    response = requests.request("GET", url)
    response = json.loads(response.text)

    return response