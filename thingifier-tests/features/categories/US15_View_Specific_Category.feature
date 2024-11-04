Feature: View Specific Category
As a student,
I want to view a specific category 
So that I can see its associated todos and projects.

  Background:
    Given the thingifier application is running
    And no objects exist in the thingifier app other than the following categories:
      | title                | description              |
      | Home Chores          | List of home tasks      |
      | School Assignments   | List of assignments     |

  Scenario Outline: Student views a specific category by id (Normal Flow)
    When the student attempts to view a category with the id of the category with title "<title>"
    Then the thingifier app should return a response with status code "200"
    And the response should contain the category with title "<title>" and description "<description>"

    Examples:
      | title               | description            |
      | Home Chores         | List of home tasks     |
      | School Assignments  | List of assignments    |

  Scenario Outline: Student views a specific category by title (Alternate Flow)
    When the student attempts to view a category with title "<title>"
    Then the thingifier app should return a response with status code "200"
    And the response should contain the category with title "<title>" and description "<description>"

    Examples:
      | title               | description            |
      | Home Chores         | List of home tasks     |
      | School Assignments  | List of assignments    |

  Scenario Outline: Student attempts to view a category that does not exist (Error Flow)
    When the student attempts to view a category with non-existent id "<id>"
    Then the thingifier app should return a response with status code "404"
    And the thingifier app should return an error message containing "Could not find an instance"

    Examples:
      | id   |
      | 999  | 