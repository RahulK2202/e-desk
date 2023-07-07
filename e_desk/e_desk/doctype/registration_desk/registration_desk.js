// Copyright (c) 2023, sathya and contributors
// For license information, please see license.txt

frappe.ui.form.on('Registration Desk', {
	refresh:function(frm){
		frm.set_query('participant_id', 'participant', function() {
			return {
				filters: {
					'status': ['!=', 'Registered']
				}
			}
			
		})
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
		
		// if(frm.doc.part_profile){
		// 	let $profileimg = `
		// 		<img
		// 		class="sign"
		// 		src=${frm.doc.part_profile} 
		// 		/>
		// 		`
		// 		frm.get_field("profile_preview").$wrapper.html($profileimg);
		// }
		// if(frm.doc.part_profile){
		// 	let $profileimg = `
		// 		<img
		// 		class="sign"https://media.istockphoto.com/id/1313644269/vector/gold-and-silver-circle-star-logo-template.jpg?s=612x612&w=0&k=20&c=hDqCI9qTkNqNcKa6XS7aBim7xKz8cZbnm80Z_xiU2DI=
		// 		src=${frm.doc.part_profile} 
		// 		/>
		// 		`
		// 		frm.get_field("profile_preview").$wrapper.html($profileimg);
		// }
	},
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
