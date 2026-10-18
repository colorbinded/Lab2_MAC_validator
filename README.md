Перед запуском в терминале папки проекта:
python -m pip install --upgrade pip
python -m pip install -e .

для запуска тестов:
python -m pytest -v

для запуска основной программы:
python -m MAC_validator.validator

для поиска MAC-адреса в файле есть пример файла - examples/network_devices.txt

url с MAC-адресом - https://www.networkcenter.info/inform/mac