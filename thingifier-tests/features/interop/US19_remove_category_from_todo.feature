Feature: Remove category from todo
As a student,
I want to remove a category from a todo
So that I can maintain accurate and relevant classifications for my tasks.

  Background:
    Given the thingifier application is running
    Given the thingifier application has no data

  Scenario Outline: Student removes an existing category from an existing todo (Normal Flow)
    Given the todo "<todo>" exists
    Given the category "<category>" exists
    Given the category is assigned to the todo
    When the category is removed from the todo
    Then the thingifier app should return a response with status code "200"
    Then the todo should not have the category "<category>"

    Examples:
      | todo                        | category |
      | Study algebra               | Math     |
      | Read Shakespeare            | English  |
      | Listen to Sabrina Carpenter | Music    |

  Scenario Outline: Student deletes the category assigned to a todo (Alternate Flow)
    Given the todo "<todo>" exists
    Given the category "<category>" exists
    Given the category is assigned to the todo
    When the student deletes the category
    Then the thingifier app should return a response with status code "200"
    Then the todo should not have the category "<todo>"

    Examples:
      | todo                        | category |
      | Study algebra               | Math     |
      | Read Shakespeare            | English  |
      | Listen to Sabrina Carpenter | Music    |

  Scenario Outline: Student deletes a non-existent category from the todo (Error Flow)
    Given the category "<category>" does not exist
    Given the todo "<todo>" exists
    When the student deletes the category from the todo
    Then the thingifier app should return a response with status code "404"
    Then the thingifier app should return an error message containing "Could not find any instances with"

    Examples:
      | todo                        | category |
      | Study algebra               | Math     |
      | Read Shakespeare            | English  |
      | Listen to Sabrina Carpenter | Music    |
