frappe.ready(function() {
    // Bind the onchange event to the e_mail field
    $('input[data-fieldname="e_mail"]').on('change', function() {
        let email = $(this).val();
     
        if (email) {
      

            frappe.call({
                method: "e_desk.e_desk.web_form.participant_registration.participant_registration.check_user_exists",
                args: {
                    email: email
                },
                callback: function(response) {
                    
                    let user = response.message;

                    if (user) {
                        // Email exists, redirect to login
                  
                        frappe.msgprint({
                            title: __('Error'),
                            indicator: 'red',
                            message: __('This email is already registered.')
                        });
                     
                    } 
                 
                }
            });
        }
    });
});
