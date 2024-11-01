Feature: Delete a todo

As a student,
I want to delete a todo
So that I can remove assignments and project tasks that are no longer relevant.

  Background: 
    Given the thingifier application is running
    And no objects exist other than the following todos in the thingifier application:
      | title                 | doneStatus | description                |
      | A1-ECSE316            | true       | DNS client app development |
      | ClassExercise-ECSE429 | false      | Decision Tables designing  |

  Scenario Outline: Student attempts to delete a todo (Normal Flow)
    When the student sends a DELETE API requests for the "/todos/:id" endpoint with the id of the todo with title "<title>" 
    Then the thingifier app should return the error status "200"
    And the thingifier app should not contain a todo with title "<title>"
  Examples:
      | title                   |
      | A1-ECSE316              |
      | ClassExercise-ECSE429   |
  
  Scenario Outline: Student attempts to delete a todo with extra query parameters (Alternate Flow) (Alternative Flow)
    When the student sends a DELETE API request for the "/todos/:id" endpoint with the id of the todo with title "<title>" and extra query parameters "<queryParams>"
    Then the thingifier app should return the error status "200"
    And the thingifier app should not contain a todo with title "<title>"
  Examples:
      | title                   | queryParams       |
      | A1-ECSE316              | ?title=A1-ECSE316 |
      | ClassExercise-ECSE429   | ?donStatus=false  |

  Scenario Outline: Student attempts to delete a todo that doesn't exist (Error Flow)
    When the student sends a DELETE API request for the todo with id "<id>" 
    Then the thingifier app should return the error status "404"
    And the thingifier app should return an error message containing "<errorMessage>"
  Examples:
      | id      | errorMessage                                    |
      | 9999999 | Could not find any instances with todos/9999999 |
      | 9999998 | Could not find any instances with todos/9999998 |
