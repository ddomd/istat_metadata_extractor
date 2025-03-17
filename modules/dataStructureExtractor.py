# Importa i moduli necessari ElementTree per leggere e estrarre i dati XML
import xml.etree.ElementTree as ET
import json
import requests
import os
from tqdm import tqdm


def extractDataStructure(path):
    dimensions = {}

    with open(os.path.join(path, "datastructure.txt")) as struct_file:
        datastructure = struct_file.readline()

    response = requests.get(
        f"https://esploradati.istat.it/SDMXWS/rest/datastructure/IT1/{datastructure}",
        stream=True,
    )

    # inizializza e usa una progress bar con unita' byte
    with tqdm(
        desc=f"Downloading structure {datastructure}", unit="b", unit_scale=True
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
    }

    # Cerca nel file XML tutti i tag che contengono <structure:Dimension> e li salva in un array
    matching_elements = root.findall(".//structure:Dimension", namespaces)

    # cicla tutti i tag salvati
    for elem in matching_elements:
        dimension_name = elem.get("id")

        enumeration = elem.find(".//structure:Enumeration", namespaces)

        # controlla che la lista non sia vuota
        if enumeration is not None:
            # Cerca negli elementi Enumeration la lista di ogni sotto elemento che contiene il tag <Ref>
            ref = enumeration.find(".//Ref", namespaces)
            # prende e stampa l'id di ogni Ref che contiene i codici da usare per le CodeList
            dimensions[dimension_name] = ref.get("id")

    # salvo in un file json il risultato
    with open(os.path.join(path, "dimensions.json"), "w") as write:
        json.dump(dimensions, write)
