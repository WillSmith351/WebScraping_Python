import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

# URL du site
site_url = "https://www.jeuxvideo.com/forums/42-51-67306968-1-0-1-0-les-meilleures-marques-de-pc-portables.htm"

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

# Vérifier si le contenu a été récupéré avec succès
if html_content:
    # Utiliser BeautifulSoup pour analyser le HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Exemple : Récupérer le titre de la page
    title = soup.title.text.strip()

    # Exemple : Récupérer les pseudos des utilisateurs, la date et le commentaire
    users_data = []
    for post in soup.select('.bloc-message-forum'):
        pseudo = post.select_one('.bloc-pseudo-msg').text.strip()

        # Utilisez '.bloc-date-msg .lien-jv' pour le sélecteur de la date
        post_time_element = post.select_one('.bloc-date-msg .lien-jv')
        post_time = post_time_element.text.strip() if post_time_element else None

        # Utilisez '.bloc-contenu .text-enrichi-forum' pour le sélecteur du commentaire
        comment_element = post.select_one('.bloc-contenu .text-enrichi-forum')
        comment_content = comment_element.text.strip() if comment_element else None

        users_data.append({
            "Pseudo": pseudo,
            "Date": post_time,
            "Contenu du Commentaire": comment_content
        })

    # Utiliser pandas pour créer un DataFrame
    df = pd.DataFrame(users_data)

    # Enregistrer le DataFrame dans un fichier JSON
    output_data = {"Titre de la page": title, "Utilisateurs": df.to_dict(orient='records')}
    output_file = "page_content_with_users_pandas.json"
    
    with open(output_file, "w", encoding="utf-8") as json_file:
        json.dump(output_data, json_file, ensure_ascii=False, indent=2)

    print(f"Contenu de la page avec les utilisateurs enregistré dans {output_file}")
else:
    print("Impossible de récupérer le contenu de la page.")
