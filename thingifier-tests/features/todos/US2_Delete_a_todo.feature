Feature: Delete a todo

As a student,
I want to delete a todo
So that I can remove assignments and project tasks that are no longer relevant.

  Background: 
    Given the thingifier application is running
    And there exists the following todos in the thingifier application:
      | title                 | doneStatus | description                |
      | A1-ECSE316            | true       | DNS client app development |
      | ClassExercise-ECSE429 | false      | Decision Tables designing  |

  Scenario: Student attempts to delete a todo (Normal Flow)
    When the student sends a DELETE API request for the "/todos/:id" endpoint with the id of the todo with title "<title>" 
    Then the thingifier app should return a response with status code 200
    And the thingifier app should not contain a todo with title "<title>"
      | title                   |
      | A1-ECSE316              |
      | ClassExercise-ECSE429   |
  
  Scenario: Student attempts to delete a todo with extra query parameters (Alternate Flow) (Alternative Flow)
    When the student sends a DELETE API request for the "/todos/:id" endpoint with the id of the todo with title "<title>" and extra query parameters "<queryParams>"
    Then the thingifier app should return a response with status code 200
    And the thingifier app should not contain a todo with title "<title>"
      | title                   | queryParams       |
      | A1-ECSE316              | ?title=A1-ECSE316 |
      | ClassExercise-ECSE429   | ?donStatus=false  |

  Scenario: Student attempts to delete a todo that doesn't exist (Error Flow)
    When the student sends a DELETE API request for the todo with id "<id>" 
    Then the thingifier app should return the error status 404
    And the thingifier app should return the error message "<errorMessage>"
      | id      | errorMessage                                    |
      | 9999999 | Could not find any instances with todos/9999999 |
      | 9999998 | Could not find any instances with todos/9999998 |
