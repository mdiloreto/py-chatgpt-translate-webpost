from azure.ai.translation.document import DocumentTranslationClient
from azure.core.credentials import AzureKeyCredential
import requests, uuid, json


class Translator_azure:
    def __init__(self, endpoint, key):
        self.endpoint = endpoint  # Store the endpoint as an instance variable
        self.key = key  # Store the key as an instance variable
        self.client = DocumentTranslationClient(endpoint, AzureKeyCredential(key))

    def translate(self, text):
        location = "eastus"
        path = '/translate'
        constructed_url = self.endpoint + path

        params = {
            'api-version': '3.0',
            'from': 'es',
            'to': ['en']
        }

        headers = {
            'Ocp-Apim-Subscription-Key': self.key,
            'Ocp-Apim-Subscription-Region': location,
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }

        # You can pass more than one object in body.
        body = [{
            'text': text
        }]

        try:
            request = requests.post(constructed_url, params=params, headers=headers, json=body)
            request.raise_for_status()  # Raise exception for HTTP errors
            response = request.json()

            # Assuming response contains the translated text
            return response[0]['translations'][0]['text']
        
        except Exception as e:
            print(f"Error during translation: {e}")
            return None