import requests
from bs4 import BeautifulSoup


class Scraper: 
    def __init__(self, url):
        self.url = url
        self.soup = None
        
    def fetch_content(self):
        response = requests.get(self.url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        self.soup = BeautifulSoup(response.content, 'html.parser')
        
    def extract_list_items(self, ul):
        ul_list = ul.find('ul')

        return ul_list       

    def html_process(self):
        content_list = []
        
        main_tag = self.soup.find('main', class_='wp-block-group is-layout-flow wp-block-group-is-layout-flow')
        if main_tag:
            for element in main_tag.find_all(True):  # Iterate over all tags within main_tag
                
                # Stop processing if the 'wp-block-comments' class is encountered
                if 'wp-block-comments' in element.get('class', []):
                    break

                ##CHECKEAR
                if element.name == 'h1' and any('wp-block-post-title' in cls for cls in element.get('class', [])):
                    # Process as title
                    content_list.append({'type': 'title', 'content': element.get_text(strip=True)})
                
                elif any('ez-toc' in cls for cls in element.get('class', [])):
                    continue  # Skip this element and move to the next one
                        
                elif 'wp-block-heading' in element.get('class', []):
                    # Process as heading
                    heading_text = ''.join(child for child in element if isinstance(child, str)).strip()
                    content_list.append({'type': 'heading', 'content': heading_text})

                elif element.name == 'p':
                    paragraph_text = element.get_text(strip=True)
                    if paragraph_text.lower() in ['posted', 'siteadmin' ,'in', 'by', 'tags:', 'Comment*', 'name*', 'email*', 'website', 'Save my name, email, and website in this browser for the next time I comment.', 'Δ', '']:
                        continue  # Skip these paragraphs
                    content_list.append({'type': 'paragraph', 'content': paragraph_text})
                  
                elif element.name == 'ul':
                    if element.parent.name == 'li':
                        continue  
                    else:
                        element.find('li')
                        text = element.get_text()
                        content_list.append({'type': 'bullet-list', 'content': text})                                

                elif element.name == 'img':
                    # Process as image
                    content_list.append({'type': 'image', 'content': element.get('src')})

                elif element.name == 'code':
                    # Process as code
                    content_list.append({'type': 'code', 'content': element.get_text()})
                    

        return content_list