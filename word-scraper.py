import requests
from bs4 import BeautifulSoup
import time

BASE_URL = "https://en.wiktionary.org/"
WIKI_URL = "wiki/"
CATEGORY_URL = BASE_URL + WIKI_URL + "Category:Portuguese_lemmas"
LANG_URL = "#Portuguese"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
#SAVE_INTERVAL = 200
BLOCKED_WORDS = ('Português','eu','tu','ele','ela','você','nós','vós','eles','elas','vocês','não')

def get_words_from_page(url):
    words = []
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        for word in soup.find_all('div', class_='mw-category-group'):
            for a in word.find_all('a'):
              if (str(a.string).isalpha() and str(a.string).islower()):
                new_word = a.string
                words.append(new_word)
                connected_words = get_connected_words(new_word)
                if len(connected_words) > 0:
                  words.append('###############')
                  words.extend(connected_words)
    return words

def get_connected_words(word):
    connected_words = []
    url = BASE_URL + WIKI_URL + word
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
      connected_soup = BeautifulSoup(response.content, 'html.parser')
      for line in connected_soup.find_all(lang='pt'):
        if line.string is not None and line.string.isalpha() and line.string not in BLOCKED_WORDS and line.string not in connected_words:
          connected_words.append(line.string)
    else: 
      print(response.status_code)
    return connected_words

def get_next_page(soup):
    next_page = soup.find('a', string='next page')
    if next_page:
        return BASE_URL + next_page['href']
    return None

def save_words_to_file(words, file_path="portuguese_words.txt"):
    with open(file_path, "a", encoding="utf-8") as f:
        for word in words:
            if word is not None:
                f.write(f"{word}\n")
    print(f"Saved {len(words)} words to {file_path}")

def save_last_url(url, file_path="last_word_found.txt"):
   with open(file_path, "w", encoding="utf-8") as f:
        if url is not None:
            f.write(url)

def get_last_url(file_path="last_word_found.txt"):
   with open(file_path, "r", encoding="utf-8") as f:
        return f.readline()

def scrape_portuguese_words(start_url):
    words = []
    #next_word = get_last_word()
    next_url = get_last_url()
    if next_url == '':
      next_url = start_url
       
    total_words = 0
    #counter = 0
    while next_url:
    #while counter < 10:
        print('searching inside - ', next_url)
        response = requests.get(next_url, headers=HEADERS)
        if response.status_code != 200:
            break
        
        soup = BeautifulSoup(response.content, 'html.parser')
        words_on_page = get_words_from_page(next_url)
        words.extend(words_on_page)
        total_words += len(words_on_page)
        print(f"Scraped {len(words_on_page)} words from {next_url}")
        
        next_url = get_next_page(soup)

        # Periodically save words to file
        #if len(words) >= SAVE_INTERVAL:
        save_last_url(next_url)
        save_words_to_file(words)
        
        words = []  # Reset the list to free memory

        # Respectful scraping: delay between requests
        time.sleep(1)
        #counter += 1
    
    # Save any remaining words
    if words:
        save_words_to_file(words)
    
    return total_words

if __name__ == "__main__":
    file = open('portuguese_words.txt') 
    file.close()     
    total_words_scraped = scrape_portuguese_words(CATEGORY_URL)
    print(f"Total words scraped: {total_words_scraped}")