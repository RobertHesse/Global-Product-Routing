import csv
import requests
import xml.etree.ElementTree as ET

def extract_product_urls(sitemap_url):
    product_urls = []
    try:
        response = requests.get(sitemap_url)
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            for url in root.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
                loc = url.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
                if loc is not None:
                    product_urls.append(loc.text)
    except Exception as e:
        print(f"Fehler beim Abrufen oder Parsen von {sitemap_url}: {e}")
    return product_urls

def filename_from_sitemap_url(sitemap_url):
    parts = sitemap_url.split('/')
    # Domain extrahieren (z.B. "stauff.com.br" aus der URL)
    domain_part = parts[2].replace('www.', '').replace('.com', '')
    # Dateiname-Komponente aus der URL extrahieren und Domain hinzufügen
    filename_part = parts[-1].replace('sitemap-product-', '').replace('.xml', '')
    # Dateinamen unter Einbeziehung von Domain, Land und Sprache erstellen
    return f'data/{domain_part}_produkte_{filename_part}.csv'

def read_sitemaps_csv_and_write_products():
    with open('shops_sitemaps.csv', mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            product_sitemap_url = row['Product Sitemap URL']
            product_urls = extract_product_urls(product_sitemap_url)
            
            if product_urls:
                filename = filename_from_sitemap_url(product_sitemap_url)
                with open(filename, mode='w', newline='', encoding='utf-8') as product_file:
                    writer = csv.writer(product_file)
                    writer.writerow(['Product URL'])
                    for product_url in product_urls:
                        writer.writerow([product_url])
                print(f"Produkt-URLs geschrieben nach: {filename}")

read_sitemaps_csv_and_write_products()
