import httpx

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

@given('the following projects exist in the system')
def step_given_projects_exist_in_the_system(context):

    # create fake id map for mapping real project ids to the ids specified in feature files
    context.fake_id_map = {}

    for row in context.table:
        fake_id = row.get("id")
        title = row.get("title")
        completed = row.get("completed")
        active = row.get("active")
        description = row.get("description")

        create_project(context=context,
                       title=title,
                       completed=completed,
                       active=active,
                       description=description)
        
        real_project_id = context.response.json().get("id")
        
        context.fake_id_map[fake_id] = real_project_id

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

@when('the user deletes project with id {id}')
def step_when_user_deletes_project_with_id(context, id):
    real_id = context.fake_id_map.get(id, id)
    response = httpx.delete(f"{projects_url}/{real_id}")

    context.response = response

@when('the user sends extra query parameters {parameters} with values {values} when deleting project with id {id}')
def step_when_the_user_deletes_project_with_id_and_extra_query_params(context, id, parameters, values):
    real_id = context.fake_id_map.get(id, id)
    parameters = parameters.split(",")
    values = values.split(",")

    query_param_string = "?"
    for i, param in enumerate(parameters):
        value = values[i]
        current_param_string = f"{param}={value}{"&" if i != len(parameters) else ""}"
        query_param_string += current_param_string

    response = httpx.delete(f"{projects_url}/{real_id}{query_param_string}")

    context.response = response


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
    print(errorMessage)
    print(context.response.json().get("errorMessages"))
    assert context.response.json().get("errorMessages") == [errorMessage]

@then('the project with id {id} should not exist in the system')
def step_then_project_with_id_should_not_exist_in_the_system(context, id):
    # assert the original response gives 200
    assert context.response.status_code == 200

    # assert new response gives 404 and error message
    real_id = context.fake_id_map.get("id", id)
    response = httpx.get(f"{projects_url}/{real_id}")

    assert response.status_code == 404
    print(response.json().get("errorMessages"))
    print()
    assert response.json().get("errorMessages") == [f"Could not find an instance with projects/{real_id}"]