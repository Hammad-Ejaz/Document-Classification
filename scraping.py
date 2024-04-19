import re
import requests
from bs4 import BeautifulSoup

def scrape_page_content(url):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract the text content of the page
        page_content = soup.get_text()
        
        # Print or return the content as required
        return page_content
    else:
        print(f"Failed to fetch page content. Status code: {response.status_code}")
        return None


def clean_text(raw_text):
    # Remove excess newlines and whitespace
    cleaned_text = re.sub(r'\s+', ' ', raw_text.strip())
    
    # Remove non-alphanumeric characters except space and period
    cleaned_text = re.sub(r'[^a-zA-Z\s.]', '', cleaned_text)
    
     # Remove duplicate words
    words = cleaned_text.split()
    unique_words = set(words)
    cleaned_text = ' '.join(unique_words)
    
    return cleaned_text

def save_to_file(content, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)

def read_links_from_file(filename):
    links = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                # Remove leading and trailing whitespace and add the link to the list
                links.append(line.strip())
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    return links

# Example usage:
filename = "food-links.txt"  # Change to the name of your text file containing links
link_list = read_links_from_file(filename)
print(link_list)
i = 1
for link in link_list:
# Example usage:
    content = scrape_page_content(link)
    if content:
        cleaned_content = clean_text(content)  # No need to encode here
        print(cleaned_content)
        save_to_file(cleaned_content,  f"food-file{i}.txt")
    i = i + 1
