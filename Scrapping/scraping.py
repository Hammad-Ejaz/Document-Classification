import re
import nltk
import requests
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
nltk.download('punkt')

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
        links = [link.string for link in soup.find_all('a')]
        links = preprocess_links(links)
        # Extract the text content of the page
        page_content = soup.get_text()
        
        # Print or return the content as required
        return title, links, page_content
    else:
        print(f"Failed to fetch page content. Status code: {response.status_code}")
        return None, None, None


def preprocess_links(links):
    preprocessed_links = []
    for link in links:
        if(link is not None):
            not_allowed_pattern = r'[^a-zA-Z0-9\s.,!?]+'
            
            preprocessed_link = link.replace('\n', ' ')
  
            # Remove non-allowed characters
            preprocessed_link = re.sub(not_allowed_pattern, '', preprocessed_link)
            
            preprocessed_link = re.sub(r'\s+', ' ', preprocessed_link)
            # Removing any leading or trailing whitespace
            preprocessed_link = preprocessed_link.strip()
            # preprocessed_link = ' '.join(word for word in preprocessed_link.split() if len(word) > 1)
            preprocessed_links.append(preprocessed_link)
    return preprocessed_links

def clean_text(raw_text):
     # Define regex pattern to match only alphabets, numeric values, punctuation marks, and spaces
    not_allowed_pattern = r'[^a-zA-Z0-9\s.,!?]+'
    
    cleaned_text = raw_text.replace('\n', ' ')
    # Remove non-allowed characters
    cleaned_text = re.sub(not_allowed_pattern, '', cleaned_text)
    
    # Remove excess whitespace
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text.strip())
    
    # Convert all alphabets to lowercase
    cleaned_text = cleaned_text.lower()
    
    # Remove numeric values
    cleaned_text = re.sub(r'\b\d+\b', '', cleaned_text)
    
    # Remove stop words
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(cleaned_text)
    cleaned_words = [word for word in words if word not in stop_words]
    
  
    cleaned_text = ' '.join(cleaned_words)
    
    return cleaned_text

def save_to_file(content, filename, title=None, links=None):
    if title and links and content:
        # Save all data in a single file
        with open(filename, 'w', encoding='utf-8') as file:
            file.write("{}\n".format(title))

            filtered_links = []

            for link in links:
                if link and len(link) > 0:
                    filtered_links.append(link)
                
            file.write(",".join(filtered_links))
            file.write("\n{}\n".format(content))
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

def do_topic_scrapping(topic):
    links = read_links_from_file(f'{topic}-links.txt')

    for i in range(len(links)):
        title, links_text, content = scrape_page_content(links[i])
        if title and links and content:
            print("Title:", title)
            print("Links:", links_text)
            save_to_file(content,  f"{topic}\\RawData\\file-{i + 1}.txt") # save the raw data in file
            cleaned_content = clean_text(content) 
            save_to_file(cleaned_content, f"{topic}\\CleanData\\file-{i + 1}.txt" , title , links_text) 

do_topic_scrapping("Food")
do_topic_scrapping("Sport")
#do_topic_scrapping("Travel")