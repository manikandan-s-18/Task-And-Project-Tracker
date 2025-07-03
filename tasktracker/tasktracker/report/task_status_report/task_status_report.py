import frappe

def execute(filters=None):
    columns = [
        {"label": "Task", "fieldname": "name", "fieldtype": "Link", "options": "Task", "width": 150},
        {"label": "Project", "fieldname": "project", "fieldtype": "Link", "options": "Project", "width": 150},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 120},
        {"label": "Assigned To", "fieldname": "assigned_to", "fieldtype": "Data", "width": 200},
        {"label": "Due Date", "fieldname": "due_date", "fieldtype": "Date", "width": 100},
        {"label": "Completion %", "fieldname": "completion_percent", "fieldtype": "Percent", "width": 120},
    ]

    data = frappe.db.sql("""
        SELECT 
            t.name, t.project, t.status, ut.assigned_to, t.due_date, t.completion_percent
        FROM `tabTask` t
        LEFT JOIN `tabUser Table` ut 
            ON ut.parent = t.name AND ut.parenttype = 'Task'
        ORDER BY t.status, t.project
    """, as_dict=1)

    return columns, data
