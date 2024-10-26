Feature: Modify Project
As a user,
I want to modify a project
So that the project reflects changing requirements over time.

    Background:
        Given the following projects exist in the system:
            | id | project                                                                                                           |
            | 1  | {"title": "Project Title #1", "completed": false, "active": true, "description": "The best project"}              |
            | 2  | {"title": "Project Title #2", "completed": true, "active": false, "description": "The second best project"}       |

    Scenario Outline: User updates a project with all fields using POST /projects/{id} (Normal Flow)
        When the user updates the project with id "<id>" by specifying title "<title>", completed "<completed>", active "<active>", and description "<description>" using POST /projects/{id}
        Then the project with id "<id>" should have the new fields "<project>"

        Examples:
            | id | title                | completed | active | description                   | project                                                                                             |
            | 1  | New Project Title #1 | true      | false  | No longer the best project :( | {"title": "New Project Title #1", "completed": true, "active": false, "description": "No longer the best project :("} |
            | 2  | New Project Title #2 | false     | true   | The new best project! :)      | {"title": "New Project Title #2", "completed": false, "active": true, "description": "The new best project! :)"}     |

    Scenario Outline: User updates a project with all fields using PUT /projects/{id} (Alternate Flow)
        When the user updates the project with id "<id>" by specifying title "<title>", completed "<completed>", active "<active>", and description "<description>" using PUT /projects/{id}
        Then the project with id "<id>" should have the new fields "<project>"

        Examples:
            | id | title                | completed | active | description                   | project                                                                                             |
            | 1  | New Project Title #1 | true      | false  | No longer the best project :( | {"title": "New Project Title #1", "completed": true, "active": false, "description": "No longer the best project :("} |
            | 2  | New Project Title #2 | false     | true   | The new best project! :)      | {"title": "New Project Title #2", "completed": false, "active": true, "description": "The new best project! :)"}     |

    Scenario Outline: User attempts to update a project with data that is the incorrect type (Error Flow)
        When the user attempts to update the project with id "<id>" by specifying title "<title>", completed "<completed>", active "<active>", and description "<description>" using POST /projects/{id}
        Then the response should have status code "<statusCode>"
        And the error message "<errorMessage>" should be raised

        Examples:
        | id | title                | completed | active  | description                   | statusCode | errorMessage                                   |
        | 1  | New Project Title #1 | "invalid" | false   | No longer the best project :( | 400        | Failed Validation: completed should be BOOLEAN |
        | 2  | New Project Title #2 | false     | "invalid" | The new best project! :)    | 400        | Failed Validation: active should be BOOLEAN    |
