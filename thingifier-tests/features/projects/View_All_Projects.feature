Feature: View All Projects
As a user,
I want to modify a project
So that the project reflects chaning requirements over time.

    Background:
        Given the following projects exist in the system:
            | project                                                                                                           |
            | {"title": "Project Title #1", "completed": false, "active": true, "description": "The best project"}              |
            | {"title": "Project Title #2", "completed": true, "active": false, "description": "The second best project"}       |

    Scenario Outline: User views all projects using JSON (Normal Flow)
        When the user attempts to view all projects in JSON format
        Then the user should see the projects "<project1>" and "<project2>" in the JSON response

        Examples:
            | project1                                                                                             | project2                                                                                                    |
            | {"title": "Project Title #1", "completed": false, "active": true, "description": "The best project"} | {"title": "Project Title #2", "completed": true, "active": false, "description": "The second best project"} |

    Scenario Outline: User views all projects using XML (Alternate Flow)
        When the user attempts to view all projects in XML format
        Then the user should see the projects "<project1>" and "<project2>" in the XML response

        Examples:
            | project1                                                                                                                                       | project2                                                                                                                                              | 
            | <project><active>true</active><description>The best project</description><completed>false</completed><title>Project Title #1</title></project> | <project><active>false</active><description>The second best project</description><completed>true</completed><title>Project Title #2</title></project> |


    Scenario Outline: User attempts to view all projects when no projects exist in the system (Error Flow)
        Given all projects in the system have been deleted
        When the user attempts to view all projects in JSON format
        Then the user should receive an empty JSON array
        And the user should not see the projects "<project1>" and "<project2>" in the JSON response

        Examples:
            | project1                                                                                             | project2                                                                                                    |
            | {"title": "Project Title #1", "completed": false, "active": true, "description": "The best project"} | {"title": "Project Title #2", "completed": true, "active": false, "description": "The second best project"} |


