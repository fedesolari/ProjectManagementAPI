Feature: Ticket Filtering

  Scenario: Filter by expiration
    Given two valid tickets with different priority and equal severity
    When trying to filter the tickets by expiracy
    Then we get an emptly tickets list
  #Habria que hacer otro escenario de expiration pero no se puede cambiar la cantidad de dias para aviso

  Scenario: Filter by priority
    Given two valid tickets with different priority and equal severity
    When trying to filter the tickets by priority 1
    Then we get only the first ticket

  Scenario: Filter by severity
    Given two valid tickets with different priority and equal severity
    When trying to filter the tickets by severity 1
    Then we get both tickets