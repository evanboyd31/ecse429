Feature: Modify Project
As a student, I want to modify a project so that the project reflects changing requirements over time.

    Background:
        Given the thingifier application is running
        And no objects exist other than the following projects:
            | title            | completed | active | description             |
            | Project Title #1 | false     | true   | The best project        |
            | Project Title #2 | true      | false  | The second best project |

    Scenario Outline: Student updates a project with all fields using POST /projects/:id (Normal Flow)
        When the student updates the project with title <title> by specifying new title <newTitle>, completed <newCompleted>, active <newActive>, and description <newDescription> using POST /projects/:id
        Then the project that had title <title> should have the new fields <project>

        Examples:
            | title            | newTitle             | newCompleted | newActive | newDescription                | project                                                       |
            | Project Title #1 | New Project Title #1 | true         | false     | No longer the best project :( | New Project Title #1,true,false,No longer the best project :( |
            | Project Title #2 | New Project Title #2 | false        | true      | The new best project! :)      | New Project Title #2,false,true,The new best project! :)      |

    Scenario Outline: Student updates a project with all fields using PUT /projects/:id (Alternate Flow)
        When the student updates the project with title <title> by specifying new title <newTitle>, completed <newCompleted>, active <newActive>, and description <newDescription> using PUT /projects/:id
        Then the project that had title <title> should have the new fields <project>

        Examples:
            | title            | newTitle             | newCompleted | newActive | newDescription                | project                                                       |
            | Project Title #1 | New Project Title #1 | true         | false     | No longer the best project :( | New Project Title #1,true,false,No longer the best project :( |
            | Project Title #2 | New Project Title #2 | false        | true      | The new best project! :)      | New Project Title #2,false,true,The new best project! :)      |

    Scenario Outline: Student attempts to update a project with data that is the incorrect type (Error Flow)
        When the student updates the project with title <title> by specifying new title <newTitle>, completed <newCompleted>, active <newActive>, and description <newDescription> using POST /projects/:id
        Then the response should have status code <statusCode>
        And the thingifier app should return an error message containing "<errorMessage>"

        Examples:
            | title            | newTitle             | newCompleted                           | newActive                              | newDescription                | statusCode | errorMessage                                   |
            | Project Title #1 | New Project Title #1 | This is a string but should be Boolean | false                                  | No longer the best project :( | 400        | Failed Validation: completed should be BOOLEAN |
            | Project Title #2 | New Project Title #2 | false                                  | This is a string but should be Boolean | The new best project! :)      | 400        | Failed Validation: active should be BOOLEAN    |
