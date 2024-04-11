from flask import Flask, request, redirect, render_template
import geoip2.database
import logging

app = Flask(__name__)

GEOIP_DATABASE = 'data/GeoLite2-Country.mmdb'
logging.basicConfig(level=logging.INFO)

product_base_urls = {
    'DE': {
        'de': 'https://stauff.com/de/produkte/',
        'en': 'https://stauff.com/en/products/',
    },
    'AU': {
        'en': 'https://stauff.com.au/en/products/',
    },
    'BR': {
        'en': 'https://stauff.com.br/en/products/',
        'es': 'https://stauff.com.br/es/productos/',
        'pt': 'https://stauff.com.br/pt/produtos/',
    },
    'NZ': {
        'en': 'https://stauff.co.nz/en/products/',
    },
    'GB': {
        'en': 'https://stauff.co.uk/en/products/',
    },
    'FR': {
        'en': 'https://stauff.fr/en/products/',
        'fr': 'https://stauff.fr/fr/produits/',
    },
    'IN': {
        'en': 'https://stauff.in/en/products/',
    },
    'IT': {
        'en': 'https://stauff.it/en/products/',
        'it': 'https://stauff.it/it/prodotti/',
    },
    'RU': {
        'en': 'https://stauff.ru/en/products/',
        'ru': 'https://stauff.ru/ru/produkciya/',
    },
    'CA': {
        'en': 'https://stauffcanada.com/en/products/',
    },
    'US': {
        'en': 'https://www.stauffusa.com/en/products/',
        'es': 'https://www.stauffusa.com/es/productos/',
    },
    'default': {
        'en': 'https://www.stauff.com/en/products/',
    }
}

def get_country_from_ip(ip):
    try:
        with geoip2.database.Reader(GEOIP_DATABASE) as reader:
            response = reader.country(ip)
            return response.country.iso_code
    except Exception as e:
        logging.error(f"Error getting country from IP {ip}: {e}")
        return 'default'

def get_preferred_language(accept_language):
    # Default to English if there's an issue parsing the Accept-Language header
    if not accept_language:
        return 'en'

    try:
        languages = accept_language.split(',')
        parsed_languages = []

        for lang in languages:
            parts = lang.split(';q=')
            if len(parts) == 2:
                lang_code, quality = parts
                quality = float(quality)
            else:
                lang_code = parts[0]
                quality = 1.0  # Default quality

            lang_code = lang_code.split('-')[0]  # Consider only the primary language part
            parsed_languages.append((lang_code, quality))

        # Sort languages based on quality, descending
        parsed_languages.sort(key=lambda x: x[1], reverse=True)

        return parsed_languages[0][0]  # Return the language with the highest quality value
    except Exception as e:
        logging.error(f"Error parsing Accept-Language '{accept_language}': {e}")
        return 'en'

def construct_product_url(product_num, country_code, preferred_language):
    country_urls = product_base_urls.get(country_code, product_base_urls.get('default'))
    base_url = country_urls.get(preferred_language, next(iter(country_urls.values())))
    return f"{base_url}{product_num}"

@app.route('/')
def homepage():
    return render_template('homepage.html')

# Add this mapping to your Flask application
lang_to_country_code = {
    'en': 'gb',  # Assuming 'en' should display the US flag
    'de': 'de',
    'es': 'es',
    'pt': 'pt',
    'fr': 'fr',
    'it': 'it',
    'ru': 'ru',
}

# Modify your redirect_to_product function to use the adjusted mapping
@app.route('/product/<product_num>')
def redirect_to_product(product_num):
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    country_code = get_country_from_ip(ip)
    accept_language = request.headers.get('Accept-Language', '')
    preferred_language = get_preferred_language(accept_language)

    country_urls = product_base_urls.get(country_code, product_base_urls.get('default'))
    # Adjust the language URLs to use the correct flag codes
    language_urls = {lang_to_country_code.get(lang, lang): construct_product_url(product_num, country_code, lang) for lang in country_urls}

    product_url = construct_product_url(product_num, country_code, preferred_language)
    return render_template('redirect.html', product_url=product_url, language_urls=language_urls, wait_time=5)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
