from frappe.model.document import Document
import frappe

class Task(Document):
    def validate(self):
        self.sync_status_with_workflow_state()
        self.send_assignment_emails()

    def sync_status_with_workflow_state(self):
        
        state_to_status_map = {
            "To Do": "To Do",
            "In working": "In Working",
            "Testing in progress": "Testing in Progress",
            "Completed": "Completed"
        }

        
        if self.workflow_state and self.workflow_state in state_to_status_map:
            self.status = state_to_status_map[self.workflow_state]

    def send_assignment_emails(self):
        
        if frappe.flags.get("skip_assignment_email"):
            return

        if not self.assigned_to or not self.project:
            return

        previous = self.get_doc_before_save()
        previous_assignees = set()
        if previous:
            previous_assignees = set(row.assigned_to for row in previous.assigned_to or [])

        current_assignees = set(row.assigned_to for row in self.assigned_to)

        if previous_assignees == current_assignees:
            return

        for row in self.assigned_to:
            if not row.assigned_to:
                continue

            try:
                user = frappe.get_doc("User", row.assigned_to)
                email = user.email or row.assigned_to

                frappe.sendmail(
                    recipients=[email],
                    subject=f"You have been assigned to Task: {self.name}",
                    message=f"""
                        Hi {user.first_name or user.full_name},<br><br>
                        You have been assigned to <b>{self.name}</b> under Project <b>{self.project}</b>.<br><br>
                        <b>Due Date:</b> {self.due_date or 'Not set'}<br>
                        <b>Description:</b> {self.description or 'No description'}<br><br>
                        Regards,<br>Your Task Tracker System
                    """,
                    now=True
                )
            except Exception as e:
                frappe.log_error(f"Failed to send assignment email to {row.assigned_to}: {e}", "Task Assignment Email Error")


@frappe.whitelist()
def get_project_members(doctype, txt, searchfield, start, page_len, filters):
    project = filters.get("project")
    if not project:
        return []

    members = frappe.get_all(
        "User Table",  
        filters={"parent": project},
        fields=["assigned_to"]
    )

    return [(m.assigned_to,) for m in members if m.assigned_to]
