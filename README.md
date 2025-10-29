# Integration & Integration Testing Plan for CIRCULOOS

## 1. Executive Summary

This document outlines the Integration and Integration Testing strategy for CIRCULOOS:
- CIRCULOOS Data platform ( Orion-LD Context Broker, Mintaka time-series storage, Keycloak authentication) - ED
- Manufacturing Process Orchestration (MPMS) - ED
- Stakeholder Engagement and Collaboration (RAMP)  - ED
- 3D Digital Twin (SCDT) - CUT
- AI-driven Optimization (SCOPT) - CUT
- Sustainability & Lifecycle Assessment Tool (GRETA) - SUPSI
- CV-based Composition Detection (CVTOOL) - CAN

All components communicate via REST APIs using JSON-LD format, following NGSI-LD standards.
The CIRCULOOS Data platform will be used as a database for all data related to the pilots and project. Even if the pilots have internal system, a copy of those data WILL need to be present on the Data platform.

## 2. Integration Architecture Overview

### 2.1 Component Integration Map


## 3 Integration Strategy

### 3.1 Phased Integration Approach

#### Phase 1: Core Infrastructure 
- Orion-LD Context Broker setup and configuration
- Keycloak authentication service
- Mintaka time-series integration
- Basic connectivity testing

#### Phase 2: Business Components with core Infrastructure
- Manufacturing Process Orchestration (MPMS)
- Stakeholder Engagement and Collaboration (RAMP)
- 3D Digital Twin (SCDT)
- AI-driven Optimization (SCOPT)
- Sustainability & Lifecycle Assessment Tool (GRETA)
- CV-based Composition Detection (CVTOOL)


#### Phase 3: Intra-Business Components 
- Manufacturing Process Orchestration (MPMS) <-> AI-driven Optimization (SCOPT)
- ?Manufacturing Process Orchestration (MPMS) <-> Sustainability & Lifecycle Assessment Tool (GRETA)
- ?AI-driven Optimization (SCOPT) <-> Sustainability & Lifecycle Assessment Tool (GRETA)

#### Phase 4: End-to-End Integration 
- Complete workflow testing
- Performance optimization
- Security hardening

### 3.2 Integration with CIRCULOOS data platform

Prior to any interaction with the CIRCULOOS data platform each component needs to get the a BEARER token from the CIRCULOOS Keycload.
Detailed examples can be found in https://github.com/european-dynamics-rnd/circuloos-data-platform/tree/master/commands_URL

|Component                                  |ShortName|
|-------------------------------------------|---------|
|Manufacturing Process Orchestration        |MPMS     |
|Stakeholder Engagement and Collaboration   |RAMP     |
|3D Digital Twin                            |SCDT     |
|AI-driven Optimization                     |SCOPT    |
|Sustainability & Lifecycle Assessment Tool |GRETA    |
|CV-based Composition Detection             |CVTOOL   |


- NGSI-LD Tenant: circuloos_integration
- Each component replace the COMPONENT with their short name
- Replace timestamp with the current when the the test is done

#### 3.2.1 Reading from the CIRCULOOS data platform
Each component needs to read for the CIRCULOOS data platform the following entity: urn:ngsi-ld:COMPONENT:reading-integration-test-1
Inside the entity there is a random alphanumeric per component. The alphanumeric will be used on the next step. Save the data received from the data platform as ```reading.json```

```json 
{
  "id": "urn:ngsi-ld:CVTOOL:reading-integration-test-1",
  "type": "integration",
  "magic-number": {
    "type": "Property",
    "value": "P5gADFDLM"
  }
}
```
Create a file named reading.json with the data received from the data platform and place it on your corresponding folder under verification

#### 3.2.2 Providing data to the CIRCULOOS data platform

Each component needs to send/POST the following entity on the data platform to verify their ability to read/write on the platform. The id that you need to request is: ```urn:ngsi-ld:COMPONENT:writing-integration-test-1```. Save the json-ld that you will provide to the platform as ```writing.json```

```json
{
    "id": "urn:ngsi-ld:COMPONENT:writing-integration-test-1",
    "type": "integration",
    "leather_type": {
        "type": "Property",
        "value": "animal",
        "observedAt": "2024-08-02T09:26:35Z"
    },
    "kind_of_animal": {
        "type": "Property",
        "value": "pig",
        "observedAt": "2024-08-02T09:26:35Z"
    },
    "leather_type_tanned": {
        "type": "Property",
        "value": "chrome",
        "observedAt": "2024-08-02T09:26:35Z"
    },  "magic-number":
    {
      "type": "Property",
      "value": "P5gADFDLM"
    }
}
```
#### 3.2.3 Reading historical data from the CIRCULOOS data platform
Each component needs to read the historical (Mintaka) data from the platform. The id that you need to request is: ```urn:ngsi-ld:COMPONENT:writing-integration-test-1```. Save the response in a file called ```historical-data.json```


Create a file named writing.json with the data to be send to the data platform and place it on your corresponding folder under verification. Next generate a pull request from both reading.json, writing.json and historical-data.json files.




# 6.3.2 Issue Tracking Template
```markdown
## Issue Details
- **Issue ID**: INT-XXX
- **Component(s)**: [Component names]
- **Severity**: Critical/Major/Minor
- **Test Case**: [Test ID]

## Description
[Detailed description of the issue]

## Steps to Reproduce
1. [Step 1]
2. [Step 2]

## Expected vs Actual
- **Expected**: [Expected behavior]
- **Actual**: [Actual behavior]

## Environment
- **Version**: [Component versions]
- **Test Data**: [Data set used]

## Logs/Screenshots
[Attach relevant logs or screenshots]
```