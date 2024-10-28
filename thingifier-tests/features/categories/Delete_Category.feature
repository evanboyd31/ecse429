Feature: Delete Category
As a user,
I want to delete a category 
So that I can remove unnecessary categories.

  Background:
    Given the thingifier application is running
    And no objects exist other than the following categories:
      | id   | title               | description          |
      | 1    | School Assignments  | List of assignments  |

  Scenario Outline: User deletes a category using DELETE /categories/{id} (Normal Flow)
    When the user attempts to delete the category with id "<id>"
    Then the thingifier app should return a response with status code "200"
    And category with id "<id>" should no longer exist in the thingifier app

    Examples:
      | id   |
      | 1    |

  Scenario Outline: User deletes a category with extra query parameters (Alternate Flow)
    When the user attempts to delete the category with id "<id>" using extra query parameter "force=true"
    Then the thingifier app should return a response with status code "200"
    And category with id "<id>" should no longer exist in the thingifier app

    Examples:
      | id   |
      | 1    |

  Scenario Outline: User attempts to delete a category that does not exist (Error Flow)
    When the user attempts to delete a non-existent category with id "<id>"
    Then the thingifier app should return a response with status code "404"
    And the thingifier app should return an error message containing "<errorMessage>"

    Examples:
      | id   | errorMessage                      |
      | 99   | "Category with id 99 not found"   |
