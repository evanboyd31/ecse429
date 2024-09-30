import httpx

url_header : str = "http://localhost:4567/"

def remove_all():
    todos = httpx.get(url_header + "todos").json()['todos']
    categories = httpx.get(url_header + "categories").json()['categories']
    projects = httpx.get(url_header + "projects").json()['projects']
    
    for todo in todos:
        httpx.delete(url_header + "todos/" + todo['id'])
    for category in categories:
        httpx.delete(url_header + "categories/" + category['id'])
    for project in projects:
        httpx.delete(url_header + "projects/" + project['id'])