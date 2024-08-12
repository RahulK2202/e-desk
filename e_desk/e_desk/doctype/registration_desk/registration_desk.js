// Copyright (c) 2023, sathya and contributors
// For license information, please see license.txt

frappe.ui.form.on('Registration Desk', {

	setup: function(frm) {
        // Set query for the participant link field inside the Participant child table
        frm.set_query('participant_id', 'participant', function(doc, cdt, cdn) {
            return {
                query: 'e_desk.e_desk.doctype.registration_desk.registration_desk.event_participant_filter',
                filters: {
                    conference: frm.doc.confer
                }	
            };
        });
    },
	refresh:function(frm){
		
		let imgList = [];
		(frm.doc.participant || []).forEach(row => {
			imgList.push({'img': row.profile_img})
		});

		let imgHTML = ''

		imgList.forEach(img => {
			if (img.img) {
				imgHTML += `
				<div>
					<img src='${img.img}' alt='IMG' height="100" width="100">
					<br>
					<br>
				</div>
				`
			}
		});

		frm.get_field("profile_preview").$wrapper.html(imgHTML);


		let qrList = [];
		(frm.doc.participant || []).forEach(row => {
			qrList.push({'img': row.qr_img})
		});

		let qrHTML = ''

		qrList.forEach(img => {
			if (img.img) {
				qrHTML += `
				<div>
					<img src='${img.img}' alt='IMG' height="100" width="100">
					<br>
					<br>
				</div>
				`
			}
		});

		frm.get_field("qr_preview").$wrapper.html(qrHTML);
		

	},




// ONSUBMIT FUNCTION FOR THE REGISTRATION

// before_save: function(frm) {



	
// 	console.log("why submitted",frm.doc.participant[0].participant_id)
// 	// const participantId = frm.participant_id;

	
// 	const participantId = frm.doc.participant[0].participant_id
	
// 	const eventId = frm.doc.confer;

// 	// Call your custom function to add participant to the child table
// 	addParticipantToEvent(participantId, eventId);
// },













	participant_profile:function(frm){
		if(frm.doc.part_profile){
			let $profileimg = `
				<img
				class="sign"
				src=${frm.doc.part_profile} 
				/>
				`
				frm.get_field("profile_preview").$wrapper.html($profileimg);
		}
	},
});







// Custom function to add participant to the child table
// function addParticipantToEvent(participantId, eventId) {
// 	// Check if the participant is already registered for this event
// 	frappe.call({
// 		method: "e_desk.e_desk.doctype.registration_desk.registration_desk.add_participant_to_event", // Adjust the method path
// 		args: {
// 			participant_id: participantId,
// 			event_id: eventId
// 		},
// 		callback: function(response) {
// 			if (response.message === "success") {
// 				frappe.msgprint("Participant added successfully.");
// 			} else {
// 				frappe.msgprint("Participant is already registered for this event.");
// 			}
// 		}
// 	});
// 	}