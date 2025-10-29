from behave import given, when, then
import logging
import requests


@given("the service is running")
def step_impl(context):
    host = context.online_config['HOST']
    logging.debug(f"Connecting to host: {host}")

    # Ping the service to verify it's running
    try:
        response = requests.get(f"https://{host}/index.html", timeout=5)  
        if response.status_code == 200:
            logging.debug(f"Service is running. ")
        else:
            logging.error(f"Service is not running. Ping returned status code: {response.status_code}")
            raise Exception(f"Service is not running. Status code: {response.status_code}")
    except requests.RequestException as e:
        logging.error(f"Failed to connect to the service: {e}")
        raise Exception(f"Service is not reachable: {e}")


@when("I authenticate as a partner for Orion-LD")
def step_impl(context):
    logging.debug(f"Authenticating with username: {context.online_config['PARTNER_USERNAME']} and password: {context.online_config['PARTNER_PASSWORD']}")

    # Authentication endpoint
    url = f"https://{context.online_config['HOST']}/idm/realms/fiware-server/protocol/openid-connect/token"

    # Prepare payload dynamically
    payload = {
        'username': context.online_config['PARTNER_USERNAME'],
        'password': context.online_config['PARTNER_PASSWORD'],
        'grant_type': 'password',
        'client_id': 'orion-pep',
        'client_secret': context.online_config['ORION_PEP_SECRET']
    }

    # Headers for the request
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    try:
        # Send POST request
        response = requests.post(url, headers=headers, data=payload)
        
        # Check if the request was successful
        if response.status_code == 200:
            logging.debug("Authentication successful.")
            access_token = response.json().get('access_token')
            
            if access_token:
                logging.debug(f"Access token: {access_token}")
                # Store the access token in the context for later use
                context.access_token = access_token
            else:
                logging.error("Access token not found in the response.")
                raise Exception("Authentication failed: Missing access token in response.")
        else:
            logging.error(f"Authentication failed with status code {response.status_code}: {response.text}")
            raise Exception(f"Authentication failed: {response.status_code} - {response.reason}")

    except requests.RequestException as e:
        logging


@then("I should have access to protected resources on Orion-LD")
def step_impl(context):
    # Ensure the access token is available
    assert hasattr(context, "access_token"), "Access token not found in context."
    assert context.access_token, "Access token is empty."

    # API endpoint to access protected resources
    url = f"https://{context.online_config['HOST']}/kong/keycloak-orion/version"

    # Headers with the Bearer token
    headers = {
        'Authorization': f'Bearer {context.access_token}'
    }

    # Send GET request to access the protected resource
    try:
        response = requests.get(url, headers=headers)
        
        # Check if the request was successful
        if response.status_code == 200:
            logging.debug("Access to protected resources successful.")
            
            # Parse the response JSON
            response_json = response.json()
            logging.debug(f"Response JSON: {response_json}")
            
            # Validate response content
            assert "orionld version" in response_json, "Missing 'orionld version' in the response."
            assert "orion version" in response_json, "Missing 'orion version' in the response."
            assert "uptime" in response_json, "Missing 'uptime' in the response."

            # Log specific values
            logging.debug(f"OrionLD Version: {response_json['orionld version']}")
            logging.debug(f"Orion Version: {response_json['orion version']}")
            logging.debug(f"Uptime: {response_json['uptime']}")

            # Store the response in the context for later use
            context.protected_resource_response = response_json
        else:
            logging.error(f"Failed to access protected resources: {response.status_code} - {response.text}")
            raise Exception(f"Failed to access protected resources: {response.status_code} - {response.reason}")

    except requests.RequestException as e:
        logging.error(f"An error occurred while accessing protected resources: {e}")
        raise

@then("the resource response should contain expected version information of Orion-LD")
def step_validate_version_info(context):
    assert hasattr(context, "protected_resource_response"), "Protected resource response not found in context."

    response_json = context.protected_resource_response

    # Validate versions
    assert response_json["orionld version"] == "1.4.0", f"Unexpected OrionLD version: {response_json['orionld version']}"
    assert "next" in response_json["orion version"], f"Unexpected Orion version: {response_json['orion version']}"
    
    # Log additional details
    logging.debug(f"Git Hash: {response_json['git_hash']}")
    logging.debug(f"Release Date: {response_json['release_date']}")