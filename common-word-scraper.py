import requests
from bs4 import BeautifulSoup
import re
from collections import Counter
import time

# Function to fetch article links from a category page
def fetch_article_links(category_url, max_articles=3):
    response = requests.get(category_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    #print(str(soup))
    article_links = []
    for link in soup.find_all("a"):
        if len(article_links) >= max_articles:
            break
        if link.get('href') is None:
            break
        article_links.append("https://pt.wikipedia.org" + link.get('href'))
    
    return article_links

# Function to fetch the text of a Wikipedia article
def fetch_article_text(article_url):
    try:
        response = requests.get(article_url)
        response.raise_for_status()  # This will raise an HTTPError for bad responses
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract paragraphs
        paragraphs = soup.select('p')
        text = " ".join([para.get_text() for para in paragraphs])
        return text
    except requests.RequestException as e:
        print(f"Failed to fetch {article_url}: {e}")
        return ""

# Function to clean and tokenize text
def clean_and_tokenize(text):
    text = re.sub(r'[^a-zA-ZáéíóúãõçÁÉÍÓÚÃÕÇ\s]', '', text).lower()
    words = text.split()
    return words

# Function to count word frequencies
def count_word_frequencies(words):
    return Counter(words)

# Function to get the top N words
def get_top_n_words(word_frequencies, n):
    return word_frequencies.most_common(n)

# Function to save words to a text file
def save_words_to_file(word_frequencies, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        for word, freq in word_frequencies:
            f.write(f"{word}: {freq}\n")


# Constants
PICKLE_FILENAME = 'word_frequencies.pkl'
TEXT_FILENAME = 'top_20000_words.txt'
SAVE_INTERVAL = 10  # Save after processing every 10 articles

if __name__ == '__main__':
    word_frequencies = Counter()
    category_url = "https://pt.wikipedia.org/wiki/Brasil"
    article_links = fetch_article_links(category_url, max_articles=10)

    all_words = []
    for index, article_url in enumerate(article_links):
        print(f"Fetching article: {article_url}")
        article_text = fetch_article_text(article_url)
        if article_text:  # Only process if the article was fetched successfully
            cleaned_words = clean_and_tokenize(article_text)
            word_frequencies.update(cleaned_words)
        
        # Periodically save the word frequencies
        #if (index + 1) % SAVE_INTERVAL == 0:
        #    save_word_frequencies(word_frequencies, PICKLE_FILENAME)
        #    print(f"Saved word frequencies after processing {index + 1} articles.")
        
        time.sleep(1)  # Be polite to Wikipedia servers

    # Save the final word frequencies
    #save_word_frequencies(word_frequencies, PICKLE_FILENAME)
    top_20000_words = get_top_n_words(word_frequencies, 20000)

    # Save the top 20,000 words to a text file
    save_words_to_file(top_20000_words, TEXT_FILENAME)
    print(f"Final word frequencies saved to {TEXT_FILENAME}.")