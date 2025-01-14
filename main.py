from translator_azureai import Translator_azure
from translator_gcp import Translator_gcp
from scraper import Scraper
from markdown_ft import Convertmarkdown
from publish_medium import MediumPublisher
import os
## Text Translator

access_token = os.getenv('MEDIUM_ACCESS_TOKEN')
endpoint = os.getenv('AZUREAI_ENDPOINT')
credential = os.getenv('AZUREAI_CREDENTIAL')
# client = TextTranslateionClient(endpoint,credential) 
# project_id = os.getenv('GCP_PROJECT_ID')
# GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')


if __name__ == "__main__":
    print("1. Starting scraping process...")

    scraper = Scraper('https://madsblog.net/2024/09/22/tipos-de-migracion-a-la-nube/') # <<<<< <<<<<<<<< SET THE URL 
    scraper.fetch_content()
    content = scraper.html_process()
    print("1. Scraping process finished...")   
    
  # GET content from scraping
    for element in content:
        if element['type'] == "bullet-list": 
            print(f"{element['type']}: {element['content']}\n")

    print("2. Initializing translation process...")   
  # Check AZURE Enviroment Variables
    if not endpoint:
        raise ValueError("No endpoint found in environment variables")
      
    if not credential:
        raise ValueError("No credential found in environment variables")
  
  # Initialize Translator Client - Azure
    translator = Translator_azure(endpoint, credential) ##Client for Azure Translator
        
    # Translate Content
    content_en = []
    print("2. Translation in progress...") 
    for element in content:
        if element['type'] != 'image':  # Skip translation for images
            translated_text = Translator_azure.translate(translator, element['content']) ##Translate Azure AI 
            # translator_gcp = Translator_gcp(element['content'], project_id) ## Translate with GCP Translation API
            # translated_text = translator_gcp.translate_text()
            content_en.append({'type': element['type'], 'content': translated_text})
        else:
            content_en.append(element)  # Add images as-is
    print("2. Translation finished...") 
    
    print("2. Showing translation...") 
    
    for element in content_en:
        print(f"{element['type']}: {element['content']}\n")

    print("3. Converting to Markdown format...") 
        
  # Convert to Markdown
    markdownfile = "output.md"
    converter = Convertmarkdown(content_en, markdownfile)
    markdown_content = converter.convert_to_markdown()
    saved_file = converter.save_to_markdown_file(markdown_content)  # Pass the generated markdown content to the method
    print("3. Finish Markdown format...")  
    print("File saved at:", saved_file)
    
  # Medium publish
    print("4. Medium API its disabled. So only will output the markdown file...")  
    print("5. while we wait for the API to go back online (if some day does) yo can use ChatGPT to output the Mardown output file and paste manually in Medium...") 
    print("6. sorry for the inconvenience :).") 

  #   if not access_token:
  
  #       raise ValueError("No Medium access token found in environment variables")

  #   Medium_publisher = MediumPublisher(access_token)
    
  # # Get content for the file  
  #   with open(saved_file, "r", encoding="utf-8") as file:
  #       file_content = file.read()
  #   print("4. Getting content from:", saved_file)
  # # Prepare Medium publish        
  #   user_id = Medium_publisher.get_user_id()
  #   title = ""
  #   for element in content_en:
  #       if element['type'] == 'title':
  #           title = element['content']
  #           break 
  #   print("4. Posting content to Medium as Draft...")  
  # # Publish
  #   post = Medium_publisher.create_post(user_id, title, file_content)
  #   print("4. Medium post draft was created sucessfully!") 
    