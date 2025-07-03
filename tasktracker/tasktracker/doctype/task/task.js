frappe.ui.form.on('Task', {
    onload: function(frm) {
        frm.set_query('assigned_to', 'assigned_to', function(doc, cdt, cdn) {
            if (!doc.project) {
                frappe.msgprint(__('Please select a Project first'));
                return {};
            }

            return {
                query: "tasktracker.tasktracker.doctype.task.task.get_project_members",
                filters: {
                    project: doc.project
                }
            };
        });
    }
});
