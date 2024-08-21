frappe.ready(function() {
    // Retrieve the confer_id from local storage
    const storedConferId = localStorage.getItem('confer_id');
	

    if (storedConferId) {
		
				frappe.web_form.doc.parent = storedConferId;
				frappe.web_form.doc.parenttype = 'Confer'; 
				frappe.web_form.doc.parentfield = 'event_participant';
				frappe.web_form.column.doctype='event_participant';
				frappe.web_form.section.doctype='event_participant';
				frappe.web_form.section.doc.docstatus=0
				frappe.web_form.column.doc.docstatus=0
				frappe.web_form.doc.in_view_mode="true"
				


				console.log('Parentttt:', frappe.web_form.doc.parent);  // Debugging
				console.log('Parent tttttttttttttttttttttttttType:', frappe.web_form.doc.parenttype);  // Debugging
				console.log('Parent Field:', frappe.web_form.doc.parentfield); 
	        

        // Fetch and populate additional data
        frappe.call({
            method: 'e_desk.e_desk.web_form.event_participant_details.event_participant_details.form_update',
            args: { conf: storedConferId },
            callback: function(r) {
                if (r.message) {
                    if (r.message.event_dict) {

						// frappe.web_form.set_value("parent",storedConferId)
						frappe.web_form.doc.is_new="false"



						console.log(r.message.event_dict,"r.message.event_dictr.message.event_dict");
						
                        for (let key in r.message.event_dict) {
                            if (r.message.event_dict.hasOwnProperty(key)) {
                                frappe.web_form.set_value(key, r.message.event_dict[key]);
                            }
							// frappe.web_form.set_value(docstatus, 1);
							// frappe.web_form.doc.docstatus=1
                        }
						frappe.web_form.column.docname=r.message.event_dict['name']
						frappe.web_form.section.docname=r.message.event_dict['name']
                    }
                    if (r.message.confer) {
                        const targetElement = document.querySelector('.web-form-title.ellipsis');
                        const newDiv = document.createElement('div');
                        newDiv.innerHTML = `<h6>Event: ${r.message.confer.name}</h6><span>Start Date: ${r.message.confer.start_date}</span><span>End Date: ${r.message.confer.end_date}</span>`;
                        targetElement.appendChild(newDiv);
                    }
					
                }
            }
        });
		frappe.web_form.add_field({
            fieldname: 'parent',
            fieldtype: 'Data',
            default: storedConferId,
            hidden: 0
        });

        frappe.web_form.add_field({
            fieldname: 'parenttype',
            fieldtype: 'Data',
            default: 'Confer',
            hidden: 0
        });

        frappe.web_form.add_field({
            fieldname: 'parentfield',
            fieldtype: 'Data',
            default: 'event_participant',
            hidden: 0
        });
		frappe.web_form.refresh();
    } else {
        window.location.href = '/home';
    }

});
