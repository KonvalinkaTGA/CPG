import sys
import requests
import re


def download_url_and_get_all_hrefs(url):
    """
    Stáhne obsah stránky pomocí requests.get()
    Zkontroluje kód odpovědi (musí být 200).
    Z HTML obsahu najde všechny <a href="..."> odkazy
    a vrátí je jako seznam stringů.
    """
    hrefs = []

    # stáhnutí stránky
    response = requests.get(url)

    # kontrola kódu odpovědi
    if response.status_code != 200:
        raise Exception(f"Server vrátil chybu: HTTP {response.status_code}")

    # obsah stránky (HTML)
    content = response.text

    # najít všechny href="..." odkazy
    matches = re.findall(r'<a\s+[^>]*href="([^"]+)"', content, re.IGNORECASE)

    hrefs.extend(matches)

    return hrefs


if __name__ == "__main__":
    try:
        url = sys.argv[1]
        download_url_and_get_all_hrefs(url)
    # osetrete potencialni chyby pomoci vetve except
    except Exception as e:
        print(f"Program skoncil chybou: {e}")