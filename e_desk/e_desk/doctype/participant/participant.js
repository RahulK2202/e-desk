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
					
					let d = new frappe.ui.Dialog({
						title: 'Enter details',
						fields: [
							{
								label: 'Confer List',
								fieldname: 'confer',
								fieldtype: 'Link',
								options: 'Confer',
								reqd: 1 ,
								get_query: function() {
									return {
										query: "e_desk.e_desk.utils.role.get_filtered_confer",
										filters: {
											participant: frm.doc.name  // Pass the participant name
										}
									};
								}
							}
						],
						primary_action_label: 'Submit',
						primary_action(values) {    
								frappe.call({
									method: "e_desk.e_desk.utils.role.update_event_participant_role",
									args: {
										participant: frm.doc.name,
										confer: values.confer,
										role_name:'Volunteer'
									},
									callback: function() {
										frappe.msgprint("Volunteer Created Successfully");
										d.hide(); 
									}
								});
						}
					});
					d.show();
				}, __("Create"));
			}

		let qrHTML = ''
			if (frm.doc.qr) {
				qrHTML += `
				<div>
					<img src='${frm.doc.qr}' alt='IMG' height="100" width="100">
					<br>
					<br>
				</div>
				`
			}
		

		frm.get_field("qr_preview").$wrapper.html(qrHTML);
	},

	onload:function(frm){
		
	},
	
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
	var user= 'mathew@gmail.com'
    var fieldnames = Object.keys(frm.fields_dict);
    for (var i = 0; i < fieldnames.length; i++) {
        var fieldname = fieldnames[i];
		if(frappe.session.user != user){
			if (frm.fields_dict[fieldname].df.fieldtype !== 'Section Break' &&
				frm.fields_dict[fieldname].df.fieldtype !== 'Column Break' &&
				isEditable?!frm.fields_dict[fieldname].df.reqd:true )
				{
				frm.toggle_enable(fieldname, isEditable);
        }}
		else{
			if (frm.fields_dict[fieldname].df.fieldtype !== 'Section Break' &&
				frm.fields_dict[fieldname].df.fieldtype !== 'Column Break')
				{
				frm.toggle_enable(fieldname, isEditable);
        }
		}
    }
}
