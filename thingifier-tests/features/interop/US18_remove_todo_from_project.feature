Feature: Remove todo from project

As a student,
I want to remove a todo from a project
So that I can keep my project task list current and focused on relevant activities.

  Background:
    Given the thingifier application is running
    Given the thingifier application has no data

  Scenario Outline: Student removes an existing todo from an existing project (Normal Flow)
    Given the todo "<todo>" exists
    Given the project "<project>" exists
    Given the todo is assigned to the project
    When the todo is removed from the project
    Then the thingifier app should return a response with status code "200"
    Then the todo should not have the project "<project>"
    Then the project should not have the todo "<todo>"

    Examples:
      | todo                    | project              |
      | Develop AI Model        | Skynet Development   |
      | Write final chapter     | My Novel             |
      | Write business proposal | Bakery business idea |

  Scenario Outline: Student deletes the todo linked to a project (Alternate Flow)
    Given the todo "<todo>" exists
    Given the project "<project>" exists
    Given the todo is assigned to the project
    When the student deletes the todo
    Then the thingifier app should return a response with status code "200"
    Then the project should not have the todo "<todo>"

    Examples:
      | todo                             | project                   |
      | Prove P = NP                     | Easy Math Problems        |
      | Solve the trolley problem        | Easy Philosophy Questions |
      | Show that the chicken came first | Easy Biology Questions    |

  Scenario Outline: Student deletes a non-existent todo from the project (Error Flow)
    Given the project "<project>" exists
    Given the todo "<todo>" does not exist
    When the student assigns the project to the todo
    Then the thingifier app should return a response with status code "404"
    Then the thingifier app should return an error message containing"Could not find any instances with"

    Examples:
      | todo          | project            |
      | Watch a movie | Cultural Learning  |
      | Do nothing    | Burnout Reduction  |
      | Sleep         | Health Improvement |
