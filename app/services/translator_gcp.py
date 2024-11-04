from google.cloud import translate

class Translator_gcp:
    def __init__(self, text, project_id):
        self.text = text
        self.project_id = project_id

    def translate_text(self):
        """Translating Text."""

        client = translate.TranslationServiceClient()

        location = "global"

        parent = f"projects/{self.project_id}/locations/{location}"

        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [self.text],
                "mime_type": "text/plain",  # mime types: text/plain, text/html
                "source_language_code": "es",
                "target_language_code": "en-US",
            }
        )

        # Display the translation for each input text provided
        for translation in response.translations:
            print(f"Translated text: {translation.translated_text}")

        return response.translations[0].translated_text