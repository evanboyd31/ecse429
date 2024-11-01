Feature: Filter unfinished todos

As a student,
I want to see all unfinished todos
So that I can quickly determine the assignments and project tasks that I need to complete.

  Background:
    Given the thingifier application is running
    And no objects exist other than the following todos in the thingifier application:
      | title                 | doneStatus | description                |
      | A1-ECSE316            | true       | DNS client app development |
      | ClassExercise-ECSE429 | false      | Decision Tables designing  |
      | PartB-ECSE429         | false      | User story testing         |

  Scenario Outline: Student attempts to filter unfinished todos (Normal Flow)
    When the student sends a GET API request for the "/todos?doneStatus=false" endpoint
    Then the thingifier app should return a response with status code "200"
    And the thingifier app should return a response containing the list of todos "<todosList>"
  Examples:
      | todosList                           |
      | ClassExercise-ECSE429,PartB-ECSE429 |
  
  Scenario Outline: Student attempts to filter unfinished todos with additional query params (Alternative Flow)
    When the student sends a GET API request for the "/todos?doneStatus=false" endpoint with the additional query parameters "<queryParams>"
    Then the thingifier app should return a response with status code "200"
    And the thingifier app should return a response containing the unfinished todo with title "<title>" and description "<description>"
  Examples:
      | title                 | description               | queryParams                  |
      | ClassExercise-ECSE429 | Decision Tables designing | &title=ClassExercise-ECSE429 |
      | PartB-ECSE429         | User story testing        | &title=PartB-ECSE429         |

  Scenario Outline: Student attempts to filter unfinished todos with incorrect boolean value (Normal Flow)
    When the student sends a GET API request for the "/todos?doneStatus=faultyBoolean" endpoint with the faulty boolean value "<faultyBoolean>"
    Then the thingifier app should return a response containing the list of todos "<todosList>"
  Examples:
      | faultyBoolean  | todosList |
      | False          |           |
      | 0              |           |
