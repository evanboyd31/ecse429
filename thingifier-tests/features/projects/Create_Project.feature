Feature: Create Project
As a user,
I want to create a project
So that I can keep track of related tasks.

    Scenario Outline: User creates a project with all fields (Normal Flow)
        When the user creates a project by specifying title "<title>", completed "<completed>", active "<active>", and description "<description>"
        Then the project "<project>" should be created

        Examples:
            | title           | completed | active | description           | project                                                                                          |
            | Project Title   | false     | true   | The best project      | {"title": "Project Title", "completed": false, "active": true, "description": "The best project"}|
            | Different Title | true      | false  | The different project | {"title": "Different Title", "completed": true, "active": false, "description": "The different project"} |

    Scenario Outline: User creates a project with missing fields (Alternate Flow)
        When the user creates a project by specifying title "<title>", completed "<completed>", active "<active>", and description "<description>"
        Then the project "<project>" should be created

        Examples:
            | title | completed | active | description | project                                                                |
            |       |           |        |             | {"title": "", "completed": false, "active": false, "description": ""} |
            | title |           |        |             | {"title": "title", "completed": false, "active": false, "description": ""} |
            |       | true      |        |             | {"title": "", "completed": true, "active": false, "description": ""}  |
            |       |           | true   |             | {"title": "", "completed": false, "active": true, "description": ""}  |
            |       |           |        | description | {"title": "", "completed": false, "active": false, "description": "description"} |

    Scenario Outline: User attempts to create a project with a pre-specified ID (Error Flow)
        When the user attempts to create a project by specifying id "<id>" title "<title>", completed "<completed>", active "<active>", and description "<description>"
        Then the response should have status code "<statusCode>"
        And the error message "<errorMessage>" should be raised

        Examples:
            | id | title           | completed | active | description           | statusCode | errorMessage                                                       |
            | 31 | Project Title   | false     | true   | The best project      | 400        | Invalid Creation: Failed Validation: Not allowed to create with id |
            |  1 | Different Title | true      | false  | The different project | 400        | Invalid Creation: Failed Validation: Not allowed to create with id |
