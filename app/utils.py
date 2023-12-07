from datetime import datetime
from app.yaml_reader import yaml_provincial_parser,yaml_reader, yaml_link_parser
from fake_useragent import UserAgent
import re


def convert_date_to_en(turkish_date):
    month_mapping = {
    'Ocak': 'January',
    'Şubat': 'February',
    'Mart': 'March',
    'Nisan': 'April',
    'Mayıs': 'May',
    'Haziran': 'June',
    'Temmuz': 'July',
    'Ağustos': 'August',
    'Eylül': 'September',
    'Ekim': 'October',
    'Kasım': 'November',
    'Aralık': 'December'
    }
    for tr_m, en_m in month_mapping.items():
        turkish_date = turkish_date.replace(tr_m,en_m)
    # Convert the string to a datetime object
    date_object = datetime.strptime(turkish_date, "%d %B %Y")
    # Format the datetime object as a string in a different format
    formatted_date = date_object.strftime("%Y-%m-%d")   
    return formatted_date


def get_provincial_plate(site_url):
    provincials = yaml_provincial_parser(yaml_reader("provincials.yaml"))
    match = re.search(r'/([^/]+)-hava-durumu$', site_url)
    if match:
        city_name = match.group(1).capitalize()
        return provincials[city_name]
    else:
        print("Hata: Şehir adı çıkarılamadı.")

def get_havadurumux_links():
    site_links = yaml_link_parser(yaml_reader("havadurumux_links.yaml"))
    return site_links

def get_random_user_agents():
    user = UserAgent()
    headers = {"User-Agent" : user.random}

    return headers


