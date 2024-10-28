Feature: As a student, I want to assign a todo to a category so that I can organize related or similar todos.

  Scenario Outline: Student assigns an existing category to an existing todo
    Given the todo "<todo>" exists
    Given the category "<category>" exists
    When the student assigns the category to the todo
    Then the response status code should be "201"
    Then the todo should be have the category "<category>"

    Examples:
      | todo                        | category |
      | Study algebra               | Math     |
      | Read Shakespeare            | English  |
      | Listen to Sabrina Carpenter | Music    |

  Scenario Outline: Student creates a todo with an existing category
    Given the category "<category>" exists
    When the student creates a todo with title "<todo>" with the category "<category>"
    Then the response status code should be "201"
    Then the todo should be created
    Then the todo should have the category "<category>"

    Examples:
      | todo                        | category |
      | Study algebra               | Math     |
      | Read Shakespeare            | English  |
      | Listen to Sabrina Carpenter | Music    |

  Scenario Outline: Student assigns a non-existent category to an existing todo
    Given the category "<category>" does not exist
    Given the todo "<todo>" exists
    When the student assigns the category to the todo
    Then the response status code should be "404"
    Then the error message should be "Could not find thing matching value for id"

    Examples:
      | todo          | category   |
      | Watch a movie | Fun        |
      | Do nothing    | Relaxation |
      | Sleep         | Rest       |
