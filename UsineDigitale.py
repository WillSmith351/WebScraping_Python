import requests
from bs4 import BeautifulSoup
import json


site_url = "https://www.usine-digitale.fr/ordinateur-portable/"

# Fonction pour récupérer le contenu HTML d'une page
def get_page_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"La requête a échoué avec le code d'état {response.status_code}")
        return None

# Récupérer le contenu HTML de la page
html_content = get_page_content(site_url)

# Vérifier si le contenu a été récupéré 
if html_content:
    # Utiliser BeautifulSoup pour analyser le HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Récupérer tous les articles
    articles = soup.select('.editoCardType10__content')

    # Dictionnaire pour stocker le nombre d'articles par mot-clé
    nombre_articles_par_mot_cle = {}

    # Boucler sur tous les articles
    for article in articles:
        
        mots_cles = [tag.text.strip().lower() for tag in article.select('.editoTagType5')]

        # Mettre à jour le dictionnaire
        for mot_cle in mots_cles:
            if mot_cle not in nombre_articles_par_mot_cle:
                nombre_articles_par_mot_cle[mot_cle] = 1
            else:
                nombre_articles_par_mot_cle[mot_cle] += 1

    
    output_data = {"Nombre d'articles par mot-clé": nombre_articles_par_mot_cle}
    output_file = "resultat_articles_par_mot_cle.json"
    
    with open(output_file, "w", encoding="utf-8") as json_file:
        json.dump(output_data, json_file, ensure_ascii=False, indent=2)

    print(f"Résultat enregistré dans {output_file}")
else:
    print("Impossible de récupérer le contenu de la page.")
