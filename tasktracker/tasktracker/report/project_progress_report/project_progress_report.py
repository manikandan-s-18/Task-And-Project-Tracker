import frappe

def execute(filters=None):
    columns = [
        {"label": "Project", "fieldname": "project", "fieldtype": "Link", "options": "Project", "width": 150},
        {"label": "Total Tasks", "fieldname": "total_tasks", "fieldtype": "Int", "width": 120},
        {"label": "Completed Tasks", "fieldname": "completed_tasks", "fieldtype": "Int", "width": 150},
        {"label": "Completion %", "fieldname": "completion_percent", "fieldtype": "Percent", "width": 130},
    ]

    data = frappe.db.sql("""
        SELECT 
            t.project,
            COUNT(t.name) AS total_tasks,
            SUM(CASE WHEN t.status = 'Completed' THEN 1 ELSE 0 END) AS completed_tasks,
            ROUND(
                (SUM(CASE WHEN t.status = 'Completed' THEN 1 ELSE 0 END) / COUNT(t.name)) * 100, 2
            ) AS completion_percent
        FROM `tabTask` t
        WHERE t.project IS NOT NULL
        GROUP BY t.project
        ORDER BY t.project
    """, as_dict=1)

    return columns, data
