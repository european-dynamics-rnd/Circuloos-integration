import logging
import os

def load_config(file_path):
    config_dict = {}
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()  # Remove leading/trailing whitespace
            if line and "=" in line:  # Skip empty lines or lines without '='
                key, value = line.split("=", 1)  # Split into key and value
                config_dict[key.strip()] = value.strip()  # Add to dictionary
    return config_dict


def before_all(context):
    # Load the .env file

    file_path =  os.path.dirname(os.path.abspath(__file__))+'/partner_variables.txt'  # Replace with the path to your file
    config = load_config(file_path)
    context.online_config=config

    print("Loaded Environment Variables:")
    print("HOST:", context.online_config["HOST"])
    print("PARTNER_USERNAME:", context.online_config["PARTNER_USERNAME"])
    print("PARTNER_PASSWORD:",context.online_config["PARTNER_PASSWORD"])
    print("ORION_PEP_SECRET:", context.online_config["ORION_PEP_SECRET"])
    print("MIKTAKA_PEP_SECRET:", context.online_config["MIKTAKA_PEP_SECRET"])
    if not context.config.log_capture:
        logging.basicConfig(level=logging.INFO) # INFO DEBUG
