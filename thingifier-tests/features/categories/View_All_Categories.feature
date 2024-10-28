Feature: View All Categories
As a user,
I want to view all of my categories
So that I can evaluate the organization of my todos and projects.

  Background:
    Given the thingifier application is running
    And no objects exist other than the following categories:
      | title              | description             |
      | School             | School-related items    |
      | Work               | Work-related items      |

  Scenario Outline: User views all categories using JSON (Normal Flow)
    When the user attempts to view all categories in JSON format
    Then the thingifier app should return a response with status code 200
    And the response should contain a JSON array of all categories

  Scenario Outline: User views all categories using XML (Alternate Flow)
    When the user attempts to view all categories in XML format
    Then the thingifier app should return a response with status code 200
    And the response should contain an XML array of all categories

  Scenario Outline: User attempts to view all categories when no categories exist (Error Flow)
    Given all categories have been deleted from the system
    When the user attempts to view all categories
    Then the thingifier app should return a response with status code 200
    And the response should contain an empty array