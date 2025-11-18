import logging
import os

def load_config(file_path):
    """Load configuration from file"""
    config_dict = {}
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()  # Remove leading/trailing whitespace
                if line and "=" in line:  # Skip empty lines or lines without '='
                    key, value = line.split("=", 1)  # Split into key and value
                    config_dict[key.strip()] = value.strip()  # Add to dictionary
    return config_dict


def load_config_from_env_and_file(file_path):
    """
    Load configuration from both environment variables and file.
    Priority: Environment variables > File
    """
    # First, load from file if it exists
    config = load_config(file_path)
    
    # Override with environment variables if they exist
    env_vars = {
        "HOST": os.getenv("HOST"),
        "PARTNER_USERNAME": os.getenv("PARTNER_USERNAME"),
        "PARTNER_PASSWORD": os.getenv("PARTNER_PASSWORD"),
        "ORION_PEP_SECRET": os.getenv("ORION_PEP_SECRET"),
        "MIKTAKA_PEP_SECRET": os.getenv("MIKTAKA_PEP_SECRET")
    }
    
    # Update config with environment variables (if they're set)
    for key, value in env_vars.items():
        if value is not None:
            config[key] = value
    
    return config


def before_all(context):
    # Load configuration from both file and environment variables
    file_path = os.path.dirname(os.path.abspath(__file__)) + '/partner_variables.txt'
    context.online_config = load_config_from_env_and_file(file_path)

    print("Loaded Configuration:")
    print("HOST:", context.online_config.get("HOST", "NOT SET"))
    print("PARTNER_USERNAME:", context.online_config.get("PARTNER_USERNAME", "NOT SET"))
    print("PARTNER_PASSWORD:", "***" if context.online_config.get("PARTNER_PASSWORD") else "NOT SET")
    print("ORION_PEP_SECRET:", "***" if context.online_config.get("ORION_PEP_SECRET") else "NOT SET")
    print("MIKTAKA_PEP_SECRET:", "***" if context.online_config.get("MIKTAKA_PEP_SECRET") else "NOT SET")
    
    # Validate that all required variables are set
    required_vars = ["HOST", "PARTNER_USERNAME", "PARTNER_PASSWORD", "ORION_PEP_SECRET", "MIKTAKA_PEP_SECRET"]
    missing_vars = [var for var in required_vars if not context.online_config.get(var)]
    
    if missing_vars:
        raise ValueError(f"Missing required configuration variables: {', '.join(missing_vars)}")
    
    if not context.config.log_capture:
        logging.basicConfig(level=logging.INFO)  # INFO DEBUG
