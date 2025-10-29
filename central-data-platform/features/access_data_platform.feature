

Feature: Access Protected Resources on CIRCULOOS Data platform

  Scenario: Authenticate and access resources of Orion-LD
    Given the service is running
    When I authenticate as a partner for Orion-LD
    Then I should have access to protected resources on Orion-LD
    And the resource response should contain expected version information of Orion-LD

  Scenario: Post a new entity to Orion-LD
    Given the service is running
    When I authenticate as a partner for Orion-LD
    And I post a new entity to Orion-LD with the following data:
      | id                               | type        | name        |
      | urn:ngsi-ld:Device:testDevice001 | Device      | Test Device |
    Then the entity should be created successfully in Orion-LD
    And I should be able to retrieve the entity from Orion-LD