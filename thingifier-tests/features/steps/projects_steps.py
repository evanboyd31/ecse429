import httpx
import json
import re

from behave import given, when, then

projects_url = "http://localhost:4567/projects"


def assert_project(expected, actual, compare_id=False):

    print(expected)
    print(actual)

    if compare_id:
        assert expected.get("id") == actual.get("id")

    print(repr(actual.get("description")[1:-1]))
    print(len(actual.get("description")[1:-1]))
    print(repr(expected.get("description")))
    print(len(expected.get("description")))
    
    assert repr(expected.get("title")) == repr(actual.get("title"))
    assert repr(expected.get("completed")) == repr(actual.get("completed"))
    assert repr(expected.get("active")) == repr(actual.get("active"))
    assert repr(actual.get("description")) == repr((expected.get("description"))), f"{expected.get("description")}, {actual.get("description")[1:-1]}"

def create_project(context, title, completed, active, description, project_id=None):
    project = {}

    # all fields are optional, so only specify if necessary

    if project_id and project_id != "N/A":
        project.update({
            "id": project_id
        })

    if title and title != "N/A":
        project.update({
            "title" : title
        })

    if description and description != "N/A":
        project.update({
            "description": description
        })
    
    if completed and completed != "N/A":
        project.update({
            "completed": True if completed == "true" else False
        })
    
    if active and active != "N/A":
        project.update({
            "active": True if active == "true" else False,
        })

    # ensure correct error messages and codes and check that no extra project has been created
    response = httpx.post(projects_url, json=project)

    context.response = response

    context.actual_project = response.json()

@when('the user creates a project by specifying title {title}, completed {completed}, active {active}, and description {description}')
def step_when_create_project(context, title, completed, active, description):
    create_project(context=context,
                   title=title,
                   completed=completed,
                   active=active,
                   description=description)
    
@when('the user creates a project with missing fields by specifying title {title}, completed {completed}, active {active}, and description {description}')
def step_when_create_project(context, title, completed, active, description):
    create_project(context=context,
                   title=title,
                   completed=completed,
                   active=active,
                   description=description)


@when('the user attempts to create a project by specifying id {projectId}, title {title}, completed {completed}, active {active}, and description {description}')
def step_when_create_project_with_id(context, projectId, title, completed, active, description):
    create_project(context=context,
                   title=title,
                   completed=completed,
                   active=active,
                   description=description,
                   project_id=projectId)


@then('the project {project} should be created')
def step_then_project_created(context, project):
    
    project_fields = project.split(",")

    expected_project = {
        "title": project_fields[0],
        "completed": project_fields[1],
        "active": project_fields[2],
        "description": project_fields[3]
    }


    print(expected_project)

    assert_project(expected=expected_project, 
                   actual=context.actual_project, 
                   compare_id=False)

@then('the response should have status code {statusCode}')
def step_then_response_status_code(context, statusCode):
    assert f"{context.response.status_code}" == statusCode

@then('the error message {errorMessage} should be raised')
def step_then_response_error_message(context, errorMessage):
    assert context.response.json().get("errorMessages") == [errorMessage]
