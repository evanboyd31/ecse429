import re
import os
import matplotlib.pyplot as plt


def parse_logs(log_files):
    # Data structure to store parsed data
    data = {}

    # Regex pattern to extract details
    pattern = re.compile(
        r"(?P<operation>.+?)(?:/id)?/test_(?P<test_name>.+)\.py .*?Test execution time: (?P<time>\d+\.\d+) seconds"
    )

    for file in log_files:
        num_items = file.split("_")[2]
        with open(file, "r") as f:
            for line in f:
                match = pattern.match(line)
                if match:
                    test_name = match.group("test_name")
                    time = float(match.group("time"))

                    if test_name not in data:
                        data[test_name] = []
                    data[test_name].append((num_items, time))
    return data


def plot_data(data):
    for key, values in data.items():
        num_items = [x[0] for x in values]
        times = [x[1] for x in values]

        # Plotting
        plt.figure()
        plt.plot(num_items, times, "o-", color="green")
        plt.xlabel("Number of items")
        plt.ylabel("Execution Time (seconds)")
        plt.title(f"Execution Time for {key}")
        plt.tight_layout()
        plt.grid(True)
        plt.savefig(f"execution_time_{key}.png")
        plt.show()


def main():
    # List of log files
    log_files = [
        f"test_output_{x}_items.log" for x in [10, 100, 500, 1000, 2000, 5000, 10000]
    ]

    # Parse the logs
    data = parse_logs(log_files)

    # Plot the data
    plot_data(data)


if __name__ == "__main__":
    main()
