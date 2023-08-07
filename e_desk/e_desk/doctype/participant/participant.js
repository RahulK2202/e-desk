// Copyright (c) 2023, sathya and contributors
// For license information, please see license.txt

frappe.ui.form.on('Participant', {

	//Create button for converting the participant to volunteer
	refresh: function(frm) {
		frm.add_custom_button(__('Volunteer'), function(){

			var Participant_details = frm.doc
			
			console.log(Participant_details)
			return frappe.call(
				{
					method:"e_desk.e_desk.doctype.participant.participant.volunteer_creation",
					args:{doc:Participant_details},
					callback:function(){
						frappe.msgprint("Volunteer Created Successfully")
					}
				}
			)
		}, __("Create")
		);
	},
	capacity: function(frm){
		console.log(frm.doc)
		frappe.call(
			{
				method:"e_desk.e_desk.doctype.participant.participant.categoryfile_fetching",
				args:{
					capacity_name:frm.doc.capacity,
					doc:frm.doc,
				},
				callback:function(capacity_link){
					frm.reload_doc()
					// frm.set_value("category_files",capacity_link["message"])
				}
			},
			
		)
	}
}
);
