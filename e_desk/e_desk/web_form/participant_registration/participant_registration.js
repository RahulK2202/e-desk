// frappe.ready(function() {
//     // Bind the onchange event to the e_mail field
//     $('input[data-fieldname="e_mail"]').on('change', function() {
//         let email = $(this).val();

//         if (email) {
//             console.log(email, "if caseee");

//             frappe.call({
//                 method: "e_desk.e_desk.web_form.participant_registration.participant_registration.check_user_exists",
//                 args: {
//                     email: email
//                 },
//                 callback: function(response) {

//                     console.log(response,"responseresponseresponseresponseresponse")
//                     let user = response.message;

//                     if (user) {
//                         // Email exists, redirect to login
//                         console.log(user, "this is user");
//                         frappe.msgprint({
//                             title: __('Error'),
//                             indicator: 'red',
//                             message: __('This email is already registered.')
//                         });

//                         // Redirect to Frappe login page
//                         // window.location.href = "/login";
//                     } 
//                     // else {
//                     //     // Email does not exist
//                     //     frappe.msgprint("This email is available.");
//                     // }
//                 }
//             });
//         }
//     });
// });
