admin_rights_list = {
    "channel": ["can_post_messages", "can_delete_messages"],
    "group": ["can_delete_messages"],
    "supergroup": ["can_delete_messages"]
}
    
def get_admin_rights(member, rights_list):
    return {
        prop: getattr(member, prop, False)
        for prop in rights_list
    }

def get_missing_rights(member, rights_list):
    return [
        prop for prop in rights_list 
        if not getattr(member, prop, True)
    ]

def check_all_admin_rights(member, rights_list):
    rights = [
        getattr(member, prop, False) 
        for prop in rights_list
    ]
    return all(rights)