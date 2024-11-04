Feature: Update Category
As a student,
I want to update the details of a category
So that I can correct a mistake or add more details.

  Background:
    Given the thingifier application is running
    And no objects exist in the thingifier app other than the following categories:
      | id   | title               | description          |
      | 1    | School Assignments  | List of assignments  |

  Scenario Outline: Student updates all fields of a category (Normal Flow)
    When the student attempts to update the category with title "<title>" to have title "<newTitle>" and description "<newDescription>"
    Then the thingifier app should return a response with status code "200"
    And the response should contain the updated category with title "<newTitle>" and description "<newDescription>"

    Examples:
      | title                 | newTitle            | newDescription            |
      | School Assignments    | College Work        | List of college projects  |

  Scenario Outline: Student updates select fields of a category (Alternate Flow)
    When the student attempts to update the category with title "<title>" to have title "<newTitle>"
    Then the thingifier app should return a response with status code "200"
    And the response should contain the updated category with title "<newTitle>" and the original description "<description>"

    Examples:
      | title                 | newTitle           | description           |
      | School Assignments    | University Work    | List of assignments   |

  Scenario Outline: Student attempts to update a category that does not exist (Error Flow)
    When the student attempts to update a non-existent category with id "<id>" to have title "<title>"
    Then the thingifier app should return a response with status code "404"
    And the thingifier app should return an error message containing "No such"

    Examples:
      | title              | newTitle           |
      | Non-Existent Cat   | Existent Cat       | 
