Feature: View All Categories
As a student,
I want to view all of my categories
So that I can evaluate the organization of my todos and projects.

  Background:
    Given the thingifier application is running
    And no objects exist in the thingifier app other than the following categories:
      | title  | description          |
      | School | School-related items |
      | Work   | Work-related items   |

  Scenario Outline: Student views all categories using JSON (Normal Flow)
    When the student attempts to view all categories in JSON format
    Then the thingifier app should return a response with status code "200"
    And the response should contain a JSON array of all categories

  Scenario Outline: Student views all categories using XML (Alternate Flow)
    When the student attempts to view all categories in XML format
    Then the thingifier app should return a response with status code "200"
    And the response should contain an XML array of all categories

  Scenario Outline: Student attempts to view all categories when no categories exist (Error Flow)
    Given all categories have been deleted from the system
    When the student attempts to view all categories
    Then the thingifier app should return a response with status code "200"
    And the response should contain an empty array
