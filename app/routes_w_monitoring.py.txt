from flask import Flask, request, jsonify, send_file, render_template
from app import app
from app.services.scraper import Scraper
from app.services.translator_azureai import Translator_azure
from app.services.markdown_ft import Convertmarkdown
from app.services.translator_gcp import Translator_gcp
import time
import logging
import os 
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor


# Configure logging
logging.basicConfig(level=logging.DEBUG)
output_dir = os.getenv("FLASK_OUTPUT_DIR", "/app/outputs") ## Default for local tests:"/app/outputs" ||  "/home" for Linux App Service Web App

InstrumentationKey = os.getenv("INSTRUMENTATION_KEY")
configure_azure_monitor(
    connection_string=InstrumentationKey,
    enable_live_metrics=True
)
# Instrument your Flask app and HTTP requests
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/api/translate', methods=['POST'])
def transcribe_video():
    """
    Translates the content of a web page specified by a URL and returns the translated content as a downloadable file.
    """
    try:
        data = request.get_json()
        logging.debug(f"Request data: {data}")

        if not data:
            logging.error("Missing request body")
            return jsonify({"error": "Missing request body"}), 400

        if not data.get("url"):
            logging.error("Missing 'url' in request body")
            return jsonify({"error": "Missing 'url' in request body"}), 400

        url = data.get("url")

        # Scraping
        try:
            scraper = Scraper(url)
            scraper.fetch_content()
            content = scraper.html_process()
        except Exception as e:
            logging.error(f"Error in scraper: {e}", exc_info=True)
            return jsonify({"error": f"Error in scraper: {e}"}), 500

        # Translation (Azure)
        if data.get("translator_api") == "azure":
            if data.get("azure_endpoint") and data.get("azure_credentials"):
                azure_endpoint = data.get("azure_endpoint")
                azure_credential = data.get("azure_credentials")
                translator = Translator_azure(azure_endpoint, azure_credential)
                content_en = []

                for element in content:
                    if element['type'] != 'image':  # Skip images
                        try:
                            translated_text = Translator_azure.translate(translator, element['content'])
                            content_en.append({'type': element['type'], 'content': translated_text})
                        except Exception as e:
                            logging.error(f"Error in Azure translation: {e}", exc_info=True)
                            return jsonify({"error": f"Error in Azure translation: {e}"}), 500
                    else:
                        content_en.append(element)  # Add images as-is
            else:
                logging.error("Missing 'azure_endpoint' or 'azure_credentials' in request body")
                return jsonify({"error": "Missing 'azure_endpoint' or 'azure_credentials' in request body"}), 400

        # Translation (Google)
        elif data.get("translator_api") == "google":
            if data.get("google_app_creds") and data.get("gcp_project_id"):
                gcp_project_id = data.get("gcp_project_id")
                google_app_creds = data.get("google_app_creds")
                content_en = []

                for element in content:
                    if element['type'] != 'image':  # Skip images
                        try:
                            translator_gcp = Translator_gcp(element['content'], gcp_project_id)
                            translated_text = translator_gcp.translate_text()
                            content_en.append({'type': element['type'], 'content': translated_text})
                        except Exception as e:
                            logging.error(f"Error in Google translation: {e}", exc_info=True)
                            return jsonify({"error": f"Error in Google translation: {e}"}), 500
                    else:
                        content_en.append(element)  # Add images as-is
            else:
                logging.error("Missing 'gcp_project_id' or 'google_app_creds' in request body")
                return jsonify({"error": "Missing 'gcp_project_id' or 'google_app_creds' in request body"}), 400

        else:
            translator = data.get("translator_api")
            logging.error(f"Translator '{translator}' not supported by the API")
            return jsonify({"error": f"Translator '{translator}' not supported by the API."}), 400

        # Markdown conversion
        try:
            timestr = time.strftime("%Y%m%d-%H%M%S")
            path = f"{output_dir}/output-{timestr}.md"
            converter = Convertmarkdown(content_en, path)
            markdown_content = converter.convert_to_markdown()
            saved_file = converter.save_to_markdown_file(markdown_content)
        except Exception as e:
            logging.error(f"Error in Markdown formatting: {e}", exc_info=True)
            return jsonify({"error": f"Error in Markdown formatting: {e}"}), 500

        return send_file(saved_file, as_attachment=True)

    except Exception as e:
        logging.error(f"Unhandled exception: {e}", exc_info=True)
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500
