Feature: Delete Category
As a user,
I want to delete a category 
So that I can remove unnecessary categories.

  Background:
    Given the thingifier application is running
    And no objects exist in the thingifier app other than the following categories:
      | id   | title               | description          |
      | 1    | School Assignments  | List of assignments  |

  Scenario Outline: User deletes a category using DELETE /categories/{id} (Normal Flow)
    When the user attempts to delete using only the id of the category with title "<title>"
    Then the thingifier app should return a response with status code "200"
    And category with title "<title>" should no longer exist in the thingifier app

    Examples:
      | title               | 
      | School Assignments  | 

  Scenario Outline: User deletes a category with extra query parameters (Alternate Flow)
    When the user attempts to delete using the id of the category with title "<title>" and extra query parameters "<body>"
    Then the thingifier app should return a response with status code "200"
    And category with title "<title>" should no longer exist in the thingifier app

    Examples:
      | title               | body                     |
      | School Assignments  | { "extra": "parameter" } |

  Scenario Outline: User attempts to delete a category that does not exist (Error Flow)
    When the user attempts to delete using a non-existent category id "<id>"
    Then the thingifier app should return a response with status code "404"
    And the thingifier app should return an error message containing "Could not find any instances with"

    Examples:
      | title               |
      | Non-Existent Cat    |
