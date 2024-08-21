import frappe

def get_context(context):
    pass
# 
   
@frappe.whitelist(allow_guest=True)
def form_update(conf):
 
    user = frappe.db.get_value('User', frappe.session.user, 'participant_id')
    

    exist = frappe.get_value('Event Participant', {'participant': user, 'parent': conf}, 'name')
    

    conf_doc = frappe.get_doc('Confer', conf)
    

    event_dict = {}
    
 
    if exist:
        event = frappe.get_doc('Event Participant', exist)
        event_dict = event.as_dict()
        print( event_dict," event_dict event_dict event_dict")
    

    data = {
        'confer': conf_doc.as_dict(), 
        'event_dict': event_dict
    }

    print(data,"this is data we using......................")
    
    return data
