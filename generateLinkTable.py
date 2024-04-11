import csv
import os
import re

def extract_product_number(url):
    match = re.search(r'(\d+)$', url)
    if match:
        return match.group(1)
    return None

def domain_language_from_filename(filename):
    # Extrahiert den Domain- und Sprachteil aus dem Dateinamen
    # Dateinamenformat: domain_produkte_country_language.csv
    parts = filename.split('_')
    if len(parts) >= 4:
        domain = parts[0]
        language = parts[-1].replace('.csv', '')
        return f"{domain}_{language}"
    return "unbekannt"

def aggregate_product_links():
    product_links = {}
    headers_set = set()
    for filename in os.listdir('.'):
        if filename.endswith('.csv') and 'produkte_' in filename:
            domain_language = domain_language_from_filename(filename)
            headers_set.add(domain_language)
            with open(filename, mode='r', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                next(csv_reader)  # Überspringen der Kopfzeile
                for row in csv_reader:
                    product_url = row[0]
                    product_number = extract_product_number(product_url)
                    if product_number:
                        if product_number not in product_links:
                            product_links[product_number] = {}
                        product_links[product_number][domain_language] = product_url
    headers = sorted(list(headers_set))
    return product_links, headers

def write_final_table(product_links, headers):
    with open('data/final_product_table.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Produktnummer'] + headers)
        
        for product_number, links in sorted(product_links.items()):
            row = [product_number] + [links.get(header, '') for header in headers]
            writer.writerow(row)

product_links, headers = aggregate_product_links()
write_final_table(product_links, headers)
