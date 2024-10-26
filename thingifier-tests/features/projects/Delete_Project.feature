Feature: Delete Project
As a user, 
I want to delete a project
So that I can remove projects that are no longer relevant.

    Background:
        Given the following projects exist in the system:
            | id | title            | completed | active | description             |
            |  1 | Project Title #1 | false     | true   | The best project        |
            |  2 | Project Title #2 | true      | false  | The second best project |

    Scenario Outline: User deletes a project using DELETE /todos/{id} (Normal Flow)
        When the user deletes project with id "<id>"
        Then the project with id "<id>" should not exist in the system

        Examples:
            | id |
            |  1 |
            |  2 |

    Scenario Outline: User deletes a project using DELETE /todos/{id} with extra query parameters (Alternate Flow)
        When the user deletes project with id "<id>" with extra query parameters "<parameters>" with values "<values>"
        Then the project with id "<id>" should not exist in the system

        Examples:
            | id | parameters                         | values                                              |
            |  1 | title,completed,active,description | Project Title #1,false,true,The best project        |
            |  2 | title,completed,active,description | Project Title #2,true,false,The second best project |

    Scenario Outline: User attemps to delete a project that does not exist (Error flow)
        Given no projects with id "<id>" exist in the system
        When the user attemps to delete project with id "<id>"
        Then the response should have status code "<statusCode>"
        And the error message "<errorMessage>" should be raised

        Examples:
            | id | statusCode | errorMessage                                  |
            |  3 |        404 | Could not find any instances with projects/3  |
            | -1 |        404 | Could not find any instances with projects/-1 |