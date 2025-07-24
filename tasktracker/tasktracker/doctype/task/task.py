from frappe.model.document import Document
import frappe

class Task(Document):
    def on_update(self):
        self.send_assignment_emails()
        self.send_mail_to_tester()  

    def send_mail_to_tester(self):  
        if self.status == "Testing in Progress" and self.tester:
            try:
                tester_email = self.tester.strip()
                if frappe.db.exists("User", tester_email):
                    subject = f"Task {self.name} is ready for testing"
                    message = f"""
                        Hello Tester,<br><br>
                        The task <b>{self.task_name}</b> is now in <b>Testing in Progress</b>.<br><br>
                        Please review and complete the task.<br><br>
                        Regards,<br>Frappe System
                    """

                    frappe.sendmail(
                        recipients=[tester_email],
                        subject=subject,
                        message=message
                    )
            except Exception as e:
                frappe.log_error(f"Error sending email to tester: {str(e)}", "Task Email Error")


    def send_assignment_emails(self):
        if not self.assigned_to:
            return
        user = frappe.get_value("User", self.assigned_to)
        email = user.email or self.assigned_to
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
