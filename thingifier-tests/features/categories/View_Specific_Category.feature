Feature: View Specific Category
As a user,
I want to view a specific category 
So that I can see its associated todos and projects.

  Background:
    Given the thingifier application is running
    And no objects exist other than the following categories:
      | title                | description              |
      | Home Chores          | List of home tasks      |
      | School Assignments   | List of assignments     |

  Scenario Outline: User views a specific category by id (Normal Flow)
    When the user attempts to view the category with id "<id>"
    Then the thingifier app should return a response with status code "200"
    And the response should contain the category with title "<title>" and description "<description>"

    Examples:
      | id   | title               | description            |
      | 1    | Home Chores         | List of home tasks     |
      | 2    | School Assignments  | List of assignments    |

  Scenario Outline: User views a specific category by title (Alternate Flow)
    When the user attempts to view the category with title "<title>"
    Then the thingifier app should return a response with status code "200"
    And the response should contain the category with title "<title>" and description "<description>"

    Examples:
      | title               | description            |
      | Home Chores         | List of home tasks     |
      | School Assignments  | List of assignments    |

  Scenario Outline: User attempts to view a category that does not exist (Error Flow)
    When the user attempts to view a category with non-existent id "<id>"
    Then the thingifier app should return a response with status code "404"
    And the thingifier app should return an error message containing "<errorMessage>"

    Examples:
      | id   | errorMessage                      |
      | 999  | "Category with id 999 not found"  |