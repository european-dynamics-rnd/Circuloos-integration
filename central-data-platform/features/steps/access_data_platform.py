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
    assert response_json["orionld version"] == "1.7.0", f"Unexpected OrionLD version: {response_json['orionld version']}"
    assert "next" in response_json["orion version"], f"Unexpected Orion version: {response_json['orion version']}"

    # Log additional details
    logging.debug(f"Git Hash: {response_json['git_hash']}")
    logging.debug(f"Release Date: {response_json['release_date']}")


@when("I post a new entity to Orion-LD with the following data:")
def step_post_entity_to_orion(context):
    # Ensure the access token is available
    assert hasattr(context, "access_token"), "Access token not found in context."
    assert context.access_token, "Access token is empty."

    # Parse the table data from the scenario
    assert context.table, "Table data not provided in the scenario."

    # Get the first row of data
    row = context.table[0]
    entity_id = row['id']
    entity_type = row['type']
    entity_name = row['name']

    # Construct the NGSI-LD entity payload
    entity_payload = {
        "id": entity_id,
        "type": entity_type,
        "name": {
            "type": "Property",
            "value": entity_name
        },
        "@context": [
            "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
        ]
    }

    # API endpoint to post entity
    url = f"https://{context.online_config['HOST']}/kong/keycloak-orion/ngsi-ld/v1/entities"

    # Headers with the Bearer token and content type
    headers = {
        'Authorization': f'Bearer {context.access_token}',
        'Content-Type': 'application/ld+json'
    }

    # Send POST request to create the entity
    try:
        logging.debug(f"Posting entity to Orion-LD: {entity_payload}")
        response = requests.post(url, headers=headers, json=entity_payload)

        # Store the response in context for later validation
        context.post_response = response
        context.entity_id = entity_id
        context.entity_already_exists = False

        if response.status_code in [201, 204]:
            logging.debug(f"Entity created successfully. Status code: {response.status_code}")
        elif response.status_code == 409:
            # Handle "AlreadyExists" error - not considered a failure
            try:
                error_response = response.json()
                if error_response.get('type') == 'https://uri.etsi.org/ngsi-ld/errors/AlreadyExists':
                    logging.debug(f"Entity '{entity_id}' already exists. This is not an error - continuing test.")
                    context.entity_already_exists = True
                else:
                    logging.error(f"Conflict error: {response.status_code} - {response.text}")
            except ValueError:
                logging.error(f"Failed to parse error response: {response.text}")
        else:
            logging.error(f"Failed to create entity: {response.status_code} - {response.text}")

    except requests.RequestException as e:
        logging.error(f"An error occurred while posting entity: {e}")
        raise


@then("the entity should be created successfully in Orion-LD")
def step_validate_entity_creation(context):
    assert hasattr(context, "post_response"), "Post response not found in context."

    # Check if the entity was created (status code 201 or 204) or already exists (409 with AlreadyExists)
    if context.post_response.status_code in [201, 204]:
        logging.debug(f"Entity with ID '{context.entity_id}' was created successfully.")
    elif context.post_response.status_code == 409 and hasattr(context, 'entity_already_exists') and context.entity_already_exists:
        logging.debug(f"Entity with ID '{context.entity_id}' already exists - test can proceed.")
    else:
        assert False, \
            f"Entity creation failed with status code: {context.post_response.status_code} - {context.post_response.text}"


@then("I should be able to retrieve the entity from Orion-LD")
def step_retrieve_entity(context):
    # Ensure the access token and entity ID are available
    assert hasattr(context, "access_token"), "Access token not found in context."
    assert hasattr(context, "entity_id"), "Entity ID not found in context."

    # API endpoint to retrieve the entity
    url = f"https://{context.online_config['HOST']}/kong/keycloak-orion/ngsi-ld/v1/entities/{context.entity_id}"

    # Headers with the Bearer token
    headers = {
        'Authorization': f'Bearer {context.access_token}',
        'Accept': 'application/ld+json'
    }

    # Send GET request to retrieve the entity
    try:
        logging.debug(f"Retrieving entity from Orion-LD: {context.entity_id}")
        response = requests.get(url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            entity = response.json()
            logging.debug(f"Retrieved entity: {entity}")

            # Validate the entity matches what we posted
            assert entity['id'] == context.entity_id, \
                f"Entity ID mismatch: expected {context.entity_id}, got {entity['id']}"

            logging.debug(f"Successfully retrieved entity '{context.entity_id}' from Orion-LD")
        else:
            logging.error(f"Failed to retrieve entity: {response.status_code} - {response.text}")
            raise Exception(f"Failed to retrieve entity: {response.status_code} - {response.reason}")

    except requests.RequestException as e:
        logging.error(f"An error occurred while retrieving entity: {e}")
        raise