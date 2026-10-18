# src/MAC_validator/validator.py
"""Проверка и поиск синтаксически корректных MAC-адресов"""

import re
from pathlib import Path
from collections.abc import Sequence
from urllib.parse import urlparse

import requests

# Поддерживаемые записи:
# 00:1A:2B:3C:4D:5E, 00-1A-2B-3C-4D-5E и 001A.2B3C.4D5E
# Для шестнадцатеричных цифр допустимы заглавные и строчные латинские буквы
_MAC_PATTERN = re.compile(
    r"(?<![0-9A-Fa-f])"
    r"(?:"
    r"(?:[0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}"
    r"|(?:[0-9A-Fa-f]{2}-){5}[0-9A-Fa-f]{2}"
    r"|(?:[0-9A-Fa-f]{4}\.){2}[0-9A-Fa-f]{4}"
    r")"
    r"(?![0-9A-Fa-f])"
)


def is_valid_mac(address: str) -> bool:
    """Вернуть True, если вся строка соответствует поддерживаемому формату MAC"""
    if not isinstance(address, str) or not address:
        return False
    return _MAC_PATTERN.fullmatch(address) is not None


def find_mac_addresses(text: str) -> list[str]:
    """Найти в тексте все поддерживаемые MAC-адреса без повторов"""
    if not isinstance(text, str) or not text:
        return []

    found = _MAC_PATTERN.findall(text)
    return list(dict.fromkeys(found))


def search_file(file_path: str | Path) -> list[str]:
    """Прочитать UTF-8-файл и вернуть найденные в нём MAC-адреса

        OSError: если файл нельзя открыть или прочитать
        UnicodeError: если содержимое не удаётся декодировать как UTF-8
    """
    content = Path(file_path).read_text(encoding="utf-8")
    return find_mac_addresses(content)


def search_url(url: str, timeout: float = 10.0) -> list[str]:
    """Загрузить HTTP(S) страницу и найти MAC-адреса в её тексте

        ValueError: если URL не содержит схему HTTP(S) и сетевой адрес
        requests.RequestException: при сетевой ошибке или HTTP-ошибке
    """
    if not isinstance(url, str):
        raise ValueError("URL должен быть строкой")

    parsed_url = urlparse(url)
    if parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
        raise ValueError("Укажите полный URL, начинающийся с http:// или https://")

    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    return find_mac_addresses(response.text)


def _print_results(addresses: Sequence[str]) -> None:
    """Вывести список найденных адресов или сообщение об отсутствии совпадений"""
    if not addresses:
        print("MAC-адреса не найдены")
        return

    print(f"Найдено уникальных MAC-адресов: {len(addresses)}")
    for address in addresses:
        print(f"- {address}")


def main() -> None:
    while True:
        print("\n=== MAC-валидатор ===")
        print("1. Проверить один MAC-адрес")
        print("2. Найти MAC-адреса в тексте")
        print("3. Найти MAC-адреса в файле")
        print("4. Найти MAC-адреса на веб-странице по URL")
        print("0. Выход")
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            address = input("Введите MAC-адрес: ")
            if is_valid_mac(address):
                print("MAC-адрес синтаксически корректен.")
            else:
                print("Некорректный MAC-адрес.")
        elif choice == "2":
            _print_results(find_mac_addresses(input("Введите текст: ")))
        elif choice == "3":
            file_path = input("Путь к UTF-8-файлу: ").strip()
            try:
                _print_results(search_file(file_path))
            except (OSError, UnicodeError) as error:
                print(f"Не удалось прочитать файл: {error}")
        elif choice == "4":
            url = input("Введите URL веб-страницы: ").strip()
            try:
                _print_results(search_url(url))
            except (ValueError, requests.RequestException) as error:
                print(f"Не удалось обработать URL: {error}")
        elif choice == "0":
            print("Работа программы завершена.")
            return
        else:
            print("Неизвестная команда. Выберите пункт от 0 до 4.")


if __name__ == "__main__":
    main()
