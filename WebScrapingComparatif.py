import requests
from bs4 import BeautifulSoup
from collections import Counter
import json
import re
from nltk.corpus import stopwords


website = "https://www.lesnumeriques.com/ordinateur-portable/comparatif-ordinateurs-portables-pc-mac-a449.html"
response = requests.get(website)
data = {}

if response.status_code == 200:

    soup = BeautifulSoup(response.content, 'html.parser')
    text = soup.get_text()
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\b(?:19|20)\d{2}\b', '', text)
    words = text.lower().split()
    stop_words = set(stopwords.words('french'))
    words = [mot for mot in words if mot not in stop_words]
    word_count = Counter(words)
    most_common_words = word_count.most_common(50)
    frequent_words_data = [{'mot': word, 'occurrences': count} for word, count in most_common_words]
    data['mots_frequents'] = frequent_words_data



    title = soup.find('title')
    if title:
        data['titre_page'] = title.text.strip()

    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

else:
    print("La requête a échoué. Statut de la réponse :", response.status_code)
