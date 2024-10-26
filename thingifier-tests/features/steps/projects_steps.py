import httpx

from behave import given, when, then

projects_url = "http://localhost:4567/projects"


def assert_project(expected, actual, compare_id=False):

    if compare_id:
        assert expected.get("id") == actual.get("id")
    
    assert repr(expected.get("title")) == repr(actual.get("title"))
    assert repr(expected.get("completed")) == repr(actual.get("completed"))
    assert repr(expected.get("active")) == repr(actual.get("active"))
    assert repr(actual.get("description")) == repr((expected.get("description"))), f"{expected.get("description")}, {actual.get("description")[1:-1]}"

def create_project_JSON(title, completed, active, description, project_id=None):
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
            "completed": True if completed == "true" else (False if completed == "false" else completed)
        })
    
    if active and active != "N/A":
        project.update({
            "active": True if active == "true" else (False if active == "false" else active),
        })

    return project

def create_project(context, title, completed, active, description, project_id=None):

    project = create_project_JSON(title=title,
                                  completed=completed,
                                  active=active,
                                  description=description,
                                  project_id=project_id)
    
    # ensure correct error messages and codes and check that no extra project has been created
    response = httpx.post(projects_url, json=project)

    context.response = response

    context.actual_project = response.json()

def update_project(context, title, completed, active, description, project_id, use_post_url=True):
    project = create_project_JSON(title=title,
                                  completed=completed,
                                  active=active,
                                  description=description)
    
    response = None
    if use_post_url:
        response = httpx.post(f"{projects_url}/{project_id}", json=project)
    else:
        response = httpx.put(f"{projects_url}/{project_id}", json=project)
    
    context.response = response
    context.actual_project = response.json()

@given('the following projects are the only objects that exist in the system')
def step_given_projects_exist_in_the_system(context):

    # first delete all projects in the system
    response = httpx.get(f"{projects_url}")
    projects = response.json().get("projects")
    for project in projects:
        id = project.get("id")
        response = httpx.delete(f"{projects_url}/{id}")
        assert response.status_code == 200

    context.title_id_map = {}

    for row in context.table:
        title = row.get("title")
        completed = row.get("completed")
        active = row.get("active")
        description = row.get("description")

        create_project(context=context,
                       title=title,
                       completed=completed,
                       active=active,
                       description=description)
        
        id = context.response.json().get("id")

        context.title_id_map.update({
            title: id
        })
        

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


@when('the user deletes project with title {title}')
def step_when_user_deletes_project_with_title(context, title):
    project_id = context.title_id_map.get(title, -1)
    response = httpx.delete(f"{projects_url}/{project_id}")

    context.response = response


@when('the user sends extra query parameters {parameters} with values {values} when deleting project with title {title}')
def step_when_the_user_deletes_project_with_id_and_extra_query_params(context, title, parameters, values):
    project_id = context.title_id_map.get(title, -1)
    parameters = parameters.split(",")
    values = values.split(",")

    query_param_string = "?"
    for i, param in enumerate(parameters):
        value = values[i]
        current_param_string = f"{param}={value}{"&" if i != len(parameters) else ""}"
        query_param_string += current_param_string

    response = httpx.delete(f"{projects_url}/{project_id}{query_param_string}")

    context.response = response


@when('the user updates the project with title {title} by specifying new title {newTitle}, completed {newCompleted}, active {newActive}, and description {newDescription} using POST /projects/:id')
def step_when_user_updates_project_using_post(context, title, newTitle, newCompleted, newActive, newDescription):
    project_id = context.title_id_map.get(title)
    update_project(context=context, 
                   title=newTitle, 
                   completed=newCompleted, 
                   active=newActive, 
                   description=newDescription, 
                   project_id=project_id, 
                   use_post_url=True)
    
@when('the user updates the project with title {title} by specifying new title {newTitle}, completed {newCompleted}, active {newActive}, and description {newDescription} using PUT /projects/:id')
def step_when_user_updates_project_using_post(context, title, newTitle, newCompleted, newActive, newDescription):
    project_id = context.title_id_map.get(title)
    update_project(context=context, 
                   title=newTitle, 
                   completed=newCompleted, 
                   active=newActive, 
                   description=newDescription, 
                   project_id=project_id, 
                   use_post_url=False)

@then('the project {project} should be created')
def step_then_project_created(context, project):
    
    project_fields = project.split(",")

    expected_project = {
        "title": project_fields[0],
        "completed": project_fields[1],
        "active": project_fields[2],
        "description": project_fields[3]
    }

    assert_project(expected=expected_project, 
                   actual=context.actual_project, 
                   compare_id=False)
    
@then('the project that had title {title} should have the new fields {project}')
def step_then_project_that_had_title_has_new_fields(context, title, project):
    project_fields = project.split(",")

    expected_project = {
        "title": project_fields[0],
        "completed": project_fields[1],
        "active": project_fields[2],
        "description": project_fields[3]
    }

    print(expected_project)
    print(context.actual_project)

    assert_project(expected=expected_project,
                   actual=context.actual_project,
                   compare_id=False)


@then('the response should have status code {statusCode}')
def step_then_response_status_code(context, statusCode):
    assert f"{context.response.status_code}" == statusCode


@then('the error message {errorMessage} should be raised')
def step_then_response_error_message(context, errorMessage):
    assert context.response.json().get("errorMessages") == [errorMessage]


@then('the project with title {title} should not exist in the system')
def step_then_project_with_title_should_not_exist_in_the_system(context, title):
    # assert the original response gives 200
    assert context.response.status_code == 200

    # assert new response gives 404 and error message
    response = httpx.get(f"{projects_url}")
    projects = response.json().get("projects")

    for project in projects:
        assert project.get("title") != title

@then('an error message indicating the project could not be found is raised')
def step_then_error_message_indicating_project_not_found(context):

    # since we do not know what the id of the project is during unit testing, just ensure the prefix lies in the response's error message
    assert len(context.response.json().get("errorMessages")) == 1
    errorMessage = context.response.json().get("errorMessages")[0]
    assert "Could not find any instances with projects/" in errorMessage