import pandas as pd
import matplotlib.pyplot as plt


def quantity_chart(resources):
    if not resources:
        raise ValueError("No resources available.")

    df = pd.DataFrame(resources)

    df.plot(
        x="name",
        y=["total", "available"],
        kind="bar",
        title="Resource Availability"
    )

    plt.xlabel("Resource Name")
    plt.ylabel("Quantity")
    plt.tight_layout()
    plt.show()


def usage_chart(resources):
    if not resources:
        raise ValueError("No resources available.")

    df = pd.DataFrame(resources)

    df = df.sort_values(
        by="uses",
        ascending=False
    ).head(10)

    df.plot(
        x="name",
        y="uses",
        kind="bar",
        legend=False,
        title="Frequently Used Resources"
    )

    plt.xlabel("Resource Name")
    plt.ylabel("Times Used (Items Issued)")
    plt.tight_layout()
    plt.show()


def usage_summary(resources, issues):
    total = sum(r["total"] for r in resources)
    available = sum(r["available"] for r in resources)

    currently_issued = sum(
        i["quantity"]
        for i in issues
        if i["status"] == "Issued"
    )

    most_used = sorted(
        resources,
        key=lambda r: r["uses"],
        reverse=True
    )[:5]

    summary = (
        f"Resource Types: {len(resources)}\n"
        f"Total Items: {total}\n"
        f"Available Items: {available}\n"
        f"Currently Issued: {currently_issued}\n\n"
        "Most Frequently Used Resources:\n"
    )

    for resource in most_used:
        summary += (
            f"{resource['name']} - "
            f"{resource['uses']} items issued\n"
        )

    return summary