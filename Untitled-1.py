import pandas as pd
import requests
from os import path

csv_dataset = pd.read_csv("./csv_dataset.csv", delimiter=";", on_bad_lines='skip',
                          usecols=["dataset.title", "dataset.url", "url", "title"])

lien1 = "https://www.data.gouv.fr/fr/datasets/r/b09da629-e48a-4baa-8d43-9ae28b3248da"
lien2 = "https://www.data.gouv.fr/fr/datasets/r/f4d7c0bd-8dc7-49af-8333-ec9d6abfdbee"
csv1 = "vacsi-pc-a_fra.csv"
csv2 = "covid-cedc-quot.csv"

if path.exists('vacsi-pc-a_fra.csv') == False & path.exists('covid-cedc-quot.csv') == False:
    response = requests.get(lien1)
    csv_file = open(f'./csv/{csv1}', "wb").write(response.content)

    response = requests.get(lien2)
    csv_file2 = open(f'./csv/{csv2}', "wb").write(response.content)
