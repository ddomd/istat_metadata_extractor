# Importa i moduli necessari ElementTree per leggere e estrarre i dati XML
# e json per salvare i risultati in un file json per semplificare poi la lettura
import xml.etree.ElementTree as ET
import json

# Oggetto dove aggiungo le coppie chiavi-valore da salavare poi in json
codelist = {}

filename = input("filename:")

# Apro il file dove ho salvato la chiamata XML e setto un puntatore al primo livello dei tag XML
tree = ET.parse(f"{filename}.xml")
root = tree.getroot()

# sono i namespace di SDMXML che servono per scorrere il file ricevuto
namespaces = {
    "structure": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure",
    "common": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common"
}

# Cerca nel file XML tutti i tag che contengono <structure:Dataflow> e li salva in un array
matching_elements = root.findall(".//common:KeyValue", namespaces)

# cicla tutti i tag salvati
for elem in matching_elements:
    # mi salvo per ognuno l'id in una variabile perche' corrispondono ai dataflow da cui dovremmo poi estrarre i dati
    id_attr = elem.get("id")
    codelist[id_attr] = []
    # gli specifico di aggiungere i dati all'oggetto codelist solo se l'id che mi ero salvato contiene
    # la stringa 122_54 perche' e' la sequenza che corrisponde alla sezione sul turismo
    name_elem = elem.findall("common:Value", namespaces)

    
    if name_elem is not None:
        for value in name_elem:
        # salvo nell'oggetto quello che ho trovato in forma id - nome del dataflow
            codelist[id_attr].append(value.text)

# salvo in un file json il risultato
with open( f"{filename}.json" , "w" ) as write:
    json.dump( codelist , write )