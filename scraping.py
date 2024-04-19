import re
import requests
from bs4 import BeautifulSoup
import  pandas as pd
import re
import string
from nltk.corpus import stopwords
import nltk

def scrape_page_content(url):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract the title of the page
        title = soup.title.string.strip()
        
        # Extract all links on the page
        links = [link.get('href') for link in soup.find_all('a')]
        
        # Extract the text content of the page
        page_content = soup.get_text()
        
        # Print or return the content as required
        return title, links, page_content
    else:
        print(f"Failed to fetch page content. Status code: {response.status_code}")
        return None, None, None


def clean_text(raw_text):
    # Remove excess newlines and whitespace
    cleaned_text = re.sub(r'\s+', ' ', raw_text.strip())
    
    # Remove non-alphanumeric characters except space and period
    #cleaned_text = re.sub(r'[^a-zA-Z\s.]', '', cleaned_text)
    
    # Convert all alphabets to lowercase
    cleaned_text = cleaned_text.lower()
    
    # Remove punctuation
    #cleaned_text = cleaned_text.translate(str.maketrans('', '', string.punctuation))
    
    # Remove numeric values
    cleaned_text = re.sub(r'\b\d+\b', '', cleaned_text)
    
    # Remove stop words
    stop_words = set(stopwords.words('english'))
    words = cleaned_text.split()
    cleaned_words = [word for word in words if word not in stop_words]
    
    # Remove duplicate words
    unique_words = set(cleaned_words)
    
    # Join the words back into a string
    cleaned_text = ' '.join(unique_words)
    
    return cleaned_text



def save_to_file(content, filename, title=None, links=None):
    if title and links and content:
        # Save all data in a single file
        with open(filename, 'w', encoding='utf-8') as file:
            file.write("Title:\n{}\n\n".format(title))
            file.write("Links:\n")
            for link in links:
                if link is not None:
                    file.write(link + ",")
            file.write("\nContent:\n{}\n".format(content))
    else:
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
i = 7
for link in link_list:
# Example usage:
    title, links, content = scrape_page_content(link)
    if title and links and content:
        print("Title:", title)
        print("Links:", links)
        save_to_file(content,  f"raw-food-file-{i}.txt") # save the raw data in file
        cleaned_content = clean_text(content) 
        print(cleaned_content)
        save_to_file(cleaned_content,  f"clean-food-file-{i}.txt" , title , links) 
        cleaned_words = cleaned_content.split()
        dftaxes =pd.DataFrame({'Text': cleaned_words})
        dftaxes['Category'] = 'Food'
        print(dftaxes)
    i = i + 1
