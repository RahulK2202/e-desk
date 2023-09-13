// Copyright (c) 2023, sathya and contributors
// For license information, please see license.txt

frappe.ui.form.on('Hotel', {
	refresh: function(frm) {
		if (frm.doc.latitude && frm.doc.longitude) {
			const map = frm.get_field('location').map;
			const marker = L.marker([frm.doc.latitude, frm.doc.longitude]).addTo(map);
	  
			marker.bindPopup(frm.doc.hotel).openPopup();
		  }
		frm.set_query('address', function(doc) {
			return {
				filters: {
					'link_doctype': 'Hotel',
					'link_name': doc.name
				}
			}
		})
	}
});
