import httpx
import pytest
import thingifier_tests.conftest as common

todos_url: str = "http://localhost:4567/todos"
categories_url: str = "http://localhost:4567/categories"
projects_url: str = "http://localhost:4567/projects"

# Note that ids will change every time
default: dict = {
    "todos": [
        {
            "id": "???",
            "title": "Play Daily Ball",
            "doneStatus": "true",
            "description": "",
        },
        {
            "id": "???",
            "title": "Buy Daily Ball Plus",
            "doneStatus": "false",
            "description": "",
        },
    ],
    "categories": [
        {
            "id": "???",
            "title": "Daily Ball",
            "description": "The #1 ball game in the world",
        },
        {
            "id": "???",
            "title": "Music",
            "description": "La musique",
        },
    ],
    "projects": [
        {
            "id": "???",
            "title": "test title 1",
            "completed": False,
            "active": False,
            "description": "test description 1",
        },
        {
            "id": "???",
            "title": "test title 2",
            "completed": False,
            "active": False,
            "description": "test description 2",
        },
    ]
}


@pytest.fixture(autouse=True)
def before_each():
    common.remove_all()

    def add_to_todos(title: str):
        res = httpx.post(todos_url, json={"title": title})
        print(res.json())
        todo = list(
            filter(lambda todo: todo["title"] == title, default["todos"])
        )[0]
        todo["id"] = res.json()["id"]

    def add_to_categories(title: str):
        res = httpx.post(categories_url, json={"title": title})
        print(res.json())
        category = list(
            filter(lambda category: category["title"] == title, default["categories"])
        )[0]
        category["id"] = res.json()["id"]

    def add_to_projects(title: str):
        res = httpx.post(projects_url, json={"title": title})
        print(res.json())
        project = list(
            filter(lambda project: project["title"] == title, default["projects"])
        )[0]
        project["id"] = res.json()["id"]

    for todo in default["todos"]:
        add_to_todos(todo["title"])

    for category in default["categories"]:
        add_to_categories(category["title"])
    
    for project in default["projects"]:
        add_to_projects(project["title"])
    
    # add relationship between todos and projects
    httpx.post(f"{todos_url}/{default['todos'][0]['id']}/tasksof", json={"id": default['projects'][0]['id']})

    # add relationship between todos and categories
    httpx.post(f"{todos_url}/{default['todos'][0]['id']}/categories", json={"id": default['categories'][0]['id']})

    # add relationship between projects and categories
    httpx.post(f"{projects_url}/{default['projects'][0]['id']}/categories", json={"id": default['categories'][0]['id']})

    # add relationship between categories and todos???
    httpx.post(f"{categories_url}/{default['categories'][0]['id']}/todos", json={"id": default['todos'][0]['id']})

    # add relationship between categories and projects
    httpx.post(f"{categories_url}/{default['categories'][0]['id']}/projects", json={"id": default['projects'][0]['id']})