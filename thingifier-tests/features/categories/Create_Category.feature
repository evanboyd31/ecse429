Feature: Create Category
As a user,
I want to create a category 
So that I can tag my todos and/or projects.

  Background:
    Given the thingifier application is running

  Scenario: User creates a category with all fields (Normal Flow)
    When the user attempts to create a category with title "<title>" and description "<description>"
    Then the thingifier app should return a response with status code 201
    And a category with title "<title>" and description "<description>" should exist in the thingifier app

    Examples:
      | title                  | description              |
      | School Assignments     | All school assignments   |
      | Work Tasks             | All work-related tasks   |

  Scenario: User creates a category with missing fields (Alternate Flow)
    When the user attempts to create a category with only title "<title>"
    Then the thingifier app should return a response with status code 201
    And a category with title "<title>" should exist in the thingifier app

    Examples:
      | title                |
      | Personal Projects    |
      | Miscellaneous        |

  Scenario: User attempts to create a category with a pre-specified ID (Error Flow)
    When the user attempts to create a category with id "<id>", title "<title>" and description "<description>"
    Then the thingifier app should return a response with status code 400
    And the thingifier app should return the error message "<errorMessage>"

    Examples:
      | id   | title                  | description              | errorMessage                     |
      | 100  | School Assignments     | All school assignments   | "Invalid Creation: Failed Validation: Not allowed to create with id"   |
      | 200  | Work Tasks             | All work-related tasks   | "Invalid Creation: Failed Validation: Not allowed to create with id"   |
