from modules.dataflowsExtractor import extractDataFlow
from modules.dataStructureExtractor import extractDataStructure
from modules.codeExtractor import extractCodes
import os


dataflow = input("Dataflow: ")
lang = input("Language(en,it): ")

path = os.path.join("extracted", f"{dataflow}_metadata")
csv_dim_path = os.path.join("extracted", f"{dataflow}_metadata", "dim_csv")
json_dim_path = os.path.join("extracted", f"{dataflow}_metadata", "dim_json")

if not os.path.exists(path):
    os.makedirs(path)

if not os.path.exists(csv_dim_path):
    os.makedirs(csv_dim_path)

if not os.path.exists(json_dim_path):
    os.makedirs(json_dim_path)

extractDataFlow(dataflow, lang, path)
extractDataStructure(path)
extractCodes(path, lang)
