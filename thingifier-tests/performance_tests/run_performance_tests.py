import asyncio
from performance_tests.conftest import create_one_of_each
import psutil
import pytest


num_items = 0


async def monitor_system_usage():
    global num_items
    try:
        log_file_name = f"system_usage_{num_items}_items.log"
        with open(log_file_name, "w") as log_file:
            while True:
                cpu_usage = psutil.cpu_percent()
                memory_usage = psutil.virtual_memory().percent
                log_file.write(
                    f"CPU Usage: {cpu_usage}%, Memory Usage: {memory_usage}%\n"
                )
                log_file.flush()
                await asyncio.sleep(1)
    except asyncio.CancelledError:
        pass


async def run_pytest():
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, pytest.main, ["-s", "./"])


async def main(items_to_add: int):
    global num_items
    num_items += items_to_add

    for i in range(items_to_add):
        create_one_of_each()

    monitor_task = asyncio.create_task(monitor_system_usage())
    try:
        await run_pytest()
    finally:
        monitor_task.cancel()
        await monitor_task


if __name__ == "__main__":
    asyncio.run(main(1000))
