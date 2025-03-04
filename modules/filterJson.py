import json
import os

def filter_json(input_file, allowed_values):
    """
    Filters out key-value pairs from a JSON file based on allowed values and saves it to a new file.
    
    :param input_file: Path to the input JSON file.
    :param allowed_values: List of values to retain in the JSON.
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    filtered_data = {key: value for key, value in data.items() if value in allowed_values}
    
    base, ext = os.path.splitext(input_file)
    output_file = f"{base}_copy{ext}"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(filtered_data, f, indent=4, ensure_ascii=False)
    



filter_json("CL_TIPOITTER1.json", [
    "ALL",
    "CPROV",
    "CPROV_MUN",
    "MUN",
    "TOUR",
    "TOUR_HILL",
    "TOUR_HIST_ART",
    "TOUR_LACSTR",
    "TOUR_MOUNT",
    "TOUR_SEASD",
    "TOUR_THRM"
  ])