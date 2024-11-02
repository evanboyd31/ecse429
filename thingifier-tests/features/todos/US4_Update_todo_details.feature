Feature: Update todo details

As a student,
I want to update the details of a todo
So that the todo reflects the updated information about the assignment or project task.

  Background: 
    Given the thingifier application is running
    And no objects exist other than the following todos in the thingifier application:
      | title                 | doneStatus | description                |
      | A1-ECSE316            | true       | DNS client app development |
      | ClassExercise-ECSE429 | false      | Decision Tables designing  |

  Scenario Outline: Student attempts to update the details of a todo with Json body (Normal Flow)
    When the student sends a POST API request for the "/todos/:id" endpoint with the id of the todo with title "<originalTitle>", and with json body containing title "<title>", and description "<description>"
    Then the thingifier app should return the error status "200"
    And the thingifier app should return a response containing the todo with title "<title>" done status "<doneStatus>" and description "<description>"
    Then the thingifier app should contain the todo with title "<title>" done status "<doneStatus>" and description "<description>"
  Examples:
      | originalTitle         | title       | doneStatus | description               |
      | A1-ECSE316            | DNS-ECSE316 | true       | New description           |
      | ClassExercise-ECSE429 | DT-ECSE429  | false      | Decision Tables designing |
      | A1-ECSE316            | DNS-ECSE316 | true       |                           |
  
  Scenario Outline: Student attempts to update the details of a todo with xml body (Alternative Flow)
    When the student sends a POST API request for the "/todos/:id" endpoint with the id of the todo with title "<originalTitle>", and with xml body containing title "<title>", and description "<description>"
    Then the thingifier app should return the error status "200"
    And the thingifier app should return a response containing the todo with title "<title>" done status "<doneStatus>" and description "<description>"
    Then the thingifier app should contain the todo with title "<title>" done status "<doneStatus>" and description "<description>"
  Examples:
      | originalTitle         | title       | doneStatus | description               |
      | A1-ECSE316            | DNS-ECSE316 | true       | New description           |
      | ClassExercise-ECSE429 | DT-ECSE429  | false      | Decision Tables designing |

  Scenario Outline: Student attempts to update the details of a todo with an empty title (Error Flow)
    When the student sends a POST API request for the "/todos/:id" endpoint with the id of the todo with title "<originalTitle>", and with json body containing title "<title>", and description "<description>"
    Then the thingifier app should return the error status "400"
    And the thingifier app should return an error message containing "<errorMessage>"
  Examples:
      | originalTitle         | title       | doneStatus | description               | errorMessage                                |
      | A1-ECSE316            |             | true       | New description           | Failed Validation: title : can not be empty |
      | ClassExercise-ECSE429 |             | false      | Decision Tables designing | Failed Validation: title : can not be empty |
      | A1-ECSE316            |             | true       |                           | Failed Validation: title : can not be empty |
