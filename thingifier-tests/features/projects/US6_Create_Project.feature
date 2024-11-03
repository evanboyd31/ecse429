Feature: Create Project
As a student, I want to create a project so that I can keep track of related tasks.

    Background:
        Given the thingifier application is running

    Scenario Outline: User creates a project with all fields (Normal Flow)
        When the user creates a project by specifying title <title>, completed <completed>, active <active>, and description <description>
        Then the project <project> should be created

        Examples:
            | title           | completed | active | description | project                             |                                                                      
            | Project Title   | false     | true   | project1    | Project Title,false,true,project1   |
            | Different Title | true      | false  | project2    | Different Title,true,false,project2 |

    Scenario Outline: User creates a project with missing fields (Alternate Flow)
        When the user creates a project with missing fields by specifying title <title>, completed <completed>, active <active>, and description <description>
        Then the project <project> should be created

        Examples:
            | title | completed | active | description | project                  |
            |       |           |        |             | ,false,false,            |
            | title |           |        |             | title,false,false,       |
            |       | true      |        |             | ,true,false,             |
            |       |           | true   |             | ,false,true,             |
            |       |           |        | description | ,false,false,description |

    Scenario Outline: User attempts to create a project with a pre-specified ID (Error Flow)
        When the user attempts to create a project by specifying id <projectId>, title <title>, completed <completed>, active <active>, and description <description>
        Then the response should have status code <statusCode>
        And the thingifier app should return an error message containing "<errorMessage>"

        Examples:
            | projectId | title           | completed | active | description           | statusCode | errorMessage                                                       |
            | 31        | Project Title   | false     | true   | The best project      | 400        | Invalid Creation: Failed Validation: Not allowed to create with id |
            |  1        | Different Title | true      | false  | The different project | 400        | Invalid Creation: Failed Validation: Not allowed to create with id |
