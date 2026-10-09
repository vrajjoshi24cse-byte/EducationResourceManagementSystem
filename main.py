import tkinter as tk
from tkinter import ttk, messagebox

import data_manager as dm
import reports


class ResourceManager:

    def __init__(self, root):
        self.root = root

        self.root.title(
            "Education Resource Management System"
        )

        self.root.geometry("1000x650")

        self.resources = dm.load_resources()
        self.issues = dm.load_issues()

        self.selected_id = None

        self.build_gui()
        self.refresh_table()
        self.refresh_issues()

    def build_gui(self):

        tk.Label(
            self.root,
            text="Education Resource Management System",
            font=("Arial", 18, "bold")
        ).pack(pady=10)

        form = tk.Frame(self.root)
        form.pack(pady=10)

        self.name = tk.StringVar()
        self.category = tk.StringVar(value="Book")
        self.quantity = tk.StringVar(value="1")
        self.location = tk.StringVar()

        tk.Label(form, text="Resource Name").grid(
            row=0, column=0, padx=5
        )
        tk.Entry(form, textvariable=self.name).grid(
            row=1, column=0, padx=5
        )

        tk.Label(form, text="Category").grid(
            row=0, column=1, padx=5
        )
        ttk.Combobox(
            form,
            textvariable=self.category,
            values=[
                "Book", "Laptop", "Projector",
                "Lab Equipment", "Other"
            ]
        ).grid(row=1, column=1, padx=5)

        tk.Label(form, text="Quantity").grid(
            row=0, column=2, padx=5
        )
        tk.Entry(
            form, textvariable=self.quantity
        ).grid(row=1, column=2, padx=5)

        tk.Label(form, text="Location").grid(
            row=0, column=3, padx=5
        )
        tk.Entry(
            form, textvariable=self.location
        ).grid(row=1, column=3, padx=5)

        buttons = tk.Frame(self.root)
        buttons.pack(pady=5)

        tk.Button(
            buttons, text="Add Resource",
            command=self.add_resource
        ).pack(side="left", padx=5)

        tk.Button(
            buttons, text="Update",
            command=self.update_resource
        ).pack(side="left", padx=5)

        tk.Button(
            buttons, text="Delete",
            command=self.delete_resource
        ).pack(side="left", padx=5)

        tk.Button(
            buttons, text="Clear",
            command=self.clear_form
        ).pack(side="left", padx=5)

        columns = (
            "name", "category", "total",
            "available", "location", "uses"
        )

        self.tree = ttk.Treeview(
            self.root,
            columns=columns,
            show="headings",
            height=10
        )

        headings = {
            "name": "Resource Name",
            "category": "Category",
            "total": "Total",
            "available": "Available",
            "location": "Location",
            "uses": "Times Issued"
        }

        for col in columns:
            self.tree.heading(col, text=headings[col])

        self.tree.pack(
            fill="both", expand=True, padx=10, pady=10
        )

        self.tree.bind(
            "<<TreeviewSelect>>",
            self.select_resource
        )

        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill="both", expand=True, padx=10)

        self.issue_tab = tk.Frame(self.tabs)
        self.report_tab = tk.Frame(self.tabs)

        self.tabs.add(
            self.issue_tab, text="Issue / Return"
        )
        self.tabs.add(
            self.report_tab, text="Reports"
        )

        self.build_issue_tab()
        self.build_report_tab()

    def add_resource(self):
        try:
            dm.add_resource(
                self.resources,
                self.name.get(),
                self.category.get(),
                self.quantity.get(),
                self.location.get()
            )

            self.refresh_table()
            self.clear_form()

            messagebox.showinfo(
                "Success", "Resource added successfully."
            )

        except (ValueError, OSError) as error:
            messagebox.showerror("Error", str(error))

    def update_resource(self):
        if not self.selected_id:
            messagebox.showwarning(
                "Warning", "Select a resource first."
            )
            return

        try:
            dm.update_resource(
                self.resources,
                self.selected_id,
                self.name.get(),
                self.category.get(),
                self.quantity.get(),
                self.location.get()
            )

            self.refresh_table()
            messagebox.showinfo(
                "Success", "Resource updated."
            )

        except (ValueError, OSError) as error:
            messagebox.showerror("Error", str(error))

    def delete_resource(self):
        if not self.selected_id:
            messagebox.showwarning(
                "Warning", "Select a resource first."
            )
            return

        try:
            dm.delete_resource(
                self.resources, self.selected_id
            )

            self.clear_form()
            self.refresh_table()

        except (ValueError, OSError) as error:
            messagebox.showerror("Error", str(error))

    def select_resource(self, event=None):
        selected = self.tree.selection()

        if not selected:
            return

        self.selected_id = selected[0]

        resource = next(
            (
                r for r in self.resources
                if r["id"] == self.selected_id
            ),
            None
        )

        if resource:
            self.name.set(resource["name"])
            self.category.set(resource["category"])
            self.quantity.set(str(resource["total"]))
            self.location.set(resource["location"])

    def clear_form(self):
        self.selected_id = None
        self.name.set("")
        self.category.set("Book")
        self.quantity.set("1")
        self.location.set("")

        for item in self.tree.selection():
            self.tree.selection_remove(item)

    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for r in self.resources:
            self.tree.insert(
                "",
                "end",
                iid=r["id"],
                values=(
                    r["name"],
                    r["category"],
                    r["total"],
                    r["available"],
                    r["location"],
                    r["uses"]
                )
            )

    def build_issue_tab(self):
        self.borrower = tk.StringVar()
        self.issue_quantity = tk.StringVar(value="1")
        self.issue_resource = tk.StringVar()

        tk.Label(
            self.issue_tab, text="Student / Staff Name"
        ).grid(row=0, column=0, padx=5, pady=5)

        tk.Entry(
            self.issue_tab, textvariable=self.borrower
        ).grid(row=1, column=0, padx=5)

        tk.Label(
            self.issue_tab, text="Resource"
        ).grid(row=0, column=1, padx=5)

        self.resource_box = ttk.Combobox(
            self.issue_tab,
            textvariable=self.issue_resource,
            state="readonly",
            width=35
        )
        self.resource_box.grid(
            row=1, column=1, padx=5
        )

        tk.Label(
            self.issue_tab, text="Quantity"
        ).grid(row=0, column=2, padx=5)

        tk.Entry(
            self.issue_tab,
            textvariable=self.issue_quantity,
            width=8
        ).grid(row=1, column=2, padx=5)

        tk.Button(
            self.issue_tab,
            text="Issue Resource",
            command=self.issue_item
        ).grid(row=1, column=3, padx=5)

        self.issue_tree = ttk.Treeview(
            self.issue_tab,
            columns=(
                "borrower", "resource",
                "quantity", "date", "status"
            ),
            show="headings",
            height=5
        )

        for col, title in [
            ("borrower", "Borrower"),
            ("resource", "Resource"),
            ("quantity", "Quantity"),
            ("date", "Issue Date"),
            ("status", "Status")
        ]:
            self.issue_tree.heading(col, text=title)

        self.issue_tree.grid(
            row=2, column=0, columnspan=4,
            sticky="nsew", padx=5, pady=10
        )

        tk.Button(
            self.issue_tab,
            text="Return Selected",
            command=self.return_item
        ).grid(row=3, column=3, pady=5)

    def issue_item(self):
        selected = self.issue_resource.get()

        if not selected:
            messagebox.showerror(
                "Error", "Select a resource."
            )
            return

        resource_id = selected.split(" | ID: ")[-1]

        try:
            dm.issue_resource(
                self.resources,
                self.issues,
                resource_id,
                self.borrower.get(),
                self.issue_quantity.get()
            )

            self.refresh_all()
            messagebox.showinfo(
                "Success", "Resource issued successfully."
            )

        except (ValueError, OSError) as error:
            messagebox.showerror("Error", str(error))

    def return_item(self):
        selected = self.issue_tree.selection()

        if not selected:
            messagebox.showwarning(
                "Warning", "Select an issue record."
            )
            return

        try:
            dm.return_resource(
                self.resources, self.issues, selected[0]
            )

            self.refresh_all()
            messagebox.showinfo(
                "Success", "Resource returned successfully."
            )

        except (ValueError, OSError) as error:
            messagebox.showerror("Error", str(error))

    def refresh_issues(self):
        for item in self.issue_tree.get_children():
            self.issue_tree.delete(item)

        for issue in self.issues:
            self.issue_tree.insert(
                "",
                "end",
                iid=issue["id"],
                values=(
                    issue["borrower"],
                    issue["resource_name"],
                    issue["quantity"],
                    issue["date"],
                    issue["status"]
                )
            )

        self.resource_box["values"] = [
            f"{r['name']} (available: {r['available']}) | ID: {r['id']}"
            for r in self.resources
            if r["available"] > 0
        ]

    def build_report_tab(self):
        tk.Button(
            self.report_tab,
            text="Resource Quantity Chart",
            command=self.quantity_chart
        ).pack(pady=5)

        tk.Button(
            self.report_tab,
            text="Frequently Used Resources",
            command=self.usage_chart
        ).pack(pady=5)

        tk.Button(
            self.report_tab,
            text="Show Usage Summary",
            command=self.show_summary
        ).pack(pady=5)

        self.summary_text = tk.Text(
            self.report_tab, height=7
        )
        self.summary_text.pack(
            fill="both", expand=True, padx=10, pady=5
        )

    def quantity_chart(self):
        try:
            reports.quantity_chart(self.resources)
        except (ValueError, ImportError) as error:
            messagebox.showerror("Report Error", str(error))

    def usage_chart(self):
        try:
            reports.usage_chart(self.resources)
        except (ValueError, ImportError) as error:
            messagebox.showerror("Report Error", str(error))

    def show_summary(self):
        summary = reports.usage_summary(
            self.resources, self.issues
        )

        self.summary_text.delete("1.0", tk.END)
        self.summary_text.insert(tk.END, summary)

    def refresh_all(self):
        self.refresh_table()
        self.refresh_issues()


if __name__ == "__main__":
    root = tk.Tk()
    app = ResourceManager(root)
    root.mainloop()