import json
import os
from datetime import datetime

DATA_FILE = "education_resources.json"
ISSUES_FILE = "resource_issues.json"


def load_data(filename):
    if os.path.exists(filename):
        try:
            with open(filename, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            return []
    return []


def save_data(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


def load_resources():
    return load_data(DATA_FILE)


def load_issues():
    return load_data(ISSUES_FILE)


def add_resource(resources, name, category, quantity, location):
    if not name.strip() or not category.strip() or not location.strip():
        raise ValueError("All fields are required.")

    quantity = int(quantity)

    if quantity < 1:
        raise ValueError("Quantity must be at least 1.")

    resource = {
        "id": str(int(datetime.now().timestamp() * 1000000)),
        "name": name.strip(),
        "category": category.strip(),
        "total": quantity,
        "available": quantity,
        "location": location.strip(),
        "uses": 0
    }

    resources.append(resource)
    save_data(DATA_FILE, resources)


def update_resource(resources, resource_id, name, category, quantity, location):
    resource = next(
        (r for r in resources if r["id"] == resource_id), None
    )

    if resource is None:
        raise ValueError("Resource not found.")

    quantity = int(quantity)
    issued = resource["total"] - resource["available"]

    if not name.strip() or not category.strip() or not location.strip():
        raise ValueError("All fields are required.")

    if quantity < max(1, issued):
        raise ValueError("Quantity cannot be less than items already issued.")

    resource.update({
        "name": name.strip(),
        "category": category.strip(),
        "total": quantity,
        "available": quantity - issued,
        "location": location.strip()
    })

    save_data(DATA_FILE, resources)


def delete_resource(resources, resource_id):
    resource = next(
        (r for r in resources if r["id"] == resource_id), None
    )

    if resource is None:
        raise ValueError("Resource not found.")

    if resource["available"] != resource["total"]:
        raise ValueError("Return all issued items before deleting.")

    resources.remove(resource)
    save_data(DATA_FILE, resources)


def issue_resource(resources, issues, resource_id, borrower, quantity):
    resource = next(
        (r for r in resources if r["id"] == resource_id), None
    )

    if resource is None:
        raise ValueError("Resource not found.")

    if not borrower.strip():
        raise ValueError("Enter the borrower's name.")

    quantity = int(quantity)

    if quantity < 1:
        raise ValueError("Quantity must be at least 1.")

    if quantity > resource["available"]:
        raise ValueError("Not enough resources available.")

    resource["available"] -= quantity
    resource["uses"] += quantity

    issue = {
        "id": str(int(datetime.now().timestamp() * 1000000)),
        "resource_id": resource_id,
        "resource_name": resource["name"],
        "borrower": borrower.strip(),
        "quantity": quantity,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "status": "Issued"
    }

    issues.append(issue)

    save_data(DATA_FILE, resources)
    save_data(ISSUES_FILE, issues)


def return_resource(resources, issues, issue_id):
    issue = next(
        (i for i in issues if i["id"] == issue_id), None
    )

    if issue is None or issue["status"] != "Issued":
        raise ValueError("Invalid or already returned record.")

    resource = next(
        (r for r in resources if r["id"] == issue["resource_id"]), None
    )

    if resource:
        resource["available"] = min(
            resource["total"],
            resource["available"] + issue["quantity"]
        )

    issue["status"] = "Returned"

    save_data(DATA_FILE, resources)
    save_data(ISSUES_FILE, issues)