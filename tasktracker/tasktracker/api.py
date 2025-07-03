# your_app/api.py
import frappe

@frappe.whitelist()
def initiate_testing(task_id, tester):
    task = frappe.get_doc("Task", task_id)

    doc = frappe.get_doc({
        "doctype": "Task Testing Review",
        "task": task_id,
        "tester": tester
    })
    doc.insert(ignore_permissions=True)

    # Send mail to tester
    link = f"{frappe.utils.get_url()}/app/task-testing-review/{doc.name}"
    frappe.sendmail(
        recipients=[tester],
        subject=f"Task Testing Assigned: {task.subject}",
        message=f"""
        Hello,<br><br>
        You are assigned to test the task: <b>{task.subject}</b>.<br>
        <a href="{link}">Click here to test</a><br><br>
        Regards,<br>Your Task Tracker
        """
    )

    return doc.name
