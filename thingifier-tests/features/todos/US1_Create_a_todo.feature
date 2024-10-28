Feature: Create a todo

As a student,
I want to create a todo
So that I can remember what assignments and project tasks I need to complete.

  Background: 
    Given the thingifier application is running
    And no objects exist other than the following todos in the thingifier application:
      | title                 | doneStatus | description                |
      | A1-ECSE316            | true       | DNS client app development |
      | ClassExercise-ECSE429 | false      | Decision Tables designing  |

  Scenario Outline: Student attempts to create a new todo using Json body (Normal Flow)
    When the student sends a POST API request for the "/todos" endpoint with json body containing title "<title>" done status "<doneStatus>" and description "<description>"
    Then the thingifier app should return a response with status code "201"
    Then the thingifier app should return a response containing the new todo with title "<title>" done status "<doneStatus>" and description "<description>"
    Then the thingifier app should contain the new todo with title "<title>" done status "<doneStatus>" and description "<description>"
  Examples: 
      | title          | doneStatus | description             |
      | A3-ECSE427     | false      | Shell memory management |
      | A3-ECSE446     | true       | Mesh light sampling     |
      | PartB-ECSE429  |            |                         |
  
  Scenario Outline: Student attempts to create a new todo using Xml body (Alternative Flow)
    When the student sends a POST API request for the "/todos" endpoint with xml body containing title "<title>" done status "<doneStatus>" and description "<description>"
    Then the thingifier app should return a response with status code "201"
    And the thingifier app should return a response containing the new todo with title "<title>" done status "<doneStatus>" and description "<description>"
    And the thingifier app should contain the new todo with title "<title>" done status "<doneStatus>" and description "<description>"
  Examples:
      | title          | doneStatus | description             |
      | A3-ECSE427     | false      | Shell memory management |
      | A3-ECSE446     | true       | Mesh light sampling     |
      | PartB-ECSE429  |            |                         |

  Scenario Outline: Student attempts to create a new todo without specifying the title (Error Flow)
    When the student sends a POST API request for the "/todos" endpoint with json body containing title "<title>" done status "<doneStatus>" and description "<description>"
    Then the thingifier app should return the error status "400"
    And the thingifier app should return an error message containing "<errorMessage>"
    And the thingifier app should not contain a todo with title "<title>" done status "<doneStatus>" and description "<description>"
  Examples:
      | title          | doneStatus | description             | errorMessage               |
      |                | false      | Shell memory management | title : field is mandatory |
      |                | true       | Mesh light sampling     | title : field is mandatory |
      |                |            |                         | title : field is mandatory |
