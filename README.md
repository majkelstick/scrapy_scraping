

## Utworzenie środowiska wirtualnego

### Windows

`
python -m venv venv
`

`
.\venv\Scripts\activate
`

`
pip install Scrapy
`

Może być dodatkowo konieczne dodanie uprawnień do wykonywania skryptów jeśli korzystasz z PyCharma:

`
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted
`

### Linux

`
python -m venv venv
`

`
source venv/bin/activate
`

`
pip install Scrapy
`

## Scrapy - jak korzystać

Utworzenie nowego projektu:

`
scrapy startproject nazwa_projektu
`

Korzystanie ze Scrapy'iego w shellu:

`
scrapy shell 'https://www.example.com'
`

Uruchomimenie spidera:

`
scrapy crawl spider_name [-o output_file] [-a arg1=value1 arg2=value2]
`


## Zadania

### 1. Korzystając z odpowiedniego selektora wypisz wszystkie tytuły artykułów z https://www.nytimes.com/section/world

### 2. Stwórz nowy projekt i napisz spider'a, który będzie odwiedzał każdy napotkany link. Pająk ma zapisywać wyniki jako Itemy zawierające jedno pole: URL. 

### 3. Do napisanego w zadaniu drugim Itemu dodaj dodatkowe pole: domena. Dodaj w spiderze opcje zapisywania domeny, a następnie napisz pipeline, który w osobnym pliku będzie zapisywał nazwy odwiedzonych domen. Nazwy nie powinny się powtarzać.

https://www.nytimes.com/section/world - URL

www.nytimes.com - domena

Podpowiedź:

`
from urllib.parse import urlparse
`

`
parsed_uri = urlparse(response.url)
`

`
domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
`
