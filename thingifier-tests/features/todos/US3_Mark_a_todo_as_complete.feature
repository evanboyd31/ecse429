Feature: Mark a todo as complete

As a student,
I want to mark a todo as completed
So that I can keep track of assignments and project tasks I have already done.

  Background: 
    Given the thingifier application is running
    And no objects exist other than the following todos in the thingifier application:
      | title                 | doneStatus | description                |
      | A1-ECSE316            | true       | DNS client app development |
      | ClassExercise-ECSE429 | false      | Decision Tables designing  |

  Scenario Outline: Student attempts to mark a todo as complete with Json body (Normal Flow)
    When the student sends a POST API request for the "/todos/:id" endpoint with the id of the todo with title "<title>", and with json body containing doneStatus "<doneStatus>"
    Then the thingifier app should return a response with status code "200"
    And the thingifier app should return a response containing the todo with title "<title>" done status "<doneStatus>" and description "<description>"
    And the thingifier app should have the todo with title "<title>" marked as done
  Examples:
      | title                 | doneStatus | description                |
      | A1-ECSE316            | true       | DNS client app development |
      | ClassExercise-ECSE429 | true       | Decision Tables designing  |
  
  Scenario Outline: Student attempts to mark a todo as complete with xml body (Alternative Flow)
    When the student sends a POST API request for the "/todos/:id" endpoint with the id of the todo with title "<title>", and with xml body containing doneStatus "<doneStatus>"
    Then the thingifier app should return a response with status code "200"
    And the thingifier app should return a response containing the todo with title "<title>" done status "<doneStatus>" and description "<description>"
    And the thingifier app should have the todo with title "<title>" marked as done
  Examples:
      | title                 | doneStatus | description                |
      | A1-ECSE316            | true       | DNS client app development |
      | ClassExercise-ECSE429 | true       | Decision Tables designing  |

  Scenario Outline: Student attempts to mark a todo as complete with non-boolean doneStatus (Error Flow)
    When the student sends a POST API request for the "/todos/:id" endpoint with the id of the todo with title "<title>", and with json body containing doneStatus "<doneStatus>"
    Then the thingifier app should return the error status "400"
    And the thingifier app should return an error message containing "<errorMessage>"
  Examples:
      | title                 | doneStatus      | errorMessage                                      |
      | A1-ECSE316            | "true"          | Failed Validation: doneStatus should be BOOLEAN   |
      | ClassExercise-ECSE429 | 234             | Failed Validation: doneStatus should be BOOLEAN   |
      | ClassExercise-ECSE429 | "random string" | Failed Validation: doneStatus should be BOOLEAN   |
