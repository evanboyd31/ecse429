Feature: As a student, I want to remove a todo from a project so that I can keep my project task list current and focused on relevant activities.

  Scenario Outline: Student removes an existing todo from an existing project
    Given the todo "<todo>" exists
    Given the project "<project>" exists
    Given the todo is assigned to the project
    When the todo is removed from the project
    Then the response status code should be "200"
    Then the todo should not have the project "<project>"
    Then the project should not have the todo "<todo>"

    Examples:
      | todo                    | project              |
      | Develop AI Model        | Skynet Development   |
      | Write final chapter     | My Novel             |
      | Write business proposal | Bakery business idea |

  Scenario Outline: Student deletes the todo linked to a project
    Given the todo "<todo>" exists
    Given the project "<project>" exists
    Given the todo is assigned to the project
    When the student deletes the todo
    Then the response status code should be "200"
    Then the project should not have the todo "<todo>"

    Examples:
      | todo                             | project                   |
      | Prove P = NP                     | Easy Math Problems        |
      | Solve the trolley problem        | Easy Philosophy Questions |
      | Show that the chicken came first | Easy Biology Questions    |

  Scenario Outline: Student deletes a non-existent todo from the project 
    Given the project "<project>" exists
    Given the todo "<todo>" does not exist
    When the student assigns the project to the todo
    Then it should fail with response "404"
    Then the error message should start with "Could not find any instances with"

    Examples:
      | todo          | project            |
      | Watch a movie | Cultural Learning  |
      | Do nothing    | Burnout Reduction  |
      | Sleep         | Health Improvement |
