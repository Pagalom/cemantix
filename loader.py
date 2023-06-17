import requests
import json
import sys

# Lire les mots depuis le fichier frenchWord.txt et stocker dans une liste
if len(sys.argv) == 1:
    with open('french-word-list', 'r') as file:
        words = file.read().splitlines()
else:
    with open(sys.argv[1], 'r') as file:
        words = file.read().splitlines()

# Paramètres de la requête
url = 'https://cemantix.certitudes.org/pedantix/score'
headers = {
    'Host': 'cemantix.certitudes.org',
    'Sec-Ch-Ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
    'Accept': '*/*',
    'Sec-Ch-Ua-Platform': '"Linux"',
    'Sec-Ch-Ua-Mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    'Content-Type': 'application/json',
    'Origin': 'https://cemantix.certitudes.org',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://cemantix.certitudes.org/',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7'
}

# Boucle pour envoyer les requêtes avec les mots variables
for word in words:
    data = {
        'word': word,
        'answer': [word,word]
    }
    response = requests.post(url, headers=headers, json=data)

    # Traitement de la réponse
    if response.status_code == 200:
        response_json = response.json()
        if 'score' in response_json and response_json['score']:
            score = response_json['score']
            if any(isinstance(value, str) for value in score.values()):
                print(f"[valide] : '{word}' : valide")
            else:
                print(f"partiel : '{word}'")
        if 'solved' in response_json and response_json['solved']:
            print(f"[TROUVE] --> '{word}' <-- ")
            exit(1)
    else:
        print(f"Erreur lors de l'envoi de la requête pour le mot '{word}'")
