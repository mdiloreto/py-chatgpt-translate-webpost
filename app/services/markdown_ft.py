import re
import os

class Convertmarkdown:
    def __init__(self, content, filename):
        self.content = content
        self.filename = filename
    
    
    def check_bullet_format(self, current_line, next_line):
        # Check if current line ends with ":" and next line starts with a space
        return current_line.endswith(':') and (not next_line.strip())

    def process_bullets(self, bullet_content):
        bullet_points = bullet_content.split('\n')
        markdown_bullets = ""

        for i in range(len(bullet_points)):
            current_line = bullet_points[i]
            next_line = bullet_points[i + 1] if i + 1 < len(bullet_points) else ""

            if self.check_bullet_format(current_line, next_line):
                markdown_bullets += f"{current_line}\n"  # Add current line without bullet
                if not next_line.strip():
                    continue  # Skip the next line if it's empty or whitespace
            else:
                if current_line.strip():
                    markdown_bullets += f"* {current_line}\n" 
                else:
                    markdown_bullets += f"{current_line}\n"  # Keep empty lines as they are
                    

        return markdown_bullets
    
    # def process_bullets(self, bullet_content):
    #     bullet_points = bullet_content.split('\n')
    #     markdown_bullets = ""
    #     l = 0
    #     for point in bullet_points:
    #         # Count leading spaces to determine the level of indentation
    #         indentation_level = (len(point) - len(point.lstrip(' '))) // 2
    #         formatted_point = point.lstrip()
    #         if formatted_point:
    #             markdown_bullets += f"{'  ' * indentation_level}- {formatted_point}\n"
    #     return markdown_bullets

        
    def convert_to_markdown(self):
        
        markdown_content = ""
        for element in self.content:
            
            if element['type'] == 'title':
                markdown_content += f"# {element['content']}\n\n"          
            if element['type'] == 'heading':
                markdown_content += f"## {element['content']}\n\n"
            elif element['type'] == 'paragraph':
                markdown_content += f"\n{element['content']}\n"
            elif element['type'] == 'image':
                markdown_content += f"![Image]({element['content']})\n\n"
            elif element['type'] == 'code':
                markdown_content += f"\n```\n{element['content']}\n```\n"
            elif element['type'] == 'bullet-list':
                markdown_content += self.process_bullets(element['content']) + "\n"
                markdown_content += "\n"
                
        return markdown_content
    


    def save_to_markdown_file(self, markdown_content):
        full_path = os.path.join(os.getcwd(), self.filename)

        with open(full_path, 'w', encoding='utf-8') as file:
            file.write(markdown_content)
        
        return full_path