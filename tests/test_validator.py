# tests/test_validator.py

from MAC_validator import is_valid_mac


# ---------- Тесты через фикстуры из conftest.py ----------
def test_all_valid_fixture_mac_addresses(valid_mac_addresses):
    for address in valid_mac_addresses:
        assert is_valid_mac(address) is True, f"Должен быть корректным: {address!r}"


def test_all_invalid_fixture_mac_addresses(invalid_mac_addresses):
    for address in invalid_mac_addresses:
        assert is_valid_mac(address) is False, f"Должен быть некорректным: {address!r}"
