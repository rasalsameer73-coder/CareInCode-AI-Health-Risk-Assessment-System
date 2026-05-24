import matplotlib.pyplot as plt


def generate_health_graph(
    graph_points: list,
    parameter_name: str,
    output_path: str
):

    if not graph_points:

        return None

    x = []

    y = []

    for point in graph_points:

        x.append(
            point["report"]
        )

        y.append(
            point["value"]
        )

    plt.figure(figsize=(6, 3))

    plt.plot(
        x,
        y,
        marker="o"
    )

    plt.title(
        f"{parameter_name.upper()} Trend"
    )

    plt.xlabel(
        "Report Number"
    )

    plt.ylabel(
        parameter_name.upper()
    )

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(output_path)

    plt.close()

    return output_path