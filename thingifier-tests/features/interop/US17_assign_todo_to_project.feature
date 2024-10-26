Feature: As a student, I want to assign a todo to a project so that I can see group all the tasks needed to complete that project.

  Scenario Outline: Student assigns an existing todo to an existing project
    Given the todo "<todo>" exists
    Given the project "<project>" exists
    When the student assigns the todo to the project
    Then the response status code should be "201"
    Then the todo should have the project "<project>"
    Then the project should have the todo "<todo>"

    Examples:
      | todo                    | project              |
      | Develop AI Model        | Skynet Development   |
      | Write final chapter     | My Novel             |
      | Write business proposal | Bakery business idea |

  Scenario Outline: Student creates a todo with an existing project
    Given the project "<project>" exists
    When the student creates a todo with title "<todo>" with the project "<project>"
    Then the response status code should be "201"
    Then the todo should be created
    Then the todo should have the project "<project>"
    Then the project should have the todo "<todo>"

    Examples:
      | todo                             | project                   |
      | Prove P = NP                     | Easy Math Problems        |
      | Solve the trolley problem        | Easy Philosophy Questions |
      | Show that the chicken came first | Easy Biology Questions    |

  Scenario Outline: Student assigns a non-existent project to an existing todo
    Given the project "<project>" does not exist
    Given the todo "<todo>" exists
    When the student assigns the project to the todo
    Then the response status code should be "404"
    Then the error message should be "Could not find thing matching value for id"

    Examples:
      | todo          | project            |
      | Watch a movie | Cultural Learning  |
      | Do nothing    | Burnout Reduction  |
      | Sleep         | Health Improvement |
