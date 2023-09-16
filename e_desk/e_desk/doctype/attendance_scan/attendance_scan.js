// Copyright (c) 2023, sathya and contributors
// For license information, please see license.txt

frappe.ui.form.on('Attendance Scan', {
	setup: function(frm) {
        frm.disable_save();
    },
	submit: function(frm) {
		var name = JSON.parse(frm.doc.scan_qr).name;
		frm.set_value("scan_qr","")
				frappe.call({
				method: "e_desk.e_desk.doctype.participant.participant.validate_attendance",
				args: {
					doc: name,
				},
				callback:function(r){
					if (r.message){
						frappe.show_alert({message:"Attendance Created Sucessfully", indicator:'green'});

					}
					
				}

			})
		},
});
