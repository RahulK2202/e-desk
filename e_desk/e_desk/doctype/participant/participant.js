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
	// validate:function(frm) {
	// 	toggleEditFields(frm, false); 

	// },
	onload:function(frm){
		
	},
	

	// capacity: async function(frm){
	// 	await frappe.call({
	// 		method: "run_doc_method",
	// 		args: {
	// 			'docs': frm.doc,
	// 			'method': 'categoryfile_fetching'
	// 		},
	// 		callback: function (r) {
	// 			if (!r.exc) {
	// 				frm.refresh_fields();
	// 			}
	// 		}
	// 	});

	// },
	get_directions:function(frm){
	
		if (frm.doc.location_url) {
			const mapURL = frm.doc.location_url;
	
			window.open(mapURL);

		} else {
			frappe.msgprint(__('Location URL is required to navigate to the map.'));
		}
	},
	get_directions_church:function(frm){
	
		if (frm.doc.location_url_church) {
			const mapURL = frm.doc.location_url_church;
	
			window.open(mapURL);

		} else {
			frappe.msgprint(__('Location URL is required to navigate to the map.'));
		}
	},
	hotel: function (frm) {
			var selectedHotel = frm.doc.hotel;
			if (selectedHotel) {
				frappe.call({
					method: "e_desk.e_desk.doctype.participant.participant.full_address",
					args: {
						address: frm.doc.hotel,
					},
					callback: function (search_text) {
						frm.set_value('hotel_address', search_text.message);
					}
				});
			}
		},
	church_list: function (frm) {
		var selectedchurch = frm.doc.church_list;
		if (selectedchurch) {
			frappe.call({
				method: "e_desk.e_desk.doctype.participant.participant.full_address_church",
				args: {
					address: frm.doc.church_list,
				},
				callback: function (search_text) {
					frm.set_value('church_address', search_text.message);
				}
			});
		}
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
