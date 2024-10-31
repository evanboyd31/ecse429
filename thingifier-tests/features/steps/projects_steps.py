import httpx
import json
import xmltodict

from behave import given, when, then


projects_url = "http://localhost:4567/projects"
XML_HEADERS = {"Content-Type": "application/xml", "Accept": "application/xml"}


def assert_project(expected, actual, compare_id=False):

    if compare_id:
        assert expected.get("id") == actual.get("id")

    assert repr(expected.get("title")) == repr(actual.get("title"))
    assert repr(expected.get("completed")) == repr(actual.get("completed"))
    assert repr(expected.get("active")) == repr(actual.get("active"))
    assert repr(actual.get("description")) == repr(
        (expected.get("description"))
    ), f"{expected.get("description")}, {actual.get("description")[1:-1]}"


def is_identical_project(project1, project2):
    same_title = project1.get("title") == project2.get("title")
    same_completed = (
        "true"
        if project1.get("completed") is True or project1.get("completed") == "true"
        else "false"
    ) == (
        "true"
        if project2.get("completed") is True or project2.get("completed") == "true"
        else "false"
    )
    same_active = (
        "true"
        if project1.get("active") or project1.get("active") == "true"
        else "false"
    ) == (
        "true"
        if project2.get("active") or project2.get("active") == "true"
        else "false"
    )
    same_description = project1.get("description") == project2.get("description")
    return same_title and same_completed and same_active and same_description


def create_project_JSON(title, completed, active, description, project_id=None):
    project = {}

    # all fields are optional, so only specify if necessary

    if project_id and project_id != "N/A":
        project.update({"id": project_id})

    if title and title != "N/A":
        project.update({"title": title})

    if description and description != "N/A":
        project.update({"description": description})

    if completed and completed != "N/A":
        project.update(
            {
                "completed": (
                    True
                    if completed == "true"
                    else (False if completed == "false" else completed)
                )
            }
        )

    if active and active != "N/A":
        project.update(
            {
                "active": (
                    True
                    if active == "true"
                    else (False if active == "false" else active)
                ),
            }
        )

    return project


def create_project(context, title, completed, active, description, project_id=None):

    project = create_project_JSON(
        title=title,
        completed=completed,
        active=active,
        description=description,
        project_id=project_id,
    )

    # ensure correct error messages and codes and check that no extra project has been created
    response = httpx.post(projects_url, json=project)

    context.response = response

    context.actual_project = response.json()


def update_project(
    context, title, completed, active, description, project_id, use_post_url=True
):
    project = create_project_JSON(
        title=title, completed=completed, active=active, description=description
    )

    response = None
    if use_post_url:
        response = httpx.post(f"{projects_url}/{project_id}", json=project)
    else:
        response = httpx.put(f"{projects_url}/{project_id}", json=project)

    context.response = response
    context.actual_project = response.json()


def delete_all_projects():
    response = httpx.get(f"{projects_url}")
    projects = response.json().get("projects")
    for project in projects:
        id = project.get("id")
        response = httpx.delete(f"{projects_url}/{id}")
        assert response.status_code == 200


def assert_project1_project2_are_response(projects, project1, project2):

    assert len(projects) == 2

    # ensure both projects compose the list of returned projects
    for project in projects:
        if project.get("title") == project1.get("title"):
            assert project.get("completed") == (
                "true"
                if project1.get("completed") is True
                or project1.get("completed") == "true"
                else "false"
            )
            assert project.get("active") == (
                "true"
                if project1.get("active") or project1.get("active") == "true"
                else "false"
            )
            assert project.get("description") == project1.get("description")
        else:
            assert project.get("title") == project2.get("title")
            assert project.get("completed") == (
                "true"
                if project2.get("completed") is True
                or project2.get("completed") == "true"
                else "false"
            )
            assert project.get("active") == (
                "true"
                if project2.get("active") is True or project2.get("active") == "true"
                else "false"
            )
            assert project.get("description") == project2.get("description")


def assert_project_is_in_response(projects, project):
    project_in_response = False
    for response_project in projects:
        project_in_response = (
            is_identical_project(project1=response_project, project2=project)
            or project_in_response
        )

    assert project_in_response


@given("no objects exist other than the following projects")
def step_given_projects_exist_in_the_system(context):

    # first delete all projects in the system
    delete_all_projects()

    context.title_id_map = {}

    for row in context.table:
        title = row.get("title")
        completed = row.get("completed")
        active = row.get("active")
        description = row.get("description")

        create_project(
            context=context,
            title=title,
            completed=completed,
            active=active,
            description=description,
        )

        id = context.response.json().get("id")

        context.title_id_map.update({title: id})


@given("all projects in the system have been deleted")
def step_given_all_projects_deleted(context):
    delete_all_projects()


@given("{project2} has been deleted from the system")
def step_given_project_has_been_deleted_from_system(context, project2):

    project2_json = json.loads(project2)
    response = httpx.get(f"{projects_url}")
    projects = response.json().get("projects")

    for project in projects:
        if is_identical_project(project1=project, project2=project2_json):
            id = project.get("id")
            response = httpx.delete(f"{projects_url}/{id}")
            assert response.status_code == 200


@when(
    "the user creates a project by specifying title {title}, completed {completed}, active {active}, and description {description}"
)
def step_when_create_project(context, title, completed, active, description):
    create_project(
        context=context,
        title=title,
        completed=completed,
        active=active,
        description=description,
    )


@when(
    "the user creates a project with missing fields by specifying title {title}, completed {completed}, active {active}, and description {description}"
)
def step_when_create_project(context, title, completed, active, description):
    create_project(
        context=context,
        title=title,
        completed=completed,
        active=active,
        description=description,
    )


@when(
    "the user attempts to create a project by specifying id {projectId}, title {title}, completed {completed}, active {active}, and description {description}"
)
def step_when_create_project_with_id(
    context, projectId, title, completed, active, description
):
    create_project(
        context=context,
        title=title,
        completed=completed,
        active=active,
        description=description,
        project_id=projectId,
    )


@when("the user deletes project with title {title}")
def step_when_user_deletes_project_with_title(context, title):
    project_id = context.title_id_map.get(title, -1)
    response = httpx.delete(f"{projects_url}/{project_id}")

    context.response = response


@when(
    "the user sends extra query parameters {parameters} with values {values} when deleting project with title {title}"
)
def step_when_the_user_deletes_project_with_id_and_extra_query_params(
    context, title, parameters, values
):
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


@when(
    "the user updates the project with title {title} by specifying new title {newTitle}, completed {newCompleted}, active {newActive}, and description {newDescription} using POST /projects/:id"
)
def step_when_user_updates_project_using_post(
    context, title, newTitle, newCompleted, newActive, newDescription
):
    project_id = context.title_id_map.get(title)
    update_project(
        context=context,
        title=newTitle,
        completed=newCompleted,
        active=newActive,
        description=newDescription,
        project_id=project_id,
        use_post_url=True,
    )


@when(
    "the user updates the project with title {title} by specifying new title {newTitle}, completed {newCompleted}, active {newActive}, and description {newDescription} using PUT /projects/:id"
)
def step_when_user_updates_project_using_post(
    context, title, newTitle, newCompleted, newActive, newDescription
):
    project_id = context.title_id_map.get(title)
    update_project(
        context=context,
        title=newTitle,
        completed=newCompleted,
        active=newActive,
        description=newDescription,
        project_id=project_id,
        use_post_url=False,
    )


@when("the user attempts to view all projects in JSON format")
def step_when_user_views_all_projects_in_JSON(context):
    response = httpx.get(f"{projects_url}")
    context.response = response


@when("the user attempts to view all projects in XML format")
def step_when_user_views_all_projects_in_XML(context):
    response = httpx.get(f"{projects_url}", headers=XML_HEADERS)
    context.response = response


@when("the user attempts to view all active projects in JSON format")
def step_when_user_views_all_active_projects_in_JSON(context):
    response = httpx.get(f"{projects_url}?active=true")
    context.response = response


@when("the user attempts to view all active projects in XML format")
def step_when_user_views_all_active_projects_in_JSON(context):
    response = httpx.get(f"{projects_url}?active=true", headers=XML_HEADERS)
    context.response = response


@then("the project {project} should be created")
def step_then_project_created(context, project):

    project_fields = project.split(",")

    expected_project = {
        "title": project_fields[0],
        "completed": project_fields[1],
        "active": project_fields[2],
        "description": project_fields[3],
    }

    assert_project(
        expected=expected_project, actual=context.actual_project, compare_id=False
    )


@then("the project that had title {title} should have the new fields {project}")
def step_then_project_that_had_title_has_new_fields(context, title, project):
    project_fields = project.split(",")

    expected_project = {
        "title": project_fields[0],
        "completed": project_fields[1],
        "active": project_fields[2],
        "description": project_fields[3],
    }

    print(expected_project)
    print(context.actual_project)

    assert_project(
        expected=expected_project, actual=context.actual_project, compare_id=False
    )


@then("the response should have status code {statusCode}")
def step_then_response_status_code(context, statusCode):
    assert f"{context.response.status_code}" == statusCode


@then("the project with title {title} should not exist in the system")
def step_then_project_with_title_should_not_exist_in_the_system(context, title):
    # assert the original response gives 200
    assert context.response.status_code == 200

    # assert new response gives 404 and error message
    response = httpx.get(f"{projects_url}")
    projects = response.json().get("projects")

    for project in projects:
        assert project.get("title") != title


@then("an error message indicating the project could not be found is raised")
def step_then_error_message_indicating_project_not_found(context):

    # since we do not know what the id of the project is during unit testing, just ensure the prefix lies in the response's error message
    assert len(context.response.json().get("errorMessages")) == 1
    errorMessage = context.response.json().get("errorMessages")[0]
    assert "Could not find any instances with projects/" in errorMessage


@then("the user should see the projects {project1} and {project2} in the JSON response")
def step_then_user_sees_projects_in_JSON_response(context, project1, project2):
    projects = context.response.json().get("projects")

    project1_json = json.loads(project1)
    project2_json = json.loads(project2)

    # ensure both projects compose the list of projects
    assert_project1_project2_are_response(
        projects=projects, project1=project1_json, project2=project2_json
    )


@then("the user should see the projects {project1} and {project2} in the XML response")
def step_then_the_user_sees_projects_in_XML_response(context, project1, project2):

    response_dict = xmltodict.parse(context.response.content)
    projects = response_dict.get("projects").get("project")

    if isinstance(projects, dict):
        projects = [projects]

    project1_dict = xmltodict.parse(project1).get("project")
    project2_dict = xmltodict.parse(project2).get("project")

    # ensure both projects compose the list of projects
    assert_project1_project2_are_response(
        projects=projects, project1=project1_dict, project2=project2_dict
    )


@then("the user should receive an empty JSON array")
def step_then_the_user_receives_empty_JSON_array(context):
    assert context.response.json().get("projects") == []


@then(
    "the user should not see the projects {project1} and {project2} in the JSON response"
)
def step_then_the_user_should_not_see_project1_project2(context, project1, project2):
    projects = context.response.json().get("projects")
    assert len(projects) == 0

    project1_json = json.loads(project1)
    project1_json.update(
        {
            "completed": ("true" if project1_json.get("completed") else "false"),
            "active": ("true" if project1_json.get("active") else "false"),
        }
    )

    project2_json = json.loads(project2)
    project2_json.update(
        {
            "completed": ("true" if project2_json.get("completed") else "false"),
            "active": ("true" if project2_json.get("active") else "false"),
        }
    )

    assert project1_json not in projects
    assert project2_json not in projects


@then("the user should see the project {project2} in the JSON response")
def step_then_user_sees_project2_JSON(context, project2):
    projects = context.response.json().get("projects")

    project2_json = json.loads(project2)
    project2_json.update(
        {
            "completed": ("true" if project2_json.get("completed") else "false"),
            "active": ("true" if project2_json.get("active") else "false"),
        }
    )

    assert_project_is_in_response(projects=projects, project=project2_json)


@then("the user should see the project {project2} in the XML response")
def step_then_user_sees_project2_XML(context, project2):
    response_dict = xmltodict.parse(context.response.content)
    projects = response_dict.get("projects").get("project")

    if isinstance(projects, dict):
        projects = [projects]

    project2_dict = xmltodict.parse(project2).get("project")
    project2_dict.update(
        {
            "completed": (
                "true" if project2_dict.get("completed") is True else "false"
            ),
            "active": ("true" if project2_dict.get("active") is True else "false"),
        }
    )

    print(projects)

    print(project2_dict)
    print(type(project2_dict))

    assert_project_is_in_response(projects=projects, project=project2_dict)


@then("the user should not see the project {project1} in the JSON response")
def step_then_user_does_not_see_project1_JSON(context, project1):
    projects = context.response.json().get("projects")

    project1_json = json.loads(project1)
    project1_json.update(
        {
            "completed": ("true" if project1_json.get("completed") else "false"),
            "active": ("true" if project1_json.get("active") else "false"),
        }
    )

    for project in projects:
        assert not is_identical_project(project1=project, project2=project1_json)


@then("the user should not see the project {project1} in the XML response")
def step_then_user_does_not_see_project1(context, project1):
    response_dict = xmltodict.parse(context.response.content)
    projects = response_dict.get("projects").get("project")

    if isinstance(projects, dict):
        projects = [projects]

    project1_dict = xmltodict.parse(project1).get("project")
    project1_dict.update(
        {
            "completed": (
                "true" if project1_dict.get("completed") is True else "false"
            ),
            "active": ("true" if project1_dict.get("active") is True else "false"),
        }
    )

    for project in projects:
        assert not is_identical_project(project1=project, project2=project1_dict)
