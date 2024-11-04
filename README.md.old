# Translate Blog HTML and Post to Medium

## Description
This project, named "translate-blog-html-and-post-to-medium", automates the translation of HTML blog posts and their publication on Medium. It aims to assist bloggers and content creators in reaching a wider audience by translating and posting their blogs in different languages.

## Features
- Scrapes HTML content from a specified blog post.
- Translates the content using Azure AI Translation services.
- Converts the translated content into Markdown format.
- Publishes the translated post to Medium as a draft.

## Things that will get improved soon: 

- Links detection and convertion. 
- User interface
- Free translation platform alternative to Azure AI

## Prerequisites
- Python 3.x
- Azure AI Translation API key
- Medium API access token

## Installation
1. Clone the repository:

  ```bash
  git clone https://github.com/mdiloreto/translate-blog-html-and-post-to-medium.git
  ```

## Navigate to the directory:

```bash
cd translate-blog-html-and-post-to-medium
pip install -r requirements.txt
```
## Usage

Set the URL in the `main.py` file in line #16:

```bash
scraper = Scraper('https://madsblog.net/2023/11/24/storage-persistente-en-gke/') # <<<<< <<<<<<<<< SET THE URL 
```

Set the necessary environment variables for Azure AI and Medium API tokens. 
```bash
$env:AZUREAI_ENDPOINT='<YOUR_AZUREAI_ENDPOINT>'
$env:AZUREAI_CREDENTIAL='<YOUR_AZUREAI_CREDENTIAL>'
$env:MEDIUM_ACCESS_TOKEN='<YOUR_MEDIUM_ACCESS_TOKEN>'
```

Then, run the main.py script:
```bash
python main.py
```

## File Structure
- `main.py`: Orchestrates the scraping, translation, and posting processes.
- `scraper.py`: Extracts content from HTML blog posts.
- `translator_azureai.py`: Handles text translation using Azure AI.
- `markdown_ft.py`: Converts translated content to Markdown format.
- `publish_medium.py`: Publishes content to Medium.
- `output.md`: The Markdown formatted output file.
- `.gitignore`: Specifies untracked files to ignore.
- `requirements.txt`: Lists the project dependencies.

## Contributing
Contributions are welcome. Please fork the repository and submit pull requests with your changes.

## License
This project is released into the public domain. Anyone is free to use, modify, distribute, or sell it without restrictions.

## Contact
For inquiries or collaborations, please contact [mateoadiloreto@gmail.com].

