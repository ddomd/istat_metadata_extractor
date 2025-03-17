# Importa i moduli necessari ElementTree per leggere e estrarre i dati XML
# e json per salvare i risultati in un file json per semplificare poi la lettura
import xml.etree.ElementTree as ET
import json
import requests
import os
from tqdm import tqdm


def extractDataFlow(to_search, lang, path):
    # Oggetto dove aggiungo le coppie chiavi-valore da salavare poi in json
    dataflows = {}
    datastructure = ""

    response = requests.get(
        "https://esploradati.istat.it/SDMXWS/rest/dataflow/IT1", stream=True
    )

    # inizializza e usa una progress bar con unita' byte
    with tqdm(
        desc=f"Downloading dataflow {to_search}", unit="b", unit_scale=True
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
    all_dataflows = root.findall(".//structure:Dataflow", namespaces)

    matching_elements = [
        dataflow for dataflow in all_dataflows if to_search in dataflow.get("id")
    ]

    datastructure = matching_elements[0].find(".//Ref", namespaces).get("id")

    # cicla tutti i tag salvati
    for elem in matching_elements:
        name_elem = elem.find(f'common:Name[@xml:lang="{lang}"]', namespaces).text

        # salvo nell'oggetto quello che ho trovato in forma id - nome del dataflow
        if name_elem is not None:
            dataflows[elem.get("id")] = name_elem

    # salvo in un file json il risultato
    with open(os.path.join(path, "dataflows.json"), "w", encoding="utf-8") as json_file:
        json.dump(dataflows, json_file)

    with open(os.path.join(path, "datastructure.txt"), "w") as ds_file:
        ds_file.write(datastructure)
