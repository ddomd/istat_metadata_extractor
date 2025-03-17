# Importa i moduli necessari ElementTree per leggere e estrarre i dati XML
# e json per salvare i risultati in un file json per semplificare poi la lettura
import xml.etree.ElementTree as ET
import json
import requests
import csv
from pathlib import Path
import os
from tqdm import tqdm


def extractCodes(path, lang):
    # Oggetto dove aggiungo le coppie chiavi-valore da salavare poi in json
    codes = {}

    with open(os.path.join(path, "dimensions.json"), "r") as file:
        codelist = json.load(file)

    for key in codelist:
        # Create a Path object
        file_path = Path(f"dim_{codelist[key]}.csv")

        # Check if the file exists
        if file_path.exists():
            continue

        response = requests.get(
            f"https://esploradati.istat.it/SDMXWS/rest/codelist/IT1/{codelist[key]}",
            stream=True,
        )

        # inizializza e usa una progress bar con unita' byte
        with tqdm(
            desc=f"Downloading code {codelist[key]}", unit="b", unit_scale=True
        ) as progress:
            content = b""

            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    content += chunk
                    progress.update(len(chunk))

        # Apro il file dove ho salvato la chiamata XML e setto un puntatore al primo livello dei tag XML
        root = ET.fromstring(content.decode(response.encoding or "utf-8"))

        # sono i namespace di SDMXML che servono per scorrere il file ricevuto
        namespaces = {
            "structure": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure",
            "common": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common",
            "xml": "http://www.w3.org/XML/1998/namespace",
        }

        # Cerca nel file XML tutti i tag che contengono <structure:Dataflow> e li salva in un array
        matching_elements = root.findall(".//structure:Code", namespaces)

        # cicla tutti i tag salvati
        for elem in matching_elements:
            # mi salvo per ognuno l'id in una variabile perche' corrispondono ai dataflow da cui dovremmo poi estrarre i dati
            id_attr = elem.get("id")

            # gli specifico di aggiungere i dati all'oggetto codelist solo se l'id che mi ero salvato contiene
            # la stringa 122_54 perche' e' la sequenza che corrisponde alla sezione sul turismo
            name_elem = elem.find(f'common:Name[@xml:lang="{lang}"]', namespaces).text

            # salvo nell'oggetto quello che ho trovato in forma id - nome del dataflow
            if name_elem is not None:
                codes[id_attr] = name_elem

        # salvo in un file json il risultato
        with open(
            os.path.join(path, "dim_json", f"dim_{codelist[key]}.json"), "w"
        ) as write:
            json.dump(codes, write)

        with open(
            os.path.join(path, "dim_csv", f"dim_{codelist[key]}.csv"),
            "w",
            encoding="utf-8",
            newline="",
        ) as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["id", "nome"])
            for key, value in codes.items():
                writer.writerow([key, value])

        codes = {}
