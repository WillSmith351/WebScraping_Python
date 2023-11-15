import requests
from bs4 import BeautifulSoup
import json
import re

website = "https://www.lesnumeriques.com/ordinateur-portable/comparatif-ordinateurs-portables-pc-mac-a449.html"
response = requests.get(website)
data = {}

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')

    # Récupération de tous les items du site.
    product_cards = soup.find_all('article', class_='pr__i-pr__xs-crd-lght ln__level-one is--compare')

    # Création des différents dictionnaires.
    product_data = []
    brand_count = {}
    stars_count_per_brand = {'5': {}, '4': {}, '3': {}, '2': {}, '1': {}}

    # Récupérer les informations pour chaque item trouvé sur le site.
    for card in product_cards:
        # Création du dictionnaire pour récupérer toutes les données.
        product_info = {}

        # Récupération du nom de l'item.
        product_name = card.find('h3', class_='pr__i-pr__xs-crd-lght__t ln__font--700 ln__body-lg ln__body-md--v-xs')
        if product_name:

            # Découpage du nom pour obtenir la marque et le modèle.
            product_text = product_name.text.strip()
            product_split = product_text.split(' ', 1)

            # Transmettre les données dans deux colonnes différentes.
            product_info['marque'] = product_split[0]
            product_info['modele'] = product_split[1]

            # Compter le nombre de fois où la marque est mentionnée.
            brand = product_split[0]
            if brand in brand_count:
                brand_count[brand] += 1
            else:
                brand_count[brand] = 1

        # Récupération du prix de l'item.
        product_price = card.find('span', class_='ln__font--700')
        if product_price:
            # Nettoyage de la donnée.
            price_text = product_price.text.replace('\xa0', '').strip()

            # Transmettre la donnée dans le fichier JSON.
            product_info['prix'] = price_text

        # Récupération du nombre d'étoiles contenu dans la balise image.
        stars = card.find('img', alt=re.compile(r'Note de la rédaction: (\d) sur 5'))

        if stars:
            stars_count = re.search(r'(\d) sur 5', stars['alt']).group(1)
            product_info['etoiles'] = int(stars_count)

            # Compte le nombre de fois où la marque est mentionnée par rapport à son nombre d'étoiles.
            if stars_count in stars_count_per_brand:
                if brand in stars_count_per_brand[stars_count]:
                    stars_count_per_brand[stars_count][brand] += 1
                else:
                    stars_count_per_brand[stars_count][brand] = 1
            else:
                stars_count_per_brand[stars_count][brand] = 1

        product_data.append(product_info)

    # Créer le classement pour chaque produit.
    sorted_products = sorted(product_data, key=lambda x: x.get('etoiles', 0), reverse=True)
    for idx, product in enumerate(sorted_products):
        product['position'] = idx + 1

    # Transmettre la donnée dans le fichier JSON.
    data['informations_produits'] = sorted_products

    # Récupération du titre du site web.
    title = soup.find('title')
    if title:
        data['titre_page'] = title.text.strip()

    # Calculer les occurrences de chaque marque.
    sorted_brand_count = dict(sorted(brand_count.items(), key=lambda item: item[1], reverse=True))

    # Transmettre les données dans le fichier JSON.
    data['occurrences_marques'] = sorted_brand_count
    data['etoiles_par_marque'] = stars_count_per_brand

    # Ouvrir le fichier JSON afin de transmettre les informations.
    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# Afficher une erreur si la requête HTTP n'a pas fonctionné.
else:
    print("La requête a échoué. Statut de la réponse :", response.status_code)

