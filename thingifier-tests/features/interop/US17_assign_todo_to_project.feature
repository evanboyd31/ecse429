Feature: Assign todo to project
As a student,
I want to assign a todo to a project
So that I can see group all the tasks needed to complete that project.

  Background:
    Given the thingifier application is running
    Given no objects exist in the thingifier app

  Scenario Outline: Student assigns an existing todo to an existing project (Normal Flow)
    Given the todo "<todo>" exists
    Given the project "<project>" exists
    When the student assigns the todo to the project
    Then the thingifier app should return a response with status code "201"
    Then the todo should have the project "<project>"
    Then the project should have the todo "<todo>"

    Examples:
      | todo                    | project              |
      | Develop AI Model        | Skynet Development   |
      | Write final chapter     | My Novel             |
      | Write business proposal | Bakery business idea |

  Scenario Outline: Student creates a todo with an existing project (Alternate Flow)
    Given the project "<project>" exists
    When the student creates a todo with title "<todo>" with that project
    Then the thingifier app should return a response with status code "201"
    Then the todo should be created
    Then the todo should have the project "<project>"
    Then the project should have the todo "<todo>"

    Examples:
      | todo                             | project                   |
      | Prove P = NP                     | Easy Math Problems        |
      | Solve the trolley problem        | Easy Philosophy Questions |
      | Show that the chicken came first | Easy Biology Questions    |

  Scenario Outline: Student assigns a non-existent project to an existing todo (Error Flow)
    Given the todo "<todo>" exists
    When the student assigns a non-existent project to the todo
    Then the thingifier app should return a response with status code "404"
    Then the thingifier app should return an error message containing "Could not find thing matching value for id"

    Examples:
      | todo          |
      | Watch a movie | 
      | Do nothing    |
      | Sleep         |
