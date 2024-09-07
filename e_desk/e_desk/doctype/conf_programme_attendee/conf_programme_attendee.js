// Copyright (c) 2024, sathya and contributors
// For license information, please see license.txt
frappe.ui.form.on('Conf Programme Attendee', {


	setup: function(frm) {
        // frm.disable_save();
    },
	submit: function(frm) {
		var name = JSON.parse(frm.doc.scan_qr).name;
		console.log(name,"this is name/.....................................................")
		frm.set_value("scan_qr","")
				frappe.call({
				method: "e_desk.e_desk.doctype.conf_programme_attendee.conf_programme_attendee.scanning_validations",
				args: {
					doc: name,
					programme:frm.doc.programme
				},
				callback:function(r){
					if (r.message) {
						// Show success alert
						frappe.show_alert({message: "Attendance Scanned Successfully", indicator: 'green'});

						// Add a new item to the scanned_list child table
						var item = cur_frm.add_child("scanned_list");
						frappe.model.set_value(item.doctype, item.name, "participant", r.message.event_participant_id);
						frappe.model.set_value(item.doctype, item.name, "participant_name", r.message.full_name);
						frappe.model.set_value(item.doctype, item.name, "programme", frm.doc.programme);
						frappe.model.set_value(item.doctype, item.name, "date_time", frappe.datetime.now_datetime());

						// Refresh and save the form
						cur_frm.refresh_field('scanned_list');
						cur_frm.save();
					
						
					}
					}

			})
		},

    refresh: function(frm) {

		// frm.set_value('programme', '');
		
        frm.set_query('programme', function() {
			
            const today = frappe.datetime.get_today();
            const startOfDay = today + ' 00:00:00'; // Start of today
            const endOfDay = today + ' 23:59:59';   // End of today

            console.log(today, "Today’s date");

            return {
                filters: [
                    ['Confer Agenda', 'start_date', '>=', startOfDay],
                    ['Confer Agenda', 'end_date', '<=', endOfDay]
                ]
            };
        });
    },


});
