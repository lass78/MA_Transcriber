import requests
from bs4 import BeautifulSoup

# Indsæt URL for DR hjemmesiden
url = "https://www.dr.dk"

# Send en HTTP GET-forespørgsel til hjemmesiden og modtag svar
response = requests.get(url)

# Kontroller, at forespørgslen var succesfuld
if response.status_code == 200:
    # Hvis ja, lav en BeautifulSoup-objekt, der indeholder HTML-indholdet fra hjemmesiden
    soup = BeautifulSoup(response.content, "html.parser")

    # Find alle billeder på hjemmesiden ved at bruge BeautifulSoup's find_all()-metode
    images = soup.find_all("img")

    # Loop gennem billederne og download dem en efter en
    for image in images:
        # Hent URL'en til billedet
        img_url = image["src"]
        # Send en HTTP GET-forespørgsel til billedet og modtag svar
        img_response = requests.get(img_url)
        # Kontroller, at forespørgslen var succesfuld
        if img_response.status_code == 200:
            # Hvis ja, lav et nyt filnavn til billedet baseret på URL'en
            img_name = img_url.split("/")[-1]
            # Åben en ny fil i skriv-tilstand
            with open(img_name, "wb") as f:
                # Skriv indholdet af billedet til filen
                f.write(img_response.content)