import requests
import hashlib
import random
from bs4 import BeautifulSoup

def simple_hash(string):
    # Преобразуем строку в байты
    string_bytes = string.encode('utf-8')
    
    # Создаем хэш-объект
    hash_object = hashlib.sha256(string_bytes)
    
    # Получаем хэш в шестнадцатичном формате
    hash_hex = hash_object.hexdigest()[:8]
    print(f"HASH : {hash_hex}")
    return str(hash_hex)

def get_live_football_matches():
    # Получаем HTML-код страницы
    response = requests.get("https://matchtv.ru/football/live")
    if response.status_code != 200:
        print(f"Ошибка при загрузке страницы: {response.status_code}")
        return []

    # Парсим HTML-код с помощью BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Находим секцию с живыми матчами
    matches_section = soup.find_all('div', class_='broadcast__item')

    # Извлекаем информацию о матчах
    upcoming_matches = []
    for match in matches_section[:5]:  # Берем только первые 5 матчей
        time = match.find('span', class_='broadcast__time').get_text(strip=True)
        detail = match.find('a', class_='broadcast__link').get_text(strip=True).replace('Футбол.', '').strip()
        upcoming_matches.append({'detail': detail, 'id': simple_hash(detail)})

    return upcoming_matches

# Пример использования
matches = get_live_football_matches()
# for match in matches:
#     print(f"{match['time']}: {match['teams']}")
