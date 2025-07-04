import frappe
from frappe.utils import get_url
from frappe import _

@frappe.whitelist()
def initiate_testing(task_id, tester):
    if not task_id or not tester:
        frappe.throw(_("Task ID and Tester are required."))

    # Get the Task document
    task = frappe.get_doc("Task", task_id)

    # Create Task Testing Review document
    doc = frappe.get_doc({
        "doctype": "Task Testing Review",
        "task": task_id,
        "tester": tester
    })
    doc.insert(ignore_permissions=True)

    # Send email to tester
    link = f"{get_url()}/app/task-testing-review/{doc.name}"
   

    return doc.name
