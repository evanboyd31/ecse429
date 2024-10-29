Feature: Update Category
As a user,
I want to update the details of a category
So that I can correct a mistake or add more details.

  Background:
    Given the thingifier application is running
    And no objects exist other than the following categories:
      | id   | title               | description          |
      | 1    | School Assignments  | List of assignments  |

  Scenario Outline: User updates all fields of a category (Normal Flow)
    When the user attempts to update the category with id "<id>" to have title "<newTitle>" and description "<newDescription>"
    Then the thingifier app should return a response with status code "200"
    And the response should contain the updated category with title "<newTitle>" and description "<newDescription>"

    Examples:
      | id   | newTitle            | newDescription            |
      | 1    | College Work        | List of college projects  |

  Scenario Outline: User updates select fields of a category (Alternate Flow)
    When the user attempts to update the category with id "<id>" to have title "<newTitle>"
    Then the thingifier app should return a response with status code "200"
    And the response should contain the updated category with title "<newTitle>" and the original description "<description>"

    Examples:
      | id   | newTitle           | description           |
      | 1    | University Work    | List of assignments   |

  Scenario Outline: User attempts to update a category that does not exist (Error Flow)
    When the user attempts to update a non-existent category with id "<id>" to have title "<title>"
    Then the thingifier app should return a response with status code "404"
    And the thingifier app should return an error message containing "<errorMessage>"

    Examples:
      | id   | title             | errorMessage                         |
      | 99   | Non-Existent Cat  | "Category with id 99 not found"      |
