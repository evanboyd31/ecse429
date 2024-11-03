Feature: Delete Project
As a student, I want to delete a project so that I can remove projects that are no longer relevant.

    Background:
        Given the thingifier application is running
        And no objects exist other than the following projects:
            | title            | completed | active | description             |
            | Project Title #1 | false     | true   | The best project        |
            | Project Title #2 | true      | false  | The second best project |

    Scenario Outline: Student deletes a project using DELETE /todos/{id} (Normal Flow)
        When the student deletes project with title <title>
        Then the project with title <title> should not exist in the system

        Examples:
            | title            |
            | Project Title #1 |
            | Project Title #2 |

    Scenario Outline: Student deletes a project using DELETE /todos/{id} with extra query parameters (Alternate Flow)
        When the student sends extra query parameters <parameters> with values <values> when deleting project with title <title>
        Then the project with title <title> should not exist in the system

        Examples:
            | title            | parameters                         | values                                              |
            | Project Title #1 | title,completed,active,description | Project Title #1,false,true,The best project        |
            | Project Title #2 | title,completed,active,description | Project Title #2,true,false,The second best project |

    Scenario Outline: Student attemps to delete a project that does not exist (Error flow)
        When the student deletes project with title <title>
        Then the response should have status code <statusCode>
        And the thingifier app should return an error message containing "<errorMessage>"

        Examples:
            | title            | statusCode | errorMessage                      |
            | Project Title #3 |        404 | Could not find any instances with |
            | Project Title #4 |        404 | Could not find any instances with |