import frappe

def send_weekly_project_summary():
    projects = frappe.get_all("Project", filters={"status": ["!=", "Completed"]}, fields=["name", "project_manager"])

    for project in projects:
        tasks = frappe.get_all(
            "Task",
            filters={"project": project.name},
            fields=["name", "status", "due_date"]
        )

        # Build task summary
        task_lines = ""
        for task in tasks:
            task_lines += f"<li>{task.name} - {task.status} - Due: {task.due_date}</li>"

        # Add project link
        project_link = f'<p><a href="{frappe.utils.get_url()}/app/project/{project.name}">View Project in Frappe</a></p>'

        # Final email body
        message = f"""
        <h3>Weekly Project Summary for {project.name}</h3>
        <ul>{task_lines}</ul>
        {project_link}
        """

        # Send the email
        if project.project_manager:
            frappe.sendmail(
                recipients=project.project_manager,
                subject=f"Weekly Summary: {project.name}",
                message=message,
                now=True
            )
