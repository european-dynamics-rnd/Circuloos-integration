

Feature: Access Protected Resources on CIRCULOOS Data platform

  Scenario: Authenticate and access resources of Orion-LD
    Given the service is running
    When I authenticate as a partner for Orion-LD
    Then I should have access to protected resources on Orion-LD 
    And the resource response should contain expected version information of Orion-LD