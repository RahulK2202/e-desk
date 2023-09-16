// Copyright (c) 2023, sathya and contributors
// For license information, please see license.txt

frappe.ui.form.on('Participant', {

	//Create button for converting the participant to volunteer
	refresh: function(frm) {
		var hasPermission = frappe.user.has_role('Volunteer'); 
		if (!frm.is_new()){
			toggleEditFields(frm, false); 
			frm.add_custom_button(__('Editable'), function() {
				toggleEditFields(frm, true); 
			  });}
		
		if (hasPermission) {
			frm.add_custom_button(__('Volunteer'), function() {
	
				var Participant_details = frm.doc;
	
				console.log(Participant_details);
				return frappe.call({
					method: "e_desk.e_desk.doctype.participant.participant.volunteer_creation",
					args: { doc: Participant_details },
					callback: function() {
						frappe.msgprint("Volunteer Created Successfully");
					}
				});
			}, __("Create"));
		}
	},
	validate:function(frm) {
		toggleEditFields(frm, false); 

	},
	onload:function(frm){
		
	},
	

	capacity: async function(frm){
		await frappe.call({
			method: "run_doc_method",
			args: {
				'docs': frm.doc,
				'method': 'categoryfile_fetching'
			},
			callback: function (r) {
				if (!r.exc) {
					frm.refresh_fields();
				}
			}
		});

	}
}

);

function toggleEditFields(frm, isEditable) {
    var fieldnames = Object.keys(frm.fields_dict);
    for (var i = 0; i < fieldnames.length; i++) {
        var fieldname = fieldnames[i];
        if (frm.fields_dict[fieldname].df.fieldtype !== 'Section Break' &&
            frm.fields_dict[fieldname].df.fieldtype !== 'Column Break') {
            frm.toggle_enable(fieldname, isEditable);
        }
    }
}




// frappe.listview_settings['Participant'] = {	
// 	onload: function(listview) {
// 	listview.page.add_menu_item(__('Food Scanning'), function() {
// 			var d = new frappe.ui.Dialog({
// 				title: __("Food Scanning"),
// 				fields: [
// 					{
// 						"fieldtype": "Data",
// 						"label": __("Scan QR"),
// 						"fieldname": "scan_qr",
// 						"options":"Barcode"
// 					}
// 				],
// 				// primary_action: function (res) {
// 				// 	let values = d.get_values();
// 				// 	frappe.call({
// 				// 		method: "mehala.utils.py.quotation.rejection_updation",
// 				// 		args: {
// 				// 			docs: [{'name':cur_frm.doc.name}],
// 				// 			values: values,
// 				// 		},
// 				// 		callback: function (r) {
// 				// 			d.hide();
// 				// 			frm.reload_doc();
// 				// 		},
// 				// 	})
// 				// },
// 				primary_action_label: __('Submit')
// 			});
		
// 			d.show();
// 		},
// 	);
// },

// }
