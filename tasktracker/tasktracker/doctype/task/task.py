from frappe.model.document import Document
import frappe

class Task(Document):
    def validate(self):
        self.send_assignment_emails()

    def send_assignment_emails(self):
        if not self.assigned_to or not self.project:
            return

        for row in self.assigned_to:
            if not row.assigned_to:
                continue
            user = frappe.get_doc("User", row.assigned_to)
            email = user.email or row.assigned_to
            frappe.sendmail(
                recipients=[email],
                subject=f"You have been assigned to Task: {self.name}",
                message=f"Hi {user.first_name},<br><br>"
                        f"You have been assigned to <b>{self.name}</b> under Project <b>{self.project}</b>.<br><br>"
                        f"Due Date: {self.due_date or 'Not set'}<br>"
                        f"Description: {self.description or 'No description'}<br><br>"
                        f"Regards,<br>Task Tracker",
                now=True
            )

@frappe.whitelist()
def get_project_members(doctype, txt, searchfield, start, page_len, filters):
    project = filters.get("project")
    if not project:
        return []

    members = frappe.get_all(
        "User Table",  # This is the child table of the Project
        filters={"parent": project},
        fields=["assigned_to"]
    )

    return [(m.assigned_to,) for m in members if m.assigned_to]
