frappe.ready(function() {
	// bind events here



	const urlParams = new URLSearchParams(window.location.search);
	const my_param = urlParams.get('your_get_param'); 
	console.log(urlParams,my_param,"my_parammy_parammy_parammy_parammy_parammy_param")
	frappe.web_form.set_value('your_field', my_param)






})