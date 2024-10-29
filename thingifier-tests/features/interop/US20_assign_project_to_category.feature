Feature: Assign project to category
As a student,
I want to assign a project to a category
So that I can organize related or similar projects.

  Background:
    Given the thingifier application is running
    Given no objects exist in the thingifier app

  Scenario Outline: Student assigns an existing category to an existing project (Normal Flow)
    Given the project "<project>" exists
    Given the category "<category>" exists
    When the student assigns the category to the project
    Then the thingifier app should return a response with status code "201"
    Then the project should have the category "<category>"

    Examples:
      | project           | category |
      | Algebra           | Math     |
      | Shakespeare       | English  |
      | Sabrina Carpenter | Music    |

  Scenario Outline: Student creates a project with an existing category (Alternate Flow)
    Given the category "<category>" exists
    When the student creates a project with title "<project>" with that category
    Then the thingifier app should return a response with status code "201"
    Then the project should be created
    Then the project should have the category "<category>"

    Examples:
      | project           | category |
      | Algebra           | Math     |
      | Shakespeare       | English  |
      | Sabrina Carpenter | Music    |

  Scenario Outline: Student assigns a non-existent category to an existing project (Error Flow)
    Given the project "<project>" exists
    When the student assigns a non-existent category to the project
    Then the thingifier app should return a response with status code "404"
    Then the thingifier app should return an error message containing "Could not find thing matching value for id"

    Examples:
      | project           |
      | Algebra           |
      | Shakespeare       |
      | Sabrina Carpenter |
