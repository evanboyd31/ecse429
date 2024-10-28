Feature: View All Active Projects
As a user,
I want to modify a project
So that I can keep track of the progress of on-going projects.

    Background:
        Given the thingifier application is running
        And no objects exist other than the following projects:
            | title            | completed | active | description             |
            | Project Title #1 | true      | false  | The best project        |
            | Project Title #2 | false     | true  | The second best project  |

    Scenario Outline: User views all active projects using JSON (Normal Flow)
        When the user attempts to view all active projects in JSON format
        Then the user should see the project <project2> in the JSON response
        And the user should not see the project <project1> in the JSON response

        Examples:
            | project1                                                                                             | project2                                                                                                    |
            | {"title": "Project Title #1", "completed": true, "active": false, "description": "The best project"} | {"title": "Project Title #2", "completed": false, "active": true, "description": "The second best project"} |

    Scenario Outline: User views all active projects using XML (Alternate Flow)
        When the user attempts to view all active projects in XML format
        Then the user should see the project <project2> in the XML response
        And the user should not see the project <project1> in the XML response

        Examples:
            | project1                                                                                                                                       | project2                                                                                                                                              | 
            | <project><active>false</active><description>The best project</description><completed>true</completed><title>Project Title #1</title></project> | <project><active>true</active><description>The second best project</description><completed>false</completed><title>Project Title #2</title></project> |


    Scenario Outline: User attempts to view all projects when no active projects exist in the system (Error Flow)
        Given <project2> has been deleted from the system
        When the user attempts to view all active projects in JSON format
        Then the user should receive an empty JSON array
        And the user should not see the project <project1> in the JSON response

        Examples:
            | project1                                                                                             | project2                                                                                                    |
            | {"title": "Project Title #1", "completed": true, "active": false, "description": "The best project"} | {"title": "Project Title #2", "completed": false, "active": true, "description": "The second best project"} |



