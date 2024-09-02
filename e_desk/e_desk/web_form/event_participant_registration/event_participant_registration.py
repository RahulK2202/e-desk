import frappe

def get_context(context):
	# do your magic here
	pass



@frappe.whitelist(allow_guest=True)
def check_user_exists(email):
    print("yes exist.................")
    print(email,"email................")
    user = frappe.db.get_value("User", {"email": email})
    
    if user:
        return user
    else:
        return None