Feature: Ticket Get

  Scenario: Invalid Ticket get
    Given I dont have any tickets with an id of 1000
    When Trying to get a Ticket with that id
    Then I dont get any ticket
 
  Scenario: Successfully Ticket get
    Given a ticket with title Title, a description Description, a priority 1, a severity 1, a product_version_id 1, a client_id 1
    When Trying to get a Ticket with that id
    Then I get a valid ticket
    And We get that the title is Title, the description is Description, the priority 1, the severity 1, the product_version_id 1, and the client_id 1
