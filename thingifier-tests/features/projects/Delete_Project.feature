Feature: Delete Project
As a user, I want to delete a project so that I can remove projects that are no longer relevant.

    Background:
        Given the following projects are the only objects that exist in the system:
            | title            | completed | active | description             |
            | Project Title #1 | false     | true   | The best project        |
            | Project Title #2 | true      | false  | The second best project |

    Scenario Outline: User deletes a project using DELETE /todos/{id} (Normal Flow)
        When the user deletes project with title <title>
        Then the project with title <title> should not exist in the system

        Examples:
            | title            |
            | Project Title #1 |
            | Project Title #2 |

    Scenario Outline: User deletes a project using DELETE /todos/{id} with extra query parameters (Alternate Flow)
        When the user sends extra query parameters <parameters> with values <values> when deleting project with title <title>
        Then the project with title <title> should not exist in the system

        Examples:
            | title            | parameters                         | values                                              |
            | Project Title #1 | title,completed,active,description | Project Title #1,false,true,The best project        |
            | Project Title #2 | title,completed,active,description | Project Title #2,true,false,The second best project |

    Scenario Outline: User attemps to delete a project that does not exist (Error flow)
        When the user deletes project with title <title>
        Then the response should have status code <statusCode>
        And an error message indicating the project could not be found is raised

        Examples:
            | title            | statusCode |
            | Project Title #3 |        404 |
            | Project Title #4 |        404 |