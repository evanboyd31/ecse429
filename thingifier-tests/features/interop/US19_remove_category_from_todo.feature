Feature: As a student, I want to remove a category from a todo so that I can maintain accurate and relevant classifications for my tasks.

  Scenario Outline: Student removes an existing category from an existing todo
    Given the todo "<todo>" exists
    Given the category "<category>" exists
    Given the category is assigned to the todo
    When the category is removed from the todo
    Then the response status code should be "200"
    Then the todo should not have the category "<category>"

    Examples:
      | todo                        | category |
      | Study algebra               | Math     |
      | Read Shakespeare            | English  |
      | Listen to Sabrina Carpenter | Music    |

  Scenario Outline: Student deletes the category assigned to a todo
    Given the todo "<todo>" exists
    Given the category "<category>" exists
    Given the category is assigned to the todo
    When the student deletes the category
    Then the response status code should be "200"
    Then the todo should not have the category "<todo>"

    Examples:
      | todo                        | category |
      | Study algebra               | Math     |
      | Read Shakespeare            | English  |
      | Listen to Sabrina Carpenter | Music    |

  Scenario Outline: Student deletes a non-existent category from the todo
    Given the category "<category>" does not exist
    Given the todo "<todo>" exists
    When the student deletes the category from the todo
    Then it should fail with response "404"
    Then the error message should start with "Could not find any instances with"

    Examples:
      | todo                        | category |
      | Study algebra               | Math     |
      | Read Shakespeare            | English  |
      | Listen to Sabrina Carpenter | Music    |
