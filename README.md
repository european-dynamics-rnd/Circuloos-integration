# Integration & Integration Testing Plan for CIRCULOOS

## 1. Executive Summary

This document outlines the Integration and Integration Testing strategy for CIRCULOOS:
- CIRCULOOS Data platform (CDP) ( Orion-LD Context Broker, Mintaka time-series storage, Keycloak authentication) - ED
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

![CIRCULOOS Platform Architecture](./CIRCULOOS_integration.png)


## 3 Integration Strategy

### 3.1 Phased Integration Approach

#### Phase 1: Business Components with core Infrastructure (CIRCULOOS data platform)

- Manufacturing Process Orchestration (MPMS)
- Stakeholder Engagement and Collaboration (RAMP)
- 3D Digital Twin (SCDT)
- AI-driven Optimization (SCOPT)
- Sustainability & Lifecycle Assessment Tool (GRETA)
- CV-based Composition Detection (CVTOOL)

#### Phase 2: Intra-Business Components
Circular Supply chain testing
- SCOPT <-> CDP <-> GRETA
- MPMS <-> CDP <-> SCOPT
- CVTOOL <-> CDP <-> MPMS

#### Phase 3: End-to-End Integration 
- Complete workflow testing
- Performance optimization
- Security hardening

### 3.2 Integration Phase 1 with CIRCULOOS data platform

Prior to any interaction with the CIRCULOOS data platform each component needs to get a BEARER token from the CIRCULOOS Keycloak.
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
- Each component should replace COMPONENT with their short name
- Replace timestamp with the current timestamp when the test is done

#### 3.2.1 Reading from the CIRCULOOS data platform
Each component needs to read from the CIRCULOOS data platform the following entity:

 ```urn:ngsi-ld:COMPONENT:reading-integration-test-1```

Inside the entity there is a random alphanumeric value for each component. The alphanumeric value will be used in the next step. Save the data received from the data platform as ```reading.json```

```json 
{
  "id": "urn:ngsi-ld:ORION:reading-integration-test-1",
  "type": "integration",
  "magic-number": {
    "type": "Property",
    "value": "P5gADFDLM"
  }
}
```
Create a file named reading.json with the data received from the data platform and place it on your corresponding folder under verification-phase-1

#### 3.2.2 Providing data to the CIRCULOOS data platform

Each component needs to send/POST the following entity on the data platform to verify their ability to read/write on the platform. The id that you need to request is: 

```urn:ngsi-ld:COMPONENT:writing-integration-test-1```.

 Save the json-ld that you will provide to the platform as ```writing.json```. **IMPORTANT** Replace the magic-number with the alphanumeric value received from the previous task and change the observedAt to the current data-time.

```json
{
    "id": "urn:ngsi-ld:ORION:writing-integration-test-1",
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
    },
    "magic-number":
    {
      "type": "Property",
      "value": "P5gADFDLM",
      "observedAt": "2025-10-02T09:26:35Z"
    }
}
```
#### 3.2.3 Reading historical data from the CIRCULOOS data platform

Each component needs to read the historical (Mintaka) data from the platform. The id that you need to request is: ```urn:ngsi-ld:COMPONENT:writing-integration-test-1```. Save the response in a file called ```historical-data.json```

Create a file named writing.json with the data to be sent to the data platform and place it on your corresponding folder under verification-phase-1 folder. Next generate a pull request from both reading.json, writing.json and historical-data.json files.

See also under the folder verification-phase-1/example for an example. 

#### 3.2.4 Postman

Also there is a [Postman collection](./verification-phase-1/example/ED%20CIRCULOOS%20Platform%20Integration%20Testing.postman_collection.json). See the variables to change the PARTNER_USERNAME and PARTNER_PASSWORD

## 3.3 Open calls

All the open calls will need to be able to read/write to the data platform. You will need to change the COMPONENT part of the ID with with your PARTNER_USERNAME.

So if your PARTNER_USERNAME is circuloos-european_dynamics, the ID that you need to read is:  
```urn:ngsi-ld:circuloos-european_dynamics:reading-integration-test-1```

You will not need to upload anything to the GitHub, but you will need to include relevant screenshot to your specific deliverable. Please remember to remove/hide your PARTNER_PASSWORD from any screenshot.


## 4. Issue Tracking and Resolution

### 4.1 Issue Management Process

All integration issues will be tracked using GitHub Issues in the project repository. The workflow follows these steps:

#### 4.1.1 Issue Creation
1. **Identify the Issue**: During integration testing, when an issue is discovered, create a new GitHub Issue immediately
2. **Use Labels**: Apply appropriate labels:
   - `integration` - For all integration-related issues
   - `bug` - For defects or errors
   - `enhancement` - For improvement requests
   - `documentation` - For documentation issues
   - `critical` / `high` / `medium` / `low` - For priority levels
   - Component labels: `MPMS`, `RAMP`, `SCDT`, `SCOPT`, `GRETA`, `CVTOOL`, `data-platform`
3. **Assign Responsibility**: Assign to the partner responsible for the affected component
4. **Set Milestone**: Link to the appropriate project phase milestone

#### 4.1.2 Issue Tracking Workflow
1. **Open** - Issue created and awaiting triage
2. **In Progress** - Partner is actively working on the issue
3. **Testing** - Fix implemented and ready for verification
4. **Closed** - Issue resolved and verified

#### 4.1.3 Communication Protocol
- All technical discussion happens in GitHub Issue comments
- Tag relevant partners using `@username` mentions
- For urgent issues, notify via project communication channels (email/Slack) with GitHub Issue link
- Update issue status within 2 business days of assignment
- All partners must monitor issues labeled with their component name

### 4.2 Escalation Procedures

#### 4.2.1 Escalation Levels

**Level 1: Component Level** (Days 1-3)
- Issue assigned to component owner partner
- Technical team investigates and resolves
- Expected resolution: 3 business days

**Level 2: Technical Coordination** (Days 4-7)
- If unresolved after 3 days, escalate to technical coordinator (ED)
- Multi-partner coordination meeting scheduled if needed
- Expected resolution: 7 business days total

**Level 3: Project Management** (Days 8+)
- If unresolved after 7 days or if it impacts project deliverables
- Escalate to Project Management Team
- Impact assessment on project timeline and deliverables
- Risk mitigation plan created

#### 4.2.2 Critical Issue Fast-Track
For **critical** issues (system down, data loss, security breach):
- Immediate notification to all partners via email and project channels
- Label with `critical` tag
- Technical coordinator involved from start
- Daily status updates required
- Expected resolution: 24-48 hours

#### 4.2.3 Cross-Component Issues
When issues involve multiple components:
1. Create a parent issue with all affected component labels
2. Create linked child issues for each component if needed
3. Technical coordinator facilitates resolution meeting
4. Document dependencies and integration points in issue description

#### 4.2.4 Issue Tracking Template
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