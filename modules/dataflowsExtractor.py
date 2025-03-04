# Importa i moduli necessari ElementTree per leggere e estrarre i dati XML
# e json per salvare i risultati in un file json per semplificare poi la lettura
import xml.etree.ElementTree as ET
import json
import requests
import os

def extractDataFlow(dataflow, path):
    # Oggetto dove aggiungo le coppie chiavi-valore da salavare poi in json
    dataflows = {}
    datastructure = ""

    response = requests.get("https://esploradati.istat.it/SDMXWS/rest/dataflow/IT1")

    # Apro il file dove ho salvato la chiamata XML e setto un puntatore al primo livello dei tag XML
    tree = ET.ElementTree(ET.fromstring(response.text))
    root = tree.getroot()

    # sono i namespace di SDMXML che servono per scorrere il file ricevuto
    namespaces = {
        "structure": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure",
        "common": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common"
    }

    # Cerca nel file XML tutti i tag che contengono <structure:Dataflow> e li salva in un array
    matching_elements = root.findall(".//structure:Dataflow", namespaces)

    # cicla tutti i tag salvati
    for elem in matching_elements:
        # mi salvo per ognuno l'id in una variabile perche' corrispondono ai dataflow da cui dovremmo poi estrarre i dati
        id_attr = elem.get("id")
        
        # gli specifico di aggiungere i dati all'oggetto dataflows solo se l'id che mi ero salvato contiene
        # la stringa 122_54 perche' e' la sequenza che corrisponde alla sezione sul turismo
        if id_attr and dataflow in id_attr:
            datastructure = elem.find(".//Ref", namespaces).get("id")
            
            name_elem = elem.find("common:Name", namespaces).text
            
            # salvo nell'oggetto quello che ho trovato in forma id - nome del dataflow
            if name_elem is not None:
                dataflows[id_attr] = name_elem
        

    # salvo in un file json il risultato
    with open(os.path.join(path, "dataflows.json"), "w" ) as json_file:
        json.dump( dataflows , json_file )
    
    with open(os.path.join(path, "datastructure.txt"), "w") as ds_file:
        ds_file.write(datastructure)