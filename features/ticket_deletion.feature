Feature: Ticket Deletion

  Scenario: Successfull Ticket deletion
    Given Im a resource that wants to delete a ticket
    When I delete a ticket
    Then The ticket is deleted and I no longer have access to it
    # And I no longer have access to the ticket's associated tasks -> This is still not implemented in the API.
 
  Scenario: Invalid Ticket deletion
    Given Im a resource that wants to delete a ticket
    When I delete a ticket by an invalid id
    Then The deletion fails