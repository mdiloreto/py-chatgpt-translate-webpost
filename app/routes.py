import requests 
from flask import Flask, request, jsonify, send_file, render_template
from app import app
from app.services.scraper import Scraper
from app.services.translator_azureai import Translator_azure
from app.services.markdown_ft import Convertmarkdown
from app.services.translator_gcp import Translator_gcp

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/api/translate', methods=['POST'])
def transcribe_video():
    """
    Translates the content of a web page specified by a URL and returns the translated content as a downloadable file.

    The function processes a POST request with a JSON body that specifies the content to be translated
    using either Azure or Google translation services. The response is a markdown file containing the translated content.

    Request Body:
        {
            "url": str,                  # The URL of the web page to be scraped and translated. (Required)
            "translator_api": str,       # The translation service to use: "azure" or "google". (Required)
            
            # Attributes for Azure translation:
            "azure_endpoint": str,       # The endpoint URL for the Azure translation service. (Required if using Azure)
            "azure_credential": str,     # The API key or credential for the Azure translation service. (Required if using Azure)
            
            # Attributes for Google Cloud translation:
            "gcp_project_id": str,       # The Google Cloud project ID for translation. (Required if using Google)
            "google_app_creds": str      # The path or content of Google application credentials. (Required if using Google)
        }

    Returns:
        Response: 
            - A JSON response with an error message and a 400 status code if the required attributes are missing or invalid.
            - A markdown file as a response attachment if the translation is successful.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing request body"}), 400
    
    if not data.get("url"):
        return jsonify({"error": "Missing 'url' in request body"}), 400
    else:    
        url = data.get("url")     
        try: 
            scraper = Scraper(url)
            scraper.fetch_content()
            content = scraper.html_process()
        except Exception as e:
            return jsonify(f"Error in scraper: {e}"), 500
    
    if data.get("translator_api") == "azure":
        
        if data.get("azure_endpoint") and data.get("azure_credentials"):
            azure_endpoint = data.get("azure_endpoint")
            azure_credential = data.get("azure_credentials")
            translator = Translator_azure(azure_endpoint, azure_credential)
            content_en = []
            for element in content:
                if element['type'] != 'image':  # Skip images
                    translated_text = Translator_azure.translate(translator, element['content']) ## Translate Azure AI 
                    content_en.append({'type': element['type'], 'content': translated_text})
                else:
                    content_en.append(element)  # Add images as-is
            
        else:
            return jsonify({"error": "Missing 'azure_endpoint' or 'azure_credentials' in request body"}), 400
    
    elif data.get("translator_api") == "google":        
        if data.get("google_app_creds") and data.get("gcp_project_id"):
            gcp_project_id = data.get("gcp_project_id")
            google_app_creds = data.get("google_app_creds")
            try: 
                for element in content:
                    if element['type'] != 'image':  # Skip translation for images
                        translator_gcp = Translator_gcp(element['content'], gcp_project_id) ## Translate with GCP Translation API
                        translated_text = translator_gcp.translate_text()
                        content_en.append({'type': element['type'], 'content': translated_text})
                    else:
                        content_en.append(element)  # Add images as-is                
            except Exception as e:
                return jsonify(f"Error in scraper: {e}"), 500
        else:
            return jsonify({"error": "Missing 'gcp_project_id' or 'google_app_creds' in request body"}), 400
    
    else: 
        translator = data.get("translator_api")
        return jsonify({"error": f"Translator '{translator}' not supported by the API."}), 400

    try:         
        path = "output.md"
        converter = Convertmarkdown(content_en, path)
        markdown_content = converter.convert_to_markdown()
        saved_file = converter.save_to_markdown_file(markdown_content)  # Pass the generated markdown content to the method
    except Exception as e:
        return jsonify(f"Error in scraper: {e}"), 500
                
    return send_file(saved_file, as_attachment=True)