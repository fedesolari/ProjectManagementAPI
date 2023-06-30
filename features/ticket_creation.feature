Feature: Ticket Creation

  Scenario: Invalid Ticket creation
    Given Im a resource
    		When I create a ticket with the following data
			| property          | value 									                          |
			| title     		    | Reports contain missing data                      |
			| description   	  |                                                   |
			| severity     	    | 1                                                 |
			| priority         	| 1                                                 |
			| product_version_id| 1                                                 |
			| resource_name 		| John Doe                                          |
			| client_id         | 5                                                 |
    Then The ticket does not get created

	Scenario: Successfull Ticket creation
		Given Im a resource
		When I create a ticket with the following data
			| property          | value 									                          |
			| title     		    | Reports contain missing data                      |
			| description   	  | Price column is missing from the downloaded report|
			| severity     	    | 1                                                 |
			| priority         	| 1                                                 |
			| product_version_id| 1                                                 |
			| resource_name 		| John Doe                                          |
			| client_id         | 5                                                 |
		Then The ticket gets successfully created
    And Contains valid ID
    And Ticket State is NEW
    And The title is Reports contain missing data, the description is Price column is missing from the downloaded report, the priority 1, the severity 1, the product_version_id 1, the resource_name is John Doe and the client_id 5

  
    Scenario: Correct SLA is applied
      Given Im a resource
      When When I create a ticket with a severity of 1
      Then The SLA is 7 days from creation date
