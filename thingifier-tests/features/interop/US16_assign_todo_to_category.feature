Feature: Assign todo to category
As a student,
I want to assign a todo to a category
So that I can organize related or similar todos.

  Background:
    Given the thingifier application is running
    Given no objects exist in the thingifier app

  Scenario Outline: Student assigns an existing category to an existing todo (Normal Flow)
    Given the todo "<todo>" exists
    Given the category "<category>" exists
    When the student assigns the category to the todo
    Then the thingifier app should return a response with status code "201"
    Then the todo should have the category "<category>"

    Examples:
      | todo                        | category |
      | Study algebra               | Math     |
      | Read Shakespeare            | English  |
      | Listen to Sabrina Carpenter | Music    |

  Scenario Outline: Student creates a todo with an existing category (Alternate Flow)
    Given the category "<category>" exists
    When the student creates a todo with title "<todo>" with that category
    Then the thingifier app should return a response with status code "201"
    Then the todo should be created
    Then the todo should have the category "<category>"

    Examples:
      | todo                        | category |
      | Study algebra               | Math     |
      | Read Shakespeare            | English  |
      | Listen to Sabrina Carpenter | Music    |

  Scenario Outline: Student assigns a non-existent category to an existing todo (Error Flow)
    Given the todo "<todo>" exists
    When the student assigns a non-existent category to the todo
    Then the thingifier app should return a response with status code "404"
    Then the thingifier app should return an error message containing "Could not find thing matching value for id"

    Examples:
      | todo          | 
      | Watch a movie |
      | Do nothing    |
      | Sleep         |
