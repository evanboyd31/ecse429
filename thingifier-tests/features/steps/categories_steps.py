import httpx
import parse
import xmltodict

from behave import given, when, then
from shared_steps import remove_all, url

categories_url = f"{url}categories"


def create_category(title, description):
    response = httpx.post(
        categories_url, json={"title": title, "description": description}
    )
    return response


def get_category_id(title):
    response = httpx.get(categories_url)
    categories = response.json()["categories"]
    for category in categories:
        if category["title"] == title:
            return category["id"]
    return None


@given("no objects exist in the thingifier app other than the following categories")
def step_given(context):
    # Code to ensure no objects exist other than the provided categories
    remove_all()

    for row in context.table:
        # Add each category to the application
        create_category(row["title"], row["description"])


# -------------------------- CREATE


@when(
    'the user attempts to create a category with title "{title}" and description "{description}"'
)
def when_create_category_with_title_and_description(context, title, description):
    response = create_category(title, description)
    context.response = response


@then(
    'a category with title "{title}" and description "{description}" should exist in the thingifier app'
)
def then_category_with_title_and_description_should_exist(context, title, description):
    response = httpx.get(categories_url)
    categories = response.json()["categories"]
    found = any(
        category["title"] == title and category["description"] == description
        for category in categories
    )
    assert (
        found
    ), f"Category with title '{title}' and description '{description}' not found"


@when('the user attempts to create a category with only title "{title}"')
def when_create_category_with_only_title(context, title):
    response = httpx.post(categories_url, json={"title": title})
    context.response = response


@then('a category with title "{title}" should exist in the thingifier app')
def then_category_with_title_should_exist(context, title):
    response = httpx.get(categories_url)
    categories = response.json()["categories"]
    found = any(category["title"] == title for category in categories)
    assert found, f"Category with title '{title}' not found"


@when(
    'the user attempts to create a category with id "{id}", title "{title}" and description "{description}"'
)
def when_create_category_with_id_title_and_description(context, id, title, description):
    response = httpx.post(
        categories_url, json={"id": id, "title": title, "description": description}
    )
    context.response = response


# -------------------------- DELETE


@when(
    'the user attempts to delete using only the id of the category with title "{title}"'
)
def when_delete_category_by_title(context, title):
    category_id = get_category_id(title)
    assert category_id is not None, f"Category with title '{title}' not found"
    context.response = httpx.delete(f"{categories_url}/{category_id}")


@when(
    'the user attempts to delete using the id of the category with title "{title}" and extra query parameters "{body}"'
)
def when_delete_category_by_title_with_params(context, title, body):
    category_id = get_category_id(title)
    assert category_id is not None, f"Category with title '{title}' not found"
    context.response = httpx.delete(f"{categories_url}/{category_id}", params=body)


@when('the user attempts to delete using a non-existent category id "{id}"')
def when_delete_non_existent_category(context, id):
    context.response = httpx.delete(f"{categories_url}/{id}")


@then('category with title "{title}" should no longer exist in the thingifier app')
def then_category_should_not_exist(context, title):
    category_id = get_category_id(title)
    assert category_id is None, f"Category with title '{title}' still exists"


# -------------------------- UPDATE


@when(
    'the user attempts to update the category with title "{title}" to have title "{newTitle}" and description "{newDescription}"'
)
def when_update_category_all_fields(context, title, newTitle, newDescription):
    category_id = get_category_id(title)
    assert category_id is not None, f"Category with title '{title}' not found"
    context.response = httpx.post(
        f"{categories_url}/{category_id}",
        json={"title": newTitle, "description": newDescription},
    )


@when(
    'the user attempts to update the category with title "{title}" to have title "{newTitle}"'
)
def when_update_category_title_only(context, title, newTitle):
    category_id = get_category_id(title)
    assert category_id is not None, f"Category with title '{title}' not found"
    context.response = httpx.post(
        f"{categories_url}/{category_id}", json={"title": newTitle}
    )


@when(
    'the user attempts to update a non-existent category with id "{id}" to have title "{title}"'
)
def when_update_non_existent_category(context, id, title):
    context.response = httpx.post(f"{categories_url}/{id}", json={"title": title})


@then(
    'the response should contain the updated category with title "{newTitle}" and description "{newDescription}"'
)
def then_response_contains_updated_category_all_fields(
    context, newTitle, newDescription
):
    response_json = context.response.json()
    print(response_json)
    assert (
        response_json["title"] == newTitle
    ), f"Expected title '{newTitle}', but got '{response_json['title']}'"
    assert (
        response_json["description"] == newDescription
    ), f"Expected description '{newDescription}', but got '{response_json['description']}'"


@then(
    'the response should contain the updated category with title "{newTitle}" and the original description "{description}"'
)
def then_response_contains_updated_category_title_only(context, newTitle, description):
    response_json = context.response.json()
    assert (
        response_json["title"] == newTitle
    ), f"Expected title '{newTitle}', but got '{response_json['title']}'"
    assert (
        response_json["description"] == description
    ), f"Expected description '{description}', but got '{response_json['description']}'"


# -------------------------- VIEW ALL


@when("the user attempts to view all categories in JSON format")
def when_view_all_categories_json(context):
    context.response = httpx.get(categories_url, headers={"Accept": "application/json"})


@when("the user attempts to view all categories in XML format")
def when_view_all_categories_xml(context):
    context.response = httpx.get(categories_url, headers={"Accept": "application/xml"})


@when("the user attempts to view all categories")
def when_view_all_categories(context):
    context.response = httpx.get(categories_url)


@then("the response should contain a JSON array of all categories")
def then_response_contains_json_array(context):
    response_json = context.response.json()
    assert isinstance(
        response_json["categories"], list
    ), f"Expected a JSON array, but got {type(response_json['categories'])}"
    assert all(
        isinstance(category, dict) for category in response_json["categories"]
    ), "Expected all items to be JSON objects"


@then("the response should contain an XML array of all categories")
def then_response_contains_xml_array(context):
    response_dict = xmltodict.parse(context.response.text)
    categories = response_dict.get("categories", {}).get("category", [])
    if isinstance(categories, dict):
        categories = [categories]
    assert isinstance(
        categories, list
    ), f"Expected an XML array, but got {type(categories)}"
    assert all(
        isinstance(category, dict) for category in categories
    ), "Expected all items to be XML objects"


@then("the response should contain an empty array")
def then_response_contains_empty_array(context):
    response_json = context.response.json()
    assert (
        response_json["categories"][0]["categories"] == []
    ), f"Expected an empty array, but got {response_json['categories']}"


# -------------------------- VIEW SPECIFIC


@when(
    'the user attempts to view a category with the id of the category with title "{title}"'
)
def when_view_category_by_id(context, title):
    category_id = get_category_id(title)
    assert category_id is not None, f"Category with title '{title}' not found"
    context.response = httpx.get(f"{categories_url}/{category_id}")


@when('the user attempts to view a category with title "{title}"')
def when_view_category_by_title(context, title):
    category_id = get_category_id(title)
    assert category_id is not None, f"Category with title '{title}' not found"
    context.response = httpx.get(f"{categories_url}?title={title}")


@when('the user attempts to view a category with non-existent id "{id}"')
def when_view_non_existent_category(context, id):
    context.response = httpx.get(f"{categories_url}/{id}")


@then(
    'the response should contain the category with title "{title}" and description "{description}"'
)
def then_response_contains_category(context, title, description):
    response_json = context.response.json()
    assert (
        response_json["categories"][0]["title"] == title
    ), f"Expected title '{title}', but got '{response_json['title']}'"
    assert (
        response_json["categories"][0]["description"] == description
    ), f"Expected description '{description}', but got '{response_json['description']}'"
