import asyncio
import subprocess
import os
from time import sleep
import psutil
import pytest
from performance_tests.conftest import *

num_items = 0


async def monitor_process_usage(process: psutil.Process):
    global num_items
    print(f"Doing {num_items} items")
    log_file_name = f"process_usage_{num_items}_items.log"
    try:
        with open(log_file_name, "w") as log_file:
            while True:
                try:
                    cpu_usage = process.cpu_percent(interval=None) / psutil.cpu_count()
                    memory_usage = process.memory_percent()
                    log_file.write(
                        f"CPU Usage: {cpu_usage:.2f}%, Memory Usage: {memory_usage:.2f}%\n"
                    )
                    log_file.flush()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    break
                await asyncio.sleep(0.1)
    except asyncio.CancelledError:
        pass


def find_process_by_name(name):
    # Iterate over all running processes
    for proc in psutil.process_iter(["pid", "name"]):
        try:
            if proc.info["name"] == name:
                print(f"Found process: {proc.info['name']} (PID: {proc.info['pid']})")
                return proc
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass


async def create_items_concurrently(items_to_add: int):
    tasks = [asyncio.to_thread(create_one_of_each) for _ in range(items_to_add)]
    await asyncio.gather(*tasks)


async def remove_all_concurrently():
    todos = httpx.get(url_header + "todos").json()["todos"]
    categories = httpx.get(url_header + "categories").json()["categories"]
    projects = httpx.get(url_header + "projects").json()["projects"]

    tasks = []
    for todo in todos:
        tasks.append(asyncio.to_thread(httpx.delete, url_header + "todos/" + todo["id"]))
    for category in categories:
        tasks.append(asyncio.to_thread(httpx.delete, url_header + "categories/" + category["id"]))
    for project in projects:
        tasks.append(asyncio.to_thread(httpx.delete, url_header + "projects/" + project["id"]))
    await asyncio.gather(*tasks)


async def run_pytest():
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, pytest.main, ["-s", "./"])


async def main():
    global num_items

    await remove_all_concurrently()

    process = find_process_by_name("java")

    item_counts = [10, 90, 400, 500, 1000, 3000, 5000]
    for items_to_add in item_counts:
        num_items += items_to_add
        await create_items_concurrently(items_to_add)

        monitor_task = asyncio.create_task(monitor_process_usage(process))

        await run_pytest()

        monitor_task.cancel()
        await monitor_task

    await remove_all_concurrently()


if __name__ == "__main__":
    asyncio.run(main())
