Feature: Ticket update

  Scenario: Valid Ticket title update
    Given A ticket
    When I change its title to title2
    Then The Ticket title changes to title2

  Scenario: Valid Ticket description update
    Given A ticket
    When I change its description to description2
    Then The Ticket description changes to description2

  Scenario: Valid Ticket priority update
    Given A ticket
    When I change its priority to 2
    Then The Ticket priority changes to 2

  Scenario: Valid Ticket severity update
    Given A ticket
    When I change its severity to 2
    Then The Ticket severity changes to 2

  Scenario: Valid Ticket client_id update
    Given A ticket
    When I change its client_id to 2
    Then The Ticket client_id changes to 2

  Scenario: Valid Ticket product_version_id update
    Given A ticket
    When I change its product_version_id to 2 being that this product_version_id is valid
    Then The Ticket product_version_id changes to 2

  Scenario: Valid Ticket state update
    Given A ticket
    When I change its state to IN_PROGRESS with a resource_name of resource_1
    Then The Ticket state changes to IN_PROGRESS
    And The resource_name changes to resource_1

  Scenario: Valid Ticket state update
    Given A ticket with a state of OPEN
    When I change its state to NEW
    Then The state update fails because cant change state to NEW
    And Its state is still OPEN

  Scenario: Invalid Ticket state update
    Given A ticket
    When I change its state to IN_PROGRESS without a resource_name
    Then Its state doesnt change
    And The state update fails because no resource

    Scenario: Invalid product_version_id update
    Given A ticket
    When I change its product_version_id to 1000 being that this product_version_id is invalid
    Then The product_version_id update fails
    And Its product_version_id doesnt change

  Scenario: Invalid priority change
    Given A ticket
    When I change its priority to 100
    Then The priority update fails
    And Its priority doesnt change

  Scenario: Invalid severity change
    Given A ticket
    When I change its severity to 100
    Then The severity update fails
    And Its severity doesnt change
