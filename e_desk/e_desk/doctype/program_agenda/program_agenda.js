// Copyright (c) 2023, sathya and contributors
// For license information, please see license.txt

frappe.ui.form.on('Program Agenda', {
	validate: function(frm) {

        var child_table = frm.doc.agenda_details || [];
        child_table.sort(function(a, b) {
            return frappe.datetime.get_diff(a.from_time, b.from_time);
        });


		for (var i = 0; i < child_table.length - 1; i++) {
            var current_row = child_table[i];
            var next_row = child_table[i + 1];

            if (current_row['to_time'] >= next_row['from_time']) {
                frappe.msgprint(__('Time intervals should not overlap.'));
                frappe.validated = false;
                return;
            }
        }
    }
});

