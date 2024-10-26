Feature: As a student, I want to see all the todos for a project so that I can see all the related tasks for that project

  Scenario Outline: Student gets the todos related to the project
    Given the following todos exist:
      | todo1                   | todo2        |
      | Develop AI Model        | Buy GPU      |
      | Write final chapter     | Draw cover   |
      | Write business proposal | Find a baker |
    Given the project "<project>" exists
    Given the todos are assigned to the project
    When the student gets the todos assigned to the project
    Then the response status code should be "200"
    Then the response should have the following todos:
      | todo1                   | todo2        |
      | Develop AI Model        | Buy GPU      |
      | Write final chapter     | Draw cover   |
      | Write business proposal | Find a baker |

    Examples:
      | project              |
      | Skynet Development   |
      | My Novel             |
      | Bakery business idea |

  Scenario Outline: Student gets the project information
    Given the following todos exist:
      | todo1                   | todo2        |
      | Develop AI Model        | Buy GPU      |
      | Write final chapter     | Draw cover   |
      | Write business proposal | Find a baker |
    Given the project "<project>" exists
    Given the todos are assigned to the project
    When the student gets the project information
    Then the response status code should be "200"
    Then the response should have the following todos:
      | todo1                   | todo2        |
      | Develop AI Model        | Buy GPU      |
      | Write final chapter     | Draw cover   |
      | Write business proposal | Find a baker |

    Examples:
      | project              |
      | Skynet Development   |
      | My Novel             |
      | Bakery business idea |
# IDK WHAT ERROR FLOW TO USE BECAUSE GETTING TODOS FOR A PROJECT THAT DOES NOT EXIST DOES NOT ERROR
#   Scenario Outline: Student assigns a non-existent project to an existing todo
#     Given the project "<project>" does not exist
#     Given the todo "<todo>" exists
#     When the student assigns the project to the todo
#     Then the response status code should be "200"
#     Then it should return the error message "Could not find thing matching value for id"
#     Examples:
#       | todo          | project            |
#       | Watch a movie | Cultural Learning  |
#       | Do nothing    | Burnout Reduction  |
#       | Sleep         | Health Improvement |
