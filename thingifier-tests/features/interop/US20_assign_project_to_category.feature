Feature: As a student, I want to assign a project to a category so that I can organize related or similar projects.

  Scenario Outline: Student assigns an existing category to an existing project
    Given the project "<project>" exists
    Given the category "<category>" exists
    When the student assigns the category to the project
    Then the response status code should be "201"
    Then the project should be have the category "<category>"

    Examples:
      | project           | category |
      | Algebra           | Math     |
      | Shakespeare       | English  |
      | Sabrina Carpenter | Music    |

  Scenario Outline: Student creates a project with an existing category
    Given the category "<category>" exists
    When the student creates a project with title "<project>" with the category "<category>"
    Then the response status code should be "201"
    Then the project should be created
    Then the project should have the category "<category>"

    Examples:
      | project           | category |
      | Algebra           | Math     |
      | Shakespeare       | English  |
      | Sabrina Carpenter | Music    |

  Scenario Outline: Student assigns a non-existent category to an existing project
    Given the category "<category>" does not exist
    Given the project "<project>" exists
    When the student assigns the category to the project
    Then the response status code should be "404"
    Then the error message should be "Could not find thing matching value for id"

    Examples:
      | project           | category |
      | Algebra           | Math     |
      | Shakespeare       | English  |
      | Sabrina Carpenter | Music    |
