import requests
import xml.etree.ElementTree as ET
import csv

# Sitemaps URLs
sitemap_urls = [
    "https://stauff.com.br/sitemap.xml",
    "https://stauff.fr/sitemap.xml",
    "https://stauff.com/sitemap.xml",
    "https://www.stauffusa.com/sitemap.xml",
    "https://stauff.co.uk/sitemap.xml",
    "https://stauff.com.au/sitemap.xml",
    "https://stauff.co.nz/sitemap.xml",
    "https://stauffcanada.com/sitemap.xml",
    "https://stauff.ru/sitemap.xml",
    "https://stauff.it/sitemap.xml",
    "https://stauff.in/sitemap.xml"
]

# Funktion, um Produkt-Sitemaps zu extrahieren
def extract_product_sitemaps(url):
    product_sitemaps = []
    try:
        response = requests.get(url)
        root = ET.fromstring(response.content)
        for sitemap in root.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}sitemap'):
            loc = sitemap.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
            if loc is not None and 'sitemap-product' in loc.text:
                product_sitemaps.append(loc.text)
    except Exception as e:
        print(f"Error fetching or parsing {url}: {e}")
    return product_sitemaps

# Hauptlogik, um Produkt-Sitemaps zu sammeln, Sprach- und Länderinformationen zu extrahieren und in CSV zu schreiben
with open('data/shops_sitemaps.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Shop URL', 'Product Sitemap URL', 'Country', 'Language'])
    for sitemap_url in sitemap_urls:
        product_sitemaps = extract_product_sitemaps(sitemap_url)
        for product_sitemap in product_sitemaps:
            # Sprach- und Ländercode extrahieren
            parts = product_sitemap.split('-')
            if len(parts) > 2:
                language_country_code = parts[-2]
                country, language = language_country_code.split('_')
            else:
                country = language = 'Unknown'
            writer.writerow([sitemap_url, product_sitemap, language, country])
