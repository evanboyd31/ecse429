Feature: Addition of two numbers

  Scenario: Add two positive numbers
    Given I have the numbers 5 and 10
    When I add the numbers
    Then the result should be 15

  Scenario: Add a positive and a negative number
    Given I have the numbers 5 and -3
    When I add the numbers
    Then the result should be 2
